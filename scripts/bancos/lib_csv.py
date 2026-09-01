#!/usr/bin/env python3
"""Lee y escribe el CSV de importacion (Sage 50 y cualquier otro).

MISMA REGLA DE ORO QUE EL DBF: aqui no se codifica ningun formato. Todo -el
delimitador, la codificacion, el orden y el nombre de las columnas, el formato
de fecha, el separador decimal- se deduce del fichero muestra del cliente y se
replica. No hay una "especificacion Sage 50" escrita a mano en este fichero,
porque no habria forma de verificarla: la unica fuente fiable es el fichero que
el cliente ya importa cada ano.

Expone la misma interfaz que lib_dbf, para que generar y verificar no tengan que
saber con que formato estan trabajando:

    leer_formato(ruta) -> FormatoCsv      .nombres  .campo()  .coincide_con()
    leer(ruta)         -> iterador de registros canonicos
    escribir(ruta, formato, registros) -> numero de lineas escritas

Los registros canonicos usan los nombres de campo del XDIARIO -ASIEN, FECHA,
SUBCTA, CONTRA, CONCEPTO, EURODEBE, EUROHABER- venga el fichero de donde venga.
Asi las diez comprobaciones de verificar_xdiario.py valen para los dos formatos.
"""

from __future__ import annotations

import csv
import io
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterator

CAMPOS_CANONICOS = ("ASIEN", "FECHA", "SUBCTA", "CONTRA", "CONCEPTO",
                    "EURODEBE", "EUROHABER")

# Como se llama cada campo en los ficheros que se ven por ahi. La comparacion es
# exacta sobre el nombre normalizado, no por subcadena: "contrapartida" no puede
# acabar tomandose por "cuenta".
SINONIMOS: dict[str, tuple[str, ...]] = {
    "ASIEN": ("asiento", "asien", "nasiento", "numasiento", "numeroasiento",
              "nroasiento", "ndeasiento", "diario", "apunte"),
    "FECHA": ("fecha", "fechaasiento", "fasiento", "fechaoperacion", "fechaapunte",
              "fecharegistro"),
    "SUBCTA": ("subcuenta", "cuenta", "cta", "codigocuenta", "codcuenta",
               "cuentacontable", "ctacontable", "codigosubcuenta"),
    "CONTRA": ("contrapartida", "contra", "cuentacontrapartida", "ctacontrapartida",
               "codigocontrapartida"),
    "CONCEPTO": ("concepto", "descripcion", "comentario", "detalle", "glosa",
                 "conceptoapunte", "textoexplicativo"),
    "EURODEBE": ("debe", "importedebe", "eurodebe", "cargo", "debeeuros", "debeeur"),
    "EUROHABER": ("haber", "importehaber", "eurohaber", "abono", "habereuros",
                  "habereur"),
}
# Variante de una sola columna de importe mas un indicador de debe/haber.
SINONIMOS_IMPORTE = ("importe", "importeeuros", "importeeur", "euros", "importemov")
SINONIMOS_DH = ("dh", "debehaber", "signo", "tipoimporte", "indicadordh", "tipo",
                "dhaber", "sentido")

CODIFICACIONES = ("utf-8-sig", "utf-8", "cp1252", "cp850", "latin-1")
FORMATOS_FECHA = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y", "%Y%m%d",
                  "%d/%m/%y", "%d%m%Y")
DELIMITADORES = (";", ",", "\t", "|")


class ErrorCSV(Exception):
    """El fichero muestra no permite deducir un formato utilizable."""


