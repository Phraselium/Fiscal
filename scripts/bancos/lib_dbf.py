"""Lectura y escritura de ficheros DBF (dBase III), que es lo que usa ContaPlus.

No es una dependencia externa a proposito: el XDIARIO tiene unos 98 campos y su
estructura cambia entre versiones de ContaPlus, asi que el generador NO codifica
ninguna estructura. La lee del fichero muestra del cliente y la replica byte a
byte. Este modulo es solo la mecanica del formato.

Estructura del fichero
----------------------
Cabecera, 32 bytes:
    0       version (0x03 = dBase III sin memo)
    1-3     fecha de actualizacion: ano-1900, mes, dia
    4-7     numero de registros           (uint32 little-endian)
    8-9     longitud de la cabecera       (uint16 little-endian)
    10-11   longitud de cada registro     (uint16 little-endian)
    12-31   reservado, a cero

Descriptor de campo, 32 bytes por campo:
    0-10    nombre, rellenado con \\x00
    11      tipo: C texto, N numerico, D fecha, L logico
    12-15   direccion del campo (no se usa)
    16      longitud
    17      decimales
    18-31   reservado

Despues de los descriptores, el terminador 0x0D. Luego los registros, cada uno
precedido de un byte de marca de borrado (0x20 activo, 0x2A borrado). Al final
del fichero, 0x1A.

Codificacion: cp850, que es la que usa ContaPlus en Espana.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Iterator

CODIFICACION = "cp850"
ACTIVO = 0x20
BORRADO = 0x2A
TERMINADOR_CABECERA = 0x0D
FIN_FICHERO = 0x1A


class ErrorDBF(Exception):
    """El fichero no tiene la estructura esperada."""


@dataclass(frozen=True)
class Campo:
    nombre: str
    tipo: str
    longitud: int
    decimales: int

    def a_bytes(self) -> bytes:
        nombre = self.nombre.upper().encode("ascii", "replace")[:10]
        return (nombre.ljust(11, b"\x00")
                + self.tipo.encode("ascii")
                + b"\x00" * 4
                + bytes([self.longitud, self.decimales])
                + b"\x00" * 14)


@dataclass
class Estructura:
    """La estructura de un DBF, tal como se lee del fichero muestra."""
    version: int
    campos: list[Campo]
    longitud_registro: int
    longitud_cabecera: int

    @property
    def nombres(self) -> list[str]:
        return [c.nombre for c in self.campos]

    def campo(self, nombre: str) -> Campo | None:
        nombre = nombre.upper()
        return next((c for c in self.campos if c.nombre == nombre), None)

    def coincide_con(self, otra: "Estructura") -> list[str]:
        """Diferencias con otra estructura. Vacio = identicas."""
        fallos = []
        if self.version != otra.version:
            fallos.append(f"version {self.version:#04x} vs {otra.version:#04x}")
        if self.longitud_registro != otra.longitud_registro:
            fallos.append(f"longitud de registro {self.longitud_registro} vs "
                          f"{otra.longitud_registro}")
        if len(self.campos) != len(otra.campos):
            fallos.append(f"{len(self.campos)} campos vs {len(otra.campos)}")
            return fallos
        for a, b in zip(self.campos, otra.campos):
            if a != b:
                fallos.append(f"campo {a.nombre}: {a.tipo}{a.longitud},{a.decimales} vs "
                              f"{b.tipo}{b.longitud},{b.decimales}")
        return fallos


def leer_estructura(ruta: str | Path) -> Estructura:
    datos = Path(ruta).read_bytes()
    if len(datos) < 32:
        raise ErrorDBF(f"{ruta}: demasiado corto para ser un DBF")
    version = datos[0]
    longitud_cabecera, longitud_registro = struct.unpack("<HH", datos[8:12])
    campos: list[Campo] = []
    pos = 32
    while pos < len(datos) and datos[pos] != TERMINADOR_CABECERA:
        bruto = datos[pos:pos + 32]
        if len(bruto) < 32:
            raise ErrorDBF(f"{ruta}: descriptor de campo truncado en {pos}")
        nombre = bruto[:11].split(b"\x00")[0].decode("ascii", "replace").strip()
        campos.append(Campo(nombre, chr(bruto[11]), bruto[16], bruto[17]))
        pos += 32
    if not campos:
        raise ErrorDBF(f"{ruta}: no tiene campos")
    return Estructura(version, campos, longitud_registro, longitud_cabecera)


def leer(ruta: str | Path, incluir_borrados: bool = False) -> Iterator[dict[str, Any]]:
    """Recorre los registros como diccionarios, con los tipos ya convertidos."""
    datos = Path(ruta).read_bytes()
    est = leer_estructura(ruta)
    numero = struct.unpack("<I", datos[4:8])[0]

    pos = est.longitud_cabecera
    leidos = 0
    while pos + est.longitud_registro <= len(datos) and leidos < numero:
        marca = datos[pos]
        if marca == FIN_FICHERO:
            break
        bruto = datos[pos + 1:pos + est.longitud_registro]
        pos += est.longitud_registro
        leidos += 1
        if marca == BORRADO and not incluir_borrados:
            continue
        registro: dict[str, Any] = {}
        desplazamiento = 0
        for campo in est.campos:
            crudo = bruto[desplazamiento:desplazamiento + campo.longitud]
            desplazamiento += campo.longitud
            registro[campo.nombre] = _convertir(campo, crudo)
        registro["_borrado"] = marca == BORRADO
        yield registro


def _convertir(campo: Campo, crudo: bytes) -> Any:
    texto = crudo.decode(CODIFICACION, "replace")
    if campo.tipo == "C":
        return texto.rstrip()
    if campo.tipo == "N":
        limpio = texto.strip()
        if not limpio or limpio in ("-", "."):
            return 0.0 if campo.decimales else 0
        try:
            return float(limpio) if campo.decimales else int(float(limpio))
        except ValueError:
            return 0.0 if campo.decimales else 0
    if campo.tipo == "D":
        limpio = texto.strip()
        if len(limpio) != 8 or not limpio.isdigit():
            return None
        try:
            return datetime.strptime(limpio, "%Y%m%d").date()
        except ValueError:
            return None
    if campo.tipo == "L":
        return texto.strip().upper() in ("T", "Y", "S", "1")
    return texto.rstrip()


def formatear(campo: Campo, valor: Any) -> bytes:
    """Convierte un valor al formato exacto que espera el campo."""
    if campo.tipo == "C":
        texto = "" if valor is None else str(valor)
        return texto.encode(CODIFICACION, "replace")[:campo.longitud].ljust(campo.longitud, b" ")

    if campo.tipo == "N":
        if valor is None or valor == "":
            valor = 0
        texto = f"{float(valor):{campo.longitud}.{campo.decimales}f}"
        if len(texto) > campo.longitud:
            raise ErrorDBF(
                f"El valor {valor} no cabe en el campo {campo.nombre} "
                f"(N{campo.longitud},{campo.decimales})")
        return texto.encode("ascii").rjust(campo.longitud, b" ")

    if campo.tipo == "D":
        if not valor:
            return b" " * campo.longitud
        if isinstance(valor, str):
            valor = datetime.strptime(valor[:10].replace("/", "-"), "%Y-%m-%d").date()
        if isinstance(valor, datetime):
            valor = valor.date()
        return valor.strftime("%Y%m%d").encode("ascii").ljust(campo.longitud, b" ")

    if campo.tipo == "L":
        return (b"T" if valor is True else b"F").ljust(campo.longitud, b" ")

    return b" " * campo.longitud


def valor_por_defecto(campo: Campo) -> Any:
    """Lo que va en un campo que no se rellena: ni nulos ni basura."""
    return {"C": "", "N": 0, "D": None, "L": False}.get(campo.tipo, "")


def escribir(ruta: str | Path, estructura: Estructura,
             registros: Iterable[dict[str, Any]]) -> int:
    """Escribe el DBF replicando la estructura recibida. Devuelve el nº de registros."""
    filas = list(registros)
    hoy = date.today()

    longitud_cabecera = 32 + 32 * len(estructura.campos) + 1
    longitud_registro = 1 + sum(c.longitud for c in estructura.campos)
    if longitud_registro != estructura.longitud_registro:
        raise ErrorDBF(
            f"La suma de los campos da {longitud_registro} bytes por registro y la "
            f"estructura declara {estructura.longitud_registro}")

    partes = [struct.pack(
        "<BBBBIHH20x", estructura.version, hoy.year - 1900, hoy.month, hoy.day,
        len(filas), longitud_cabecera, longitud_registro)]
    partes.extend(c.a_bytes() for c in estructura.campos)
    partes.append(bytes([TERMINADOR_CABECERA]))

    for fila in filas:
        registro = [bytes([ACTIVO])]
        for campo in estructura.campos:
            valor = fila.get(campo.nombre, valor_por_defecto(campo))
            registro.append(formatear(campo, valor))
        linea = b"".join(registro)
        if len(linea) != longitud_registro:
            raise ErrorDBF(f"Registro de {len(linea)} bytes, se esperaban {longitud_registro}")
        partes.append(linea)

    partes.append(bytes([FIN_FICHERO]))
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(b"".join(partes))
    return len(filas)


def crear_estructura(campos: list[tuple[str, str, int, int]], version: int = 0x03) -> Estructura:
    """Solo para pruebas: construye una estructura desde una lista de tuplas."""
    objetos = [Campo(n.upper(), t, l, d) for n, t, l, d in campos]
    return Estructura(version, objetos, 1 + sum(c.longitud for c in objetos),
                      32 + 32 * len(objetos) + 1)
