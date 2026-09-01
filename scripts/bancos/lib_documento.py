#!/usr/bin/env python3
"""Despachador de formato del documento de importacion.

El cliente manda cada ano su fichero muestra. Si es un DBF, se genera un
XDIARIO.DBF para ContaPlus; si es un CSV, se genera un CSV con exactamente sus
columnas, su delimitador y sus formatos, que es lo que espera Sage 50.

En los dos casos la regla es la misma y no se negocia: **el formato sale del
fichero muestra**, nunca de una especificacion escrita a mano aqui.

El resto del flujo trabaja siempre con registros canonicos -ASIEN, FECHA,
SUBCTA, CONTRA, CONCEPTO, EURODEBE, EUROHABER- asi que ni generar ni verificar
necesitan saber en que formato van a acabar.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_csv  # noqa: E402
import lib_dbf  # noqa: E402

EXTENSIONES_CSV = {".csv", ".txt", ".tsv"}


def es_csv(ruta: str | Path) -> bool:
    return Path(ruta).suffix.lower() in EXTENSIONES_CSV


def nombre_formato(ruta: str | Path) -> str:
    return "CSV (Sage 50 y similares)" if es_csv(ruta) else "DBF (XDIARIO de ContaPlus)"


def leer_formato(ruta: str | Path):
    """FormatoCsv o Estructura, segun el fichero. Los dos ofrecen la misma interfaz."""
    return lib_csv.leer_formato(ruta) if es_csv(ruta) else lib_dbf.leer_estructura(ruta)


def leer(ruta: str | Path) -> Iterator[dict[str, Any]]:
    return lib_csv.leer(ruta) if es_csv(ruta) else lib_dbf.leer(ruta)


def escribir(ruta: str | Path, formato, registros: list[dict]) -> int:
    return (lib_csv.escribir(ruta, formato, registros) if es_csv(ruta)
            else lib_dbf.escribir(ruta, formato, registros))


def plantilla(formato) -> dict[str, Any]:
    """Registro vacio con todas las columnas o campos del formato."""
    if hasattr(formato, "plantilla"):
        return formato.plantilla()
    return {c.nombre: lib_dbf.valor_por_defecto(c) for c in formato.campos}


def campos_que_faltan(formato, obligatorios) -> list[str]:
    """Campos obligatorios que la muestra no tiene. Si hay alguno, no se genera."""
    if isinstance(formato, lib_csv.FormatoCsv):
        return lib_csv.campos_que_faltan(formato)
    return [c for c in obligatorios if not formato.campo(c)]


def descripcion(formato, ruta: str | Path) -> str:
    """Que se ha deducido de la muestra. Hay que ensenarselo al usuario."""
    if isinstance(formato, lib_csv.FormatoCsv):
        return formato.descripcion()
    return (f"{len(formato.campos)} campos, {formato.longitud_registro} bytes por "
            f"registro, version {formato.version:#04x}")


def salida_por_defecto(muestra: str | Path, carpeta: str | Path = "salidas") -> Path:
    """El fichero a generar se llama como manda el formato de la muestra."""
    return Path(carpeta) / ("XDIARIO.csv" if es_csv(muestra) else "XDIARIO.DBF")