def normalizar(nombre: str) -> str:
    t = unicodedata.normalize("NFD", str(nombre).strip().lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", t)


@dataclass(frozen=True)
class Columna:
    nombre: str          # tal cual viene en la muestra
    campo: str | None    # campo canonico al que corresponde, o None

    @property
    def clave(self) -> str:
        """Con que clave viaja esta columna dentro de un registro."""
        return self.campo or self.nombre


@dataclass
class FormatoCsv:
    codificacion: str
    delimitador: str
    comillas: str
    salto: str
    cabecera: bool
    columnas: list[Columna]
    formato_fecha: str
    decimal: str
    miles: str
    modo_importe: str = "debe-haber"      # o "importe-dh"
    columna_dh: str | None = None
    marca_debe: str = "D"
    marca_haber: str = "H"
    # Columnas que valen siempre lo mismo en la muestra: son constantes del
    # formato (la empresa, el diario, la moneda). Se copian tal cual.
    constantes: dict[str, str] = field(default_factory=dict)

    @property
    def nombres(self) -> list[str]:
        """Con que claves viaja un registro de este formato.

        En modo importe-dh la columna IMPORTE se alimenta de EURODEBE y EUROHABER:
        el registro sigue siendo canonico y el reparto se hace al escribir.
        """
        salida: list[str] = []
        for c in self.columnas:
            if c.campo == "IMPORTE":
                salida += ["EURODEBE", "EUROHABER"]
            else:
                salida.append(c.clave)
        return salida

    def campo(self, nombre: str) -> Columna | None:
        nombre = nombre.upper()
        if nombre in ("EURODEBE", "EUROHABER") and self.modo_importe == "importe-dh":
            # El importe existe, solo que repartido en dos columnas distintas.
            return next((c for c in self.columnas if c.campo == "IMPORTE"), None)
        return next((c for c in self.columnas if c.campo == nombre), None)

    def plantilla(self) -> dict[str, Any]:
        base: dict[str, Any] = {}
        for c in self.columnas:
            if c.campo == "IMPORTE":
                base["EURODEBE"] = base["EUROHABER"] = 0.0
            else:
                base[c.clave] = self.constantes.get(c.nombre, "")
        return base

    def coincide_con(self, otro: "FormatoCsv") -> list[str]:
        """Diferencias con otro formato. Vacio = el fichero sale igual que la muestra."""
        fallos = []
        for atributo, etiqueta in (("codificacion", "codificación"),
                                   ("delimitador", "delimitador"),
                                   ("cabecera", "fila de cabecera"),
                                   ("decimal", "separador decimal"),
                                   ("formato_fecha", "formato de fecha"),
                                   ("modo_importe", "modo de importe")):
            a, b = getattr(self, atributo), getattr(otro, atributo)
            if a != b:
                fallos.append(f"{etiqueta}: {a!r} vs {b!r}")
        mios = [c.nombre for c in self.columnas]
        suyos = [c.nombre for c in otro.columnas]
        if mios != suyos:
            fallos.append(f"columnas: {len(mios)} vs {len(suyos)}"
                          if len(mios) != len(suyos)
                          else f"orden o nombre de columnas: {mios} vs {suyos}")
        return fallos

    def descripcion(self) -> str:
        mapeadas = [f"{c.nombre} → {c.campo}" for c in self.columnas if c.campo]
        sueltas = [c.nombre for c in self.columnas if not c.campo]
        lineas = [f"Codificación {self.codificacion}, delimitador {self.delimitador!r}, "
                  f"{'con' if self.cabecera else 'sin'} cabecera",
                  f"Fechas {self.formato_fecha}, decimales con {self.decimal!r}"
                  + (f" y miles con {self.miles!r}" if self.miles else ""),
                  "Columnas reconocidas:"]
        lineas += [f"    {m}" for m in mapeadas]
        if sueltas:
            lineas.append("Columnas que se copian de la muestra o van vacías:")
            lineas += [f"    {s}"
                       + (f" = {self.constantes[s]!r}" if s in self.constantes else " (vacía)")
                       for s in sueltas]
        return "\n".join(lineas)


# --- deteccion -----------------------------------------------------------

def _decodificar(ruta: Path) -> tuple[str, str]:
    crudo = Path(ruta).read_bytes()
    for codificacion in CODIFICACIONES:
        # utf-8-sig solo si el fichero trae BOM de verdad: al escribir lo anadiria,
        # y un BOM de mas en la primera cabecera rompe la importacion.
        if codificacion == "utf-8-sig" and not crudo.startswith(b"\xef\xbb\xbf"):
            continue
        try:
            return codificacion, crudo.decode(codificacion)
        except UnicodeDecodeError:
            continue
    raise ErrorCSV(f"{ruta}: no se ha podido decodificar con ninguna codificación conocida")


def _delimitador(primera: str) -> str:
    cuentas = {d: primera.count(d) for d in DELIMITADORES}
    mejor = max(cuentas, key=lambda d: cuentas[d])
    if not cuentas[mejor]:
        raise ErrorCSV("la primera línea no tiene ningún delimitador reconocible "
                       f"({', '.join(repr(d) for d in DELIMITADORES)})")
    return mejor


def _hay_cabecera(fila: list[str]) -> bool:
    """Una cabecera no lleva numeros ni fechas en sus celdas."""
    con_texto = [c for c in fila if c.strip()]
    if not con_texto:
        return False
    numericas = sum(1 for c in con_texto if re.fullmatch(r"[-+]?[\d.,/-]+", c.strip()))
    return numericas <= len(con_texto) // 4


def _mapear(nombres: list[str]) -> tuple[list[Columna], str, str | None]:
    usados: set[str] = set()
    columnas: list[Columna] = []
    normalizados = [normalizar(n) for n in nombres]

    def buscar(sinonimos) -> int | None:
        for i, n in enumerate(normalizados):
            if n in sinonimos and nombres[i] not in usados:
                return i
        return None

    asignado: dict[int, str] = {}
    for canonico in CAMPOS_CANONICOS:
        i = buscar(SINONIMOS[canonico])
        if i is not None:
            asignado[i] = canonico
            usados.add(nombres[i])

    modo, columna_dh = "debe-haber", None
    if "EURODEBE" not in asignado.values() and "EUROHABER" not in asignado.values():
        i = buscar(SINONIMOS_IMPORTE)
        j = buscar(SINONIMOS_DH)
        if i is not None and j is not None:
            asignado[i] = "IMPORTE"
            modo, columna_dh = "importe-dh", nombres[j]

    for i, nombre in enumerate(nombres):
        columnas.append(Columna(nombre, asignado.get(i)))
    return columnas, modo, columna_dh


def _formato_fecha(valores: list[str]) -> str:
    vivos = [v.strip() for v in valores if v.strip()]
    if not vivos:
        return FORMATOS_FECHA[0]
    for formato in FORMATOS_FECHA:
        try:
            for v in vivos:
                datetime.strptime(v, formato)
            return formato
        except ValueError:
            continue
    raise ErrorCSV(f"no se reconoce el formato de fecha de {vivos[0]!r}")


def _separadores(valores: list[str]) -> tuple[str, str]:
    """Devuelve (decimal, miles) mirando como vienen los importes de la muestra.

    El decimal se decide por mayoria. El de miles, NO: basta con que un solo
    importe venga agrupado para que el formato los lleve. Decidirlo por mayoria
    haria que en una muestra con muchos "342,50" y un "1.210,00" el agrupado se
    leyese mal -y un importe mal leido en un cuadre bancario no avisa, cuadra mal.
    """
    decimales, agrupados = Counter(), Counter()
    for v in valores:
        v = v.strip().lstrip("-+")
        if not v:
            continue
        if re.fullmatch(r"\d{1,3}(\.\d{3})+,\d+", v):
            decimales[","] += 1
            agrupados["."] += 1
        elif re.fullmatch(r"\d{1,3}(,\d{3})+\.\d+", v):
            decimales["."] += 1
            agrupados[","] += 1
        elif re.fullmatch(r"\d{1,3}(\.\d{3})+", v):
            agrupados["."] += 1
        elif re.fullmatch(r"\d{1,3}(,\d{3})+", v):
            agrupados[","] += 1
        elif re.fullmatch(r"\d+,\d+", v):
            decimales[","] += 1
        elif re.fullmatch(r"\d+\.\d+", v):
            decimales["."] += 1

    decimal = decimales.most_common(1)[0][0] if decimales else ","
    miles = next((m for m, _ in agrupados.most_common() if m != decimal), "")
    return decimal, miles


def leer_formato(ruta: str | Path) -> FormatoCsv:
    ruta = Path(ruta)
    codificacion, texto = _decodificar(ruta)
    lineas = texto.splitlines()
    if not lineas:
        raise ErrorCSV(f"{ruta}: está vacío")

    salto = "\r\n" if "\r\n" in texto else "\n"
    delimitador = _delimitador(lineas[0])
    filas = list(csv.reader(io.StringIO(texto), delimiter=delimitador))
    filas = [f for f in filas if any(c.strip() for c in f)]
    if not filas:
        raise ErrorCSV(f"{ruta}: no tiene ninguna fila con contenido")

    cabecera = _hay_cabecera(filas[0])
    if cabecera:
        nombres, datos = filas[0], filas[1:]
    else:
        # Sin cabecera no hay nombres que mapear: solo se puede replicar a ciegas.
        raise ErrorCSV(
            f"{ruta}: no tiene fila de cabecera, así que no se puede saber qué columna "
            "es cada cosa. Pásame una muestra con cabecera, o el mapeo a mano.")

    columnas, modo, columna_dh = _mapear(nombres)
    indice = {c.nombre: i for i, c in enumerate(columnas)}

    def columna(nombre: str | None) -> list[str]:
        if nombre is None or nombre not in indice:
            return []
        i = indice[nombre]
        return [f[i] for f in datos if i < len(f)]

    fechas = next((c.nombre for c in columnas if c.campo == "FECHA"), None)
    formato_fecha = _formato_fecha(columna(fechas))

    importes: list[str] = []
    for c in columnas:
        if c.campo in ("EURODEBE", "EUROHABER", "IMPORTE"):
            importes += columna(c.nombre)
    decimal, miles = _separadores(importes)

    constantes = {}
    for c in columnas:
        if c.campo:
            continue
        valores = {v.strip() for v in columna(c.nombre)}
        if len(valores) == 1 and datos and valores != {""}:
            constantes[c.nombre] = valores.pop()

    formato = FormatoCsv(codificacion=codificacion, delimitador=delimitador,
                         comillas='"', salto=salto, cabecera=cabecera,
                         columnas=columnas, formato_fecha=formato_fecha,
                         decimal=decimal, miles=miles, modo_importe=modo,
                         columna_dh=columna_dh, constantes=constantes)

    if modo == "importe-dh":
        marcas = sorted({v.strip().upper() for v in columna(columna_dh) if v.strip()})
        if len(marcas) == 2:
            formato.marca_debe, formato.marca_haber = marcas[0], marcas[1]
    return formato


def campos_que_faltan(formato: FormatoCsv) -> list[str]:
    """Campos canonicos sin columna en la muestra. Si hay alguno, no se genera."""
    faltan = []
    for campo_ in CAMPOS_CANONICOS:
        if campo_ in ("EURODEBE", "EUROHABER") and formato.modo_importe == "importe-dh":
            continue
        if formato.campo(campo_) is None:
            faltan.append(campo_)
    return faltan


# --- conversion de valores -----------------------------------------------

def _a_numero(texto: str, formato: FormatoCsv) -> float:
    """Un importe ilegible NO vale cero: se para y se dice cual es.

    Devolver 0.0 en silencio es la forma mas facil de entregar un fichero que
    cuadra sobre el papel y esta mal.
    """
    t = str(texto).strip()
    if not t:
        return 0.0
    if formato.miles:
        t = t.replace(formato.miles, "")
    t = t.replace(formato.decimal, ".")
    try:
        return float(t)
    except ValueError:
        raise ErrorCSV(
            f"no se puede leer el importe {texto!r} con separador decimal "
            f"{formato.decimal!r}"
            + (f" y de miles {formato.miles!r}" if formato.miles else "")) from None


def _de_numero(valor: float, formato: FormatoCsv) -> str:
    t = f"{float(valor):,.2f}"          # 1,234.56
    if formato.miles:
        t = t.replace(",", "\x00").replace(".", formato.decimal).replace("\x00", formato.miles)
    else:
        t = t.replace(",", "").replace(".", formato.decimal)
    return t


# --- lectura y escritura -------------------------------------------------

def leer(ruta: str | Path, formato: FormatoCsv | None = None) -> Iterator[dict[str, Any]]:
    """Registros canonicos: ASIEN, FECHA, SUBCTA, CONTRA, CONCEPTO, EURODEBE, EUROHABER."""
    ruta = Path(ruta)
    formato = formato or leer_formato(ruta)
    _, texto = _decodificar(ruta)
    filas = list(csv.reader(io.StringIO(texto), delimiter=formato.delimitador))
    filas = [f for f in filas if any(c.strip() for c in f)]
    if formato.cabecera:
        filas = filas[1:]

    for fila in filas:
        registro: dict[str, Any] = {}
        for i, columna in enumerate(formato.columnas):
            crudo = fila[i] if i < len(fila) else ""
            campo_ = columna.campo
            if campo_ == "FECHA":
                try:
                    registro["FECHA"] = datetime.strptime(crudo.strip(),
                                                          formato.formato_fecha).date()
                except ValueError:
                    registro["FECHA"] = None
            elif campo_ == "ASIEN":
                registro["ASIEN"] = int(_a_numero(crudo, formato))
            elif campo_ in ("EURODEBE", "EUROHABER", "IMPORTE"):
                registro[campo_] = round(_a_numero(crudo, formato), 2)
            elif campo_:
                registro[campo_] = crudo.strip()
            else:
                registro[columna.nombre] = crudo.strip()

        if formato.modo_importe == "importe-dh":
            importe = registro.pop("IMPORTE", 0.0)
            marca = str(registro.get(formato.columna_dh, "")).strip().upper()
            al_debe = marca == formato.marca_debe.upper()
            registro["EURODEBE"] = round(importe, 2) if al_debe else 0.0
            registro["EUROHABER"] = 0.0 if al_debe else round(importe, 2)
        yield registro


def escribir(ruta: str | Path, formato: FormatoCsv, registros: list[dict]) -> int:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.StringIO(newline="")
    escritor = csv.writer(buffer, delimiter=formato.delimitador,
                          quotechar=formato.comillas, quoting=csv.QUOTE_MINIMAL,
                          lineterminator=formato.salto)
    if formato.cabecera:
        escritor.writerow([c.nombre for c in formato.columnas])

    for registro in registros:
        fila = []
        for columna in formato.columnas:
            campo_ = columna.campo
            if campo_ == "IMPORTE":
                debe = float(registro.get("EURODEBE") or 0)
                haber = float(registro.get("EUROHABER") or 0)
                fila.append(_de_numero(debe or haber, formato))
                continue
            valor = registro.get(columna.clave, formato.constantes.get(columna.nombre, ""))
            if columna.nombre == formato.columna_dh and formato.modo_importe == "importe-dh":
                debe = float(registro.get("EURODEBE") or 0)
                fila.append(formato.marca_debe if debe else formato.marca_haber)
            elif campo_ == "FECHA":
                fila.append(valor.strftime(formato.formato_fecha)
                            if isinstance(valor, (date, datetime)) else str(valor or ""))
            elif campo_ in ("EURODEBE", "EUROHABER"):
                fila.append(_de_numero(valor or 0, formato))
            elif campo_ == "ASIEN":
                fila.append(str(int(valor or 0)))
            else:
                fila.append("" if valor is None else str(valor))
        escritor.writerow(fila)

    ruta.write_text(buffer.getvalue(), encoding=formato.codificacion)
    return len(registros)
