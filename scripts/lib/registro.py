"""Motor genérico de generación de ficheros en diseño de registro AEAT.

Los ficheros de las declaraciones informativas de la AEAT son ficheros de texto
de registros de longitud fija (habitualmente 250 posiciones), codificados en
ISO-8859-1 y con separador de registro CRLF.

Este módulo NO codifica el diseño de ningún modelo concreto: lee la definición
desde un fichero JSON de `disenos/` y la aplica. Así, cuando la AEAT publica una
orden que modifica el diseño, basta con actualizar el JSON.

Tipos de campo soportados
-------------------------
A   Alfanumérico. Ajustado a la izquierda, relleno con espacios a la derecha.
N   Numérico entero. Ajustado a la derecha, relleno con ceros a la izquierda.
I   Importe. Se expresa en céntimos sin separador decimal, ajustado a la
    derecha y relleno con ceros. El valor de entrada es un número en euros.
S   Signo. Una posición: " " si el importe asociado es positivo, "N" si es
    negativo. Se declara con `campo_importe` apuntando al campo que firma.
C   Constante. Valor fijo declarado en el propio diseño.
X   Relleno / blancos.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Iterable

CODIFICACION = "iso-8859-1"
FIN_REGISTRO = "\r\n"


class ErrorDiseno(Exception):
    """El diseño de registro es inconsistente."""


class ErrorDato(Exception):
    """Un dato de entrada no encaja en el campo que le corresponde."""


# --------------------------------------------------------------------------
# Normalización de texto
# --------------------------------------------------------------------------

_SUSTITUCIONES = {"Ñ": "Ñ", "Ç": "Ç"}


def normalizar_texto(valor: Any) -> str:
    """Mayúsculas sin acentos, conservando Ñ y Ç, apto para ISO-8859-1."""
    if valor is None:
        return ""
    texto = str(valor).upper().strip()
    salida = []
    for caracter in texto:
        if caracter in _SUSTITUCIONES:
            salida.append(caracter)
            continue
        descompuesto = unicodedata.normalize("NFD", caracter)
        base = "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")
        salida.append(base if base else caracter)
    texto = "".join(salida)
    try:
        texto.encode(CODIFICACION)
    except UnicodeEncodeError:
        texto = texto.encode(CODIFICACION, errors="replace").decode(CODIFICACION)
    return texto


def normalizar_nif(valor: Any) -> str:
    """NIF/NIE/CIF en 9 posiciones, sin guiones ni espacios."""
    if valor is None:
        return ""
    nif = re.sub(r"[^0-9A-Za-z]", "", str(valor)).upper()
    return nif.rjust(9, "0") if nif and nif[0].isdigit() and len(nif) < 9 else nif


def a_centimos(valor: Any) -> int:
    """Convierte un importe en euros a céntimos enteros, redondeando a la mitad arriba."""
    if valor is None or valor == "":
        return 0
    if isinstance(valor, str):
        limpio = valor.replace(".", "").replace(",", ".").replace("€", "").strip()
        if limpio in ("", "-"):
            return 0
        valor = limpio
    cantidad = Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(cantidad * 100)


# --------------------------------------------------------------------------
# Diseño
# --------------------------------------------------------------------------


@dataclass
class Campo:
    nombre: str
    desde: int
    hasta: int
    tipo: str
    valor: Any = None
    obligatorio: bool = False
    campo_importe: str | None = None
    descripcion: str = ""

    @property
    def longitud(self) -> int:
        return self.hasta - self.desde + 1


@dataclass
class Diseno:
    modelo: str
    longitud: int
    registros: dict[str, list[Campo]]
    fuente: str = ""
    verificado: bool = False
    descripcion: str = ""

    @classmethod
    def cargar(cls, ruta: str | Path) -> "Diseno":
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        registros: dict[str, list[Campo]] = {}
        for tipo_registro, campos in datos["registros"].items():
            registros[str(tipo_registro)] = [
                Campo(
                    nombre=c["nombre"],
                    desde=int(c["desde"]),
                    hasta=int(c["hasta"]),
                    tipo=c["tipo"].upper(),
                    valor=c.get("valor"),
                    obligatorio=bool(c.get("obligatorio", False)),
                    campo_importe=c.get("campo_importe"),
                    descripcion=c.get("descripcion", ""),
                )
                for c in campos
            ]
        diseno = cls(
            modelo=str(datos["modelo"]),
            longitud=int(datos.get("longitud", 250)),
            registros=registros,
            fuente=datos.get("fuente", ""),
            verificado=bool(datos.get("verificado", False)),
            descripcion=datos.get("descripcion", ""),
        )
        diseno.comprobar()
        return diseno

    def comprobar(self) -> None:
        """Verifica que cada registro cubre exactamente las posiciones 1..longitud."""
        for tipo_registro, campos in self.registros.items():
            ordenados = sorted(campos, key=lambda c: c.desde)
            posicion = 1
            for campo in ordenados:
                if campo.desde != posicion:
                    raise ErrorDiseno(
                        f"Modelo {self.modelo}, registro {tipo_registro}: hueco o "
                        f"solapamiento en la posición {posicion} "
                        f"(el campo '{campo.nombre}' empieza en {campo.desde})"
                    )
                if campo.hasta < campo.desde:
                    raise ErrorDiseno(
                        f"Campo '{campo.nombre}': 'hasta' ({campo.hasta}) es menor "
                        f"que 'desde' ({campo.desde})"
                    )
                posicion = campo.hasta + 1
            if posicion - 1 != self.longitud:
                raise ErrorDiseno(
                    f"Modelo {self.modelo}, registro {tipo_registro}: el diseño cubre "
                    f"{posicion - 1} posiciones y se esperaban {self.longitud}"
                )


# --------------------------------------------------------------------------
# Formateo de campos
# --------------------------------------------------------------------------


def formatear_campo(campo: Campo, datos: dict[str, Any]) -> str:
    longitud = campo.longitud
    tipo = campo.tipo

    if tipo == "C":
        bruto = normalizar_texto(campo.valor)
        if len(bruto) > longitud:
            raise ErrorDato(f"Constante '{campo.nombre}' más larga que su campo")
        return bruto.ljust(longitud)

    if tipo == "X":
        return " " * longitud

    valor = datos.get(campo.nombre, campo.valor)

    if campo.obligatorio and (valor is None or str(valor).strip() == ""):
        raise ErrorDato(f"Falta el campo obligatorio '{campo.nombre}'")

    if tipo == "A":
        texto = normalizar_texto(valor)
        if len(texto) > longitud:
            texto = texto[:longitud]
        return texto.ljust(longitud)

    if tipo == "N":
        if valor is None or str(valor).strip() == "":
            return "0" * longitud
        digitos = re.sub(r"\D", "", str(valor))
        if len(digitos) > longitud:
            raise ErrorDato(
                f"El campo numérico '{campo.nombre}' ({digitos}) no cabe en "
                f"{longitud} posiciones"
            )
        return digitos.rjust(longitud, "0")

    if tipo == "I":
        centimos = abs(a_centimos(valor))
        texto = str(centimos)
        if len(texto) > longitud:
            raise ErrorDato(
                f"El importe '{campo.nombre}' ({centimos} céntimos) no cabe en "
                f"{longitud} posiciones"
            )
        return texto.rjust(longitud, "0")

    if tipo == "S":
        if not campo.campo_importe:
            raise ErrorDiseno(f"El campo de signo '{campo.nombre}' no declara 'campo_importe'")
        asociado = datos.get(campo.campo_importe)
        return ("N" if a_centimos(asociado) < 0 else " ").ljust(longitud)

    raise ErrorDiseno(f"Tipo de campo desconocido: '{tipo}' en '{campo.nombre}'")


def construir_registro(diseno: Diseno, tipo_registro: str, datos: dict[str, Any]) -> str:
    if tipo_registro not in diseno.registros:
        raise ErrorDiseno(
            f"El diseño del modelo {diseno.modelo} no define el registro de tipo "
            f"'{tipo_registro}'"
        )
    campos = sorted(diseno.registros[tipo_registro], key=lambda c: c.desde)
    linea = "".join(formatear_campo(campo, datos) for campo in campos)
    if len(linea) != diseno.longitud:
        raise ErrorDiseno(
            f"El registro generado tiene {len(linea)} posiciones y se esperaban "
            f"{diseno.longitud}"
        )
    return linea


def escribir_fichero(ruta: str | Path, lineas: Iterable[str]) -> Path:
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    contenido = FIN_REGISTRO.join(lineas) + FIN_REGISTRO
    destino.write_bytes(contenido.encode(CODIFICACION, errors="replace"))
    return destino


def validar_fichero(ruta: str | Path, longitud: int = 250) -> list[str]:
    """Devuelve la lista de incidencias encontradas en un fichero ya generado."""
    incidencias: list[str] = []
    datos = Path(ruta).read_bytes()
    try:
        texto = datos.decode(CODIFICACION)
    except UnicodeDecodeError as exc:
        return [f"El fichero no está codificado en {CODIFICACION}: {exc}"]

    if "\r\n" not in texto and texto.count("\n") > 0:
        incidencias.append("El separador de registro no es CRLF")

    lineas = texto.replace("\r\n", "\n").split("\n")
    if lineas and lineas[-1] == "":
        lineas.pop()

    if not lineas:
        return ["El fichero está vacío"]

    for numero, linea in enumerate(lineas, start=1):
        if len(linea) != longitud:
            incidencias.append(
                f"Registro {numero}: longitud {len(linea)}, se esperaban {longitud}"
            )
        if any(ord(c) > 255 for c in linea):
            incidencias.append(f"Registro {numero}: contiene caracteres fuera de ISO-8859-1")

    if lineas[0][:1] != "1":
        incidencias.append("El primer registro no es de tipo 1 (registro del declarante)")

    tipos = {linea[:1] for linea in lineas[1:]}
    if tipos and tipos - {"2", "3"}:
        incidencias.append(f"Tipos de registro inesperados en el detalle: {sorted(tipos)}")

    return incidencias
