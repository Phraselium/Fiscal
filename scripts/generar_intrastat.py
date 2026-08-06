#!/usr/bin/env python3
"""Genera el fichero de la declaracion Intrastat listo para subir al portal de Aduanas.

Intrastat es la estadistica de intercambios de bienes entre Estados miembros de la
UE. Se declara por flujos independientes: INTRODUCCION (llegadas, flujo A) y
EXPEDICION (salidas, flujo D). Un mismo obligado puede tener que declarar uno solo
o los dos.

Formatos de salida
------------------
csv   Fichero CSV con la estructura de columnas del portal Intrastat de la AEAT.
      Es el formato habitual de carga.
json  Volcado estructurado para revision interna o para el software del despacho.

Uso
---
    python3 scripts/generar_intrastat.py \
        --flujo expedicion \
        --periodo 2026-07 \
        --declarante datos/declarante_intrastat.json \
        --lineas datos/movimientos.csv \
        --salida salidas/intrastat-expedicion-2026-07.csv

VERIFICACION OBLIGATORIA: el orden y el nombre de las columnas del fichero de
carga los fija el Departamento de Aduanas e II.EE. y se publican en la guia
Intrastat del ejercicio. Contrastalos antes del primer envio; el portal valida el
fichero al subirlo y devuelve los errores linea a linea.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.validaciones import validar_codigo_nc8, validar_nif, validar_nif_iva  # noqa: E402

FLUJOS = {"introduccion": "A", "expedicion": "D"}

# Columnas del fichero de carga. Contrastar con la guia Intrastat vigente.
COLUMNAS = [
    "numero_linea",
    "estado_miembro",
    "pais_origen",
    "provincia",
    "condiciones_entrega",
    "naturaleza_transaccion",
    "modalidad_transporte",
    "codigo_nc8",
    "masa_neta",
    "unidades_suplementarias",
    "importe_facturado",
    "importe_estadistico",
    "regimen_estadistico",
    "nif_iva_contraparte",
    "puerto_aeropuerto",
]

OBLIGATORIOS = [
    "estado_miembro",
    "naturaleza_transaccion",
    "codigo_nc8",
    "masa_neta",
    "importe_facturado",
]

# Codigos de pais de los Estados miembros (ISO 3166-1 alfa-2; XI = Irlanda del Norte).
ESTADOS_MIEMBROS = {
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GR",
    "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO",
    "SE", "SI", "SK", "XI",
}


def normalizar_importe(valor) -> Decimal:
    if valor in (None, ""):
        return Decimal("0")
    texto = str(valor).replace("€", "").strip()
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")
    return Decimal(texto or "0")


def redondear(valor: Decimal, decimales: str = "1") -> str:
    return str(valor.quantize(Decimal(decimales), rounding=ROUND_HALF_UP))


def leer_lineas(ruta: Path) -> list[dict]:
    if ruta.suffix.lower() == ".json":
        return json.loads(ruta.read_text(encoding="utf-8"))
    with ruta.open(encoding="utf-8-sig", newline="") as fichero:
        muestra = fichero.read(4096)
        fichero.seek(0)
        try:
            dialecto = csv.Sniffer().sniff(muestra, delimiters=";,\t")
        except csv.Error:
            dialecto = csv.excel
            dialecto.delimiter = ";"
        return [dict(fila) for fila in csv.DictReader(fichero, dialect=dialecto)]


def validar_linea(indice: int, fila: dict, flujo: str) -> list[str]:
    errores = []

    for campo in OBLIGATORIOS:
        if not str(fila.get(campo, "")).strip():
            errores.append(f"Linea {indice}: falta el campo obligatorio '{campo}'")

    estado = str(fila.get("estado_miembro", "")).strip().upper()
    if estado and estado not in ESTADOS_MIEMBROS:
        errores.append(f"Linea {indice}: '{estado}' no es un Estado miembro de la UE")
    if estado == "ES":
        errores.append(f"Linea {indice}: el Estado miembro no puede ser ES en Intrastat")

    codigo = str(fila.get("codigo_nc8", "")).strip()
    if codigo:
        ok, motivo = validar_codigo_nc8(codigo)
        if not ok:
            errores.append(f"Linea {indice}: codigo NC8 '{codigo}' — {motivo}")

    naturaleza = re.sub(r"\D", "", str(fila.get("naturaleza_transaccion", "")))
    if naturaleza and len(naturaleza) not in (1, 2):
        errores.append(
            f"Linea {indice}: naturaleza de la transaccion '{naturaleza}' debe tener 1 o 2 digitos"
        )

    masa = normalizar_importe(fila.get("masa_neta"))
    if masa < 0:
        errores.append(f"Linea {indice}: la masa neta no puede ser negativa")
    if masa == 0 and not str(fila.get("unidades_suplementarias", "")).strip():
        errores.append(
            f"Linea {indice}: masa neta a cero sin unidades suplementarias; "
            "revisa si la partida exige unidad suplementaria en el arancel"
        )

    if normalizar_importe(fila.get("importe_facturado")) <= 0:
        errores.append(f"Linea {indice}: el importe facturado debe ser mayor que cero")

    # Desde 2022 el NIF-IVA de la contraparte y el pais de origen de la mercancia
    # son obligatorios en el flujo de expedicion.
    if flujo == "expedicion":
        nif_iva = str(fila.get("nif_iva_contraparte", "")).strip()
        if not nif_iva:
            errores.append(
                f"Linea {indice}: falta el NIF-IVA del cliente (obligatorio en expedicion)"
            )
        else:
            ok, motivo = validar_nif_iva(nif_iva)
            if not ok:
                errores.append(f"Linea {indice}: NIF-IVA '{nif_iva}' — {motivo}")
        if not str(fila.get("pais_origen", "")).strip():
            errores.append(
                f"Linea {indice}: falta el pais de origen de la mercancia "
                "(obligatorio en expedicion desde 2022)"
            )

    return errores


def main() -> int:
    analizador = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    analizador.add_argument("--flujo", required=True, choices=sorted(FLUJOS))
    analizador.add_argument("--periodo", required=True, help="Periodo de referencia AAAA-MM")
    analizador.add_argument("--declarante", required=True, type=Path)
    analizador.add_argument("--lineas", required=True, type=Path)
    analizador.add_argument("--salida", required=True, type=Path)
    analizador.add_argument("--formato", choices=("csv", "json"), default="csv")
    analizador.add_argument("--separador", default=";")
    analizador.add_argument(
        "--umbral",
        type=float,
        default=400000.0,
        help="Umbral de exencion anual por flujo, solo informativo (verificar el vigente)",
    )
    analizador.add_argument("--forzar", action="store_true", help="Genera aunque haya errores")
    args = analizador.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}", args.periodo):
        print("ERROR: el periodo debe tener el formato AAAA-MM", file=sys.stderr)
        return 2
    mes = int(args.periodo.split("-")[1])
    if not 1 <= mes <= 12:
        print("ERROR: mes fuera de rango en el periodo", file=sys.stderr)
        return 2

    declarante = json.loads(args.declarante.read_text(encoding="utf-8"))
    valido, motivo = validar_nif(declarante.get("nif", ""))
    if not valido:
        print(f"ERROR: NIF del declarante invalido — {motivo}", file=sys.stderr)
        return 2

    filas = leer_lineas(args.lineas)
    if not filas:
        print("ERROR: no hay lineas que declarar", file=sys.stderr)
        return 2

    errores: list[str] = []
    salida: list[dict] = []
    total_facturado = Decimal("0")
    total_estadistico = Decimal("0")

    for indice, fila in enumerate(filas, start=1):
        errores.extend(validar_linea(indice, fila, args.flujo))

        facturado = normalizar_importe(fila.get("importe_facturado"))
        estadistico = normalizar_importe(fila.get("importe_estadistico")) or facturado
        total_facturado += facturado
        total_estadistico += estadistico

        salida.append(
            {
                "numero_linea": fila.get("numero_linea") or indice,
                "estado_miembro": str(fila.get("estado_miembro", "")).strip().upper(),
                "pais_origen": str(fila.get("pais_origen", "")).strip().upper(),
                "provincia": re.sub(r"\D", "", str(fila.get("provincia", ""))).zfill(2)
                if str(fila.get("provincia", "")).strip()
                else "",
                "condiciones_entrega": str(fila.get("condiciones_entrega", "")).strip().upper(),
                "naturaleza_transaccion": re.sub(
                    r"\D", "", str(fila.get("naturaleza_transaccion", ""))
                ),
                "modalidad_transporte": re.sub(
                    r"\D", "", str(fila.get("modalidad_transporte", ""))
                ),
                "codigo_nc8": re.sub(r"\D", "", str(fila.get("codigo_nc8", ""))),
                "masa_neta": redondear(normalizar_importe(fila.get("masa_neta")), "0.001"),
                "unidades_suplementarias": redondear(
                    normalizar_importe(fila.get("unidades_suplementarias")), "1"
                )
                if str(fila.get("unidades_suplementarias", "")).strip()
                else "",
                "importe_facturado": redondear(facturado, "1"),
                "importe_estadistico": redondear(estadistico, "1"),
                "regimen_estadistico": re.sub(
                    r"\D", "", str(fila.get("regimen_estadistico", ""))
                ),
                "nif_iva_contraparte": re.sub(
                    r"[^0-9A-Za-z]", "", str(fila.get("nif_iva_contraparte", ""))
                ).upper(),
                "puerto_aeropuerto": str(fila.get("puerto_aeropuerto", "")).strip().upper(),
            }
        )

    if errores:
        print(f"Se han detectado {len(errores)} incidencias:", file=sys.stderr)
        for error in errores[:60]:
            print(f"  - {error}", file=sys.stderr)
        if len(errores) > 60:
            print(f"  ... y {len(errores) - 60} mas", file=sys.stderr)
        if not args.forzar:
            print("\nGeneracion abortada. Corrige las lineas o repite con --forzar.", file=sys.stderr)
            return 1

    args.salida.parent.mkdir(parents=True, exist_ok=True)

    if args.formato == "json":
        args.salida.write_text(
            json.dumps(
                {
                    "declarante": declarante,
                    "periodo": args.periodo,
                    "flujo": args.flujo,
                    "codigo_flujo": FLUJOS[args.flujo],
                    "lineas": salida,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    else:
        with args.salida.open("w", encoding="utf-8-sig", newline="") as fichero:
            escritor = csv.DictWriter(
                fichero, fieldnames=COLUMNAS, delimiter=args.separador, extrasaction="ignore"
            )
            escritor.writeheader()
            escritor.writerows(salida)

    print(f"Fichero generado: {args.salida}")
    print(f"  Declarante:  {declarante.get('nif')} — {declarante.get('nombre', '')}")
    print(f"  Flujo:       {args.flujo.upper()} ({FLUJOS[args.flujo]})")
    print(f"  Periodo:     {args.periodo}")
    print(f"  Lineas:      {len(salida)}")
    print(f"  Facturado:   {total_facturado:,.2f} EUR".replace(",", "@").replace(".", ",").replace("@", "."))
    print(f"  Estadistico: {total_estadistico:,.2f} EUR".replace(",", "@").replace(".", ",").replace("@", "."))
    if total_facturado < Decimal(str(args.umbral)):
        umbral = f"{args.umbral:,.0f}".replace(",", ".")
        print(
            f"\n  Nota: el importe de este periodo no alcanza el umbral anual de "
            f"{umbral} EUR por flujo. Comprueba el acumulado del ANO, no el del mes,"
        )
        print("  para decidir si existe obligacion, y verifica el umbral vigente.")
    print("\nSIGUIENTE PASO: sube el fichero en el portal Intrastat de la sede electronica")
    print("de la AEAT (Aduanas e II.EE.) y revisa los errores que devuelva el validador.")
    print("Plazo: dias 1 a 12 del mes siguiente al periodo de referencia (verificar calendario).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
