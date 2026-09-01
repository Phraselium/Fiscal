#!/usr/bin/env python3
"""Genera el documento de importacion a partir de los movimientos ya clasificados.

Dos formatos, un solo criterio: **el formato sale del fichero muestra**.

    muestra .dbf  →  XDIARIO.DBF   para ContaPlus
    muestra .csv  →  XDIARIO.csv   para Sage 50 y similares

REGLA DE ORO: el formato NO se codifica aqui. Se lee del fichero muestra de
importacion del cliente y se replica. El XDIARIO ronda los 98 campos y cambia
entre versiones de ContaPlus; el CSV cambia de columnas, delimitador y formato
de fecha entre instalaciones de Sage. Cualquier formato escrito a mano acabaria
produciendo un fichero que el programa rechaza o, peor, lee mal.

Como se arma cada asiento
-------------------------
· Dos apuntes por asiento, consecutivos: primero el del debe, luego el del haber.
· Ningun importe negativo. El signo del extracto se traduce en debe o haber:
      cargo (importe < 0) → contrapartida al DEBE,  banco al HABER
      abono (importe > 0) → banco al DEBE,          contrapartida al HABER
· CONTRA de cada apunte es la subcuenta del otro apunte.
· Numeracion correlativa sin huecos desde el numero inicial, en orden cronologico.
· PTADEBE y PTAHABER a cero: los importes viajan en EURODEBE / EUROHABER.
· MONEDAUSO = '2' (euro), NIC = 'E'.
· Concepto sin acentos, en mayusculas, maximo 25 caracteres.
· Los movimientos de importe cero no generan asiento; se listan aparte.

Uso
---
    python3 scripts/bancos/generar_xdiario.py \\
        --clasificado clasificado.json --muestra MUESTRA.DBF \\
        --salida salidas/XDIARIO.DBF --asiento-inicial 1

    python3 scripts/bancos/generar_xdiario.py \\
        --clasificado clasificado.json --muestra MUESTRA_SAGE.csv \\
        --salida salidas/XDIARIO.csv --asiento-inicial 1
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_documento as ld  # noqa: E402

CAMPOS_QUE_SE_RELLENAN = (
    "ASIEN", "FECHA", "SUBCTA", "CONTRA", "CONCEPTO",
    "EURODEBE", "EUROHABER", "MONEDAUSO", "NIC",
)


def sin_acentos(texto) -> str:
    if texto is None:
        return ""
    t = unicodedata.normalize("NFD", str(texto).upper())
    return "".join(c for c in t if unicodedata.category(c) != "Mn").strip()


def ajustar_subcuenta(cuenta: str, longitud: int) -> str:
    """La longitud la manda el plan del cliente, no el fichero muestra."""
    cuenta = str(cuenta).strip()
    if not longitud or len(cuenta) == longitud:
        return cuenta
    if len(cuenta) < longitud:
        return cuenta.ljust(longitud, "0")
    return cuenta[:longitud]


def apunte(formato, asiento: int, fecha, subcta: str, contra: str,
           concepto: str, debe: float, haber: float) -> dict:
    """Un registro completo: los campos que se rellenan y el resto a su valor neutro.

    Vale para los dos formatos: la plantilla la da la muestra, no este fichero.
    """
    registro = ld.plantilla(formato)
    registro.update({
        "ASIEN": asiento,
        "FECHA": fecha,
        "SUBCTA": subcta,
        "CONTRA": contra,
        "CONCEPTO": sin_acentos(concepto)[:25],
        "EURODEBE": round(debe, 2),
        "EUROHABER": round(haber, 2),
        "PTADEBE": 0,
        "PTAHABER": 0,
        "MONEDAUSO": "2",
        "NIC": "E",
    })
    return {k: v for k, v in registro.items() if k in formato.nombres}


def construir_asientos(clasificados: list[dict], formato,
                       asiento_inicial: int = 1,
                       longitud_subcuenta: int = 0) -> tuple[list[dict], list[dict]]:
    """Devuelve (registros del documento, movimientos descartados por importe cero)."""
    vivos, ceros = [], []
    for c in clasificados:
        if c.get("contabilizado_en_otro"):
            continue
        if abs(float(c.get("importe", 0))) < 0.005:
            ceros.append(c)
            continue
        vivos.append(c)

    def clave(c):
        f = c["fecha"]
        return (datetime.fromisoformat(f).date() if isinstance(f, str) else f,
                c.get("banco", ""), c.get("fila", 0))

    vivos.sort(key=clave)

    registros: list[dict] = []
    numero = asiento_inicial
    for c in vivos:
        fecha = c["fecha"]
        if isinstance(fecha, str):
            fecha = datetime.fromisoformat(fecha).date()
        banco = ajustar_subcuenta(c["subcuenta_banco"], longitud_subcuenta)
        contra = ajustar_subcuenta(c["contrapartida"], longitud_subcuenta)
        importe = round(abs(float(c["importe"])), 2)
        concepto = c.get("concepto", "")

        if float(c["importe"]) < 0:      # cargo: sale dinero del banco
            debe_cta, haber_cta = contra, banco
        else:                            # abono: entra dinero en el banco
            debe_cta, haber_cta = banco, contra

        registros.append(apunte(formato, numero, fecha, debe_cta, haber_cta,
                                concepto, importe, 0))
        registros.append(apunte(formato, numero, fecha, haber_cta, debe_cta,
                                concepto, 0, importe))
        numero += 1

    return registros, ceros


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clasificado", required=True, type=Path)
    ap.add_argument("--muestra", required=True, type=Path,
                    help="Fichero muestra de importacion (.dbf o .csv): de aquí sale "
                         "el formato")
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--asiento-inicial", type=int, default=1)
    ap.add_argument("--longitud-subcuenta", type=int, default=0,
                    help="La del plan del cliente; 0 = dejar como viene")
    args = ap.parse_args()

    for ruta in (args.clasificado, args.muestra):
        if not ruta.exists():
            print(f"No existe {ruta}", file=sys.stderr)
            return 2

    try:
        formato = ld.leer_formato(args.muestra)
    except Exception as exc:
        print(f"No se ha podido leer el formato de {args.muestra}: {exc}", file=sys.stderr)
        return 2

    faltan = ld.campos_que_faltan(formato, CAMPOS_QUE_SE_RELLENAN)
    if faltan:
        print(f"El fichero muestra no tiene los campos {', '.join(faltan)}.",
              file=sys.stderr)
        print(f"Formato detectado: {ld.nombre_formato(args.muestra)}", file=sys.stderr)
        print(ld.descripcion(formato, args.muestra), file=sys.stderr)
        print("\nNo se genera nada: sin esos campos el fichero no se puede importar.",
              file=sys.stderr)
        return 2

    clasificados = json.loads(args.clasificado.read_text(encoding="utf-8"))
    registros, ceros = construir_asientos(
        clasificados, formato, args.asiento_inicial, args.longitud_subcuenta)

    if not registros:
        print("No hay ningún movimiento que contabilizar", file=sys.stderr)
        return 1

    if ld.es_csv(args.muestra) != ld.es_csv(args.salida):
        print(f"La muestra es {ld.nombre_formato(args.muestra)} y la salida "
              f"{ld.nombre_formato(args.salida)}: no coinciden.", file=sys.stderr)
        print(f"Usa --salida {ld.salida_por_defecto(args.muestra)}", file=sys.stderr)
        return 2

    escritos = ld.escribir(args.salida, formato, registros)
    asientos = escritos // 2
    total = sum(r["EURODEBE"] for r in registros)

    print(f"Fichero generado: {args.salida}")
    print(f"  Formato:     {ld.nombre_formato(args.muestra)}, tomado del fichero muestra")
    for linea in ld.descripcion(formato, args.muestra).splitlines():
        print(f"    {linea}")
    print(f"  Asientos:    {asientos}  ({escritos} apuntes)")
    print(f"  Numeración:  {args.asiento_inicial} a {args.asiento_inicial + asientos - 1}")
    print(f"  Total debe:  {total:,.2f} €".replace(",", "@").replace(".", ",").replace("@", "."))
    if ceros:
        print(f"\n  {len(ceros)} movimientos de importe cero, sin asiento:")
        for c in ceros[:10]:
            print(f"      {c['fecha']}  {c.get('texto', '')[:58]}")

    print("\nSIGUIENTE PASO: verifica el fichero antes de entregarlo:")
    # Sin f-string: la ruta lleva llaves y el empaquetador de claude.ai tiene que
    # poder traducirla a ruta relativa.
    print('  python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/verificar_xdiario.py \\')
    print("      " + str(args.salida) + " --muestra " + str(args.muestra))
    print("\nEl fichero está pendiente de revisar e importar. No está contabilizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
