#!/usr/bin/env python3
"""Genera el fichero de una declaracion informativa en el diseno de registro de la AEAT.

El diseno se lee de `disenos/<modelo>.json`; este script no contiene logica de
ningun modelo concreto.

Uso
---
    python3 scripts/generar_informativa.py \
        --modelo 190 \
        --ejercicio 2025 \
        --declarante datos/declarante.json \
        --detalle datos/perceptores.csv \
        --salida salidas/190-2025.txt

El fichero de detalle puede ser CSV (con cabecera cuyos nombres coincidan con los
campos del diseno) o JSON (lista de objetos). Los importes se expresan en euros,
admitiendo tanto `1234.56` como `1.234,56`.

Despues de generar, valida SIEMPRE el fichero en el formulario del modelo de la
sede electronica de la AEAT ("Importar fichero"). Ese validador es la
comprobacion definitiva.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.registro import (  # noqa: E402
    Diseno,
    ErrorDato,
    ErrorDiseno,
    a_centimos,
    construir_registro,
    escribir_fichero,
    validar_fichero,
)
from lib.validaciones import validar_nif  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def leer_detalle(ruta: Path) -> list[dict]:
    if ruta.suffix.lower() == ".json":
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        if not isinstance(datos, list):
            raise SystemExit("El JSON de detalle debe ser una lista de objetos")
        return datos
    with ruta.open(encoding="utf-8-sig", newline="") as fichero:
        muestra = fichero.read(4096)
        fichero.seek(0)
        try:
            dialecto = csv.Sniffer().sniff(muestra, delimiters=";,\t")
        except csv.Error:
            dialecto = csv.excel
            dialecto.delimiter = ";"
        return [dict(fila) for fila in csv.DictReader(fichero, dialect=dialecto)]


def comprobar_nifs(filas: list[dict], campos: list[str]) -> list[str]:
    incidencias = []
    for indice, fila in enumerate(filas, start=1):
        for campo in campos:
            valor = (fila.get(campo) or "").strip()
            if not valor:
                continue
            valido, motivo = validar_nif(valor)
            if not valido:
                incidencias.append(f"Fila {indice}, {campo}='{valor}': {motivo}")
    return incidencias


def main() -> int:
    analizador = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    analizador.add_argument("--modelo", required=True, help="Codigo del modelo, p. ej. 190")
    analizador.add_argument("--ejercicio", required=True, help="Ejercicio de la declaracion")
    analizador.add_argument("--declarante", required=True, type=Path, help="JSON con los datos del declarante")
    analizador.add_argument("--detalle", required=True, type=Path, help="CSV o JSON con los registros de detalle")
    analizador.add_argument("--salida", required=True, type=Path, help="Ruta del fichero a generar")
    analizador.add_argument("--diseno", type=Path, help="Diseno alternativo (por defecto disenos/<modelo>.json)")
    analizador.add_argument("--complementaria", action="store_true")
    analizador.add_argument("--sustitutiva", action="store_true")
    analizador.add_argument("--identificativo-anterior", default="", help="Numero identificativo de la declaracion anterior")
    analizador.add_argument("--periodo", default="", help="Periodo, en los modelos que lo exigen (01-12, 1T-4T, 0A)")
    analizador.add_argument("--campo-importe-total", default="", help="Campo del detalle que se suma en el total de percepciones")
    analizador.add_argument("--campo-retencion-total", default="", help="Campo del detalle que se suma en el total de retenciones")
    analizador.add_argument("--acepto-diseno-no-verificado", action="store_true")
    analizador.add_argument("--sin-validar-nif", action="store_true")
    args = analizador.parse_args()

    ruta_diseno = args.diseno or RAIZ / "disenos" / f"{args.modelo}.json"
    if not ruta_diseno.exists():
        print(f"ERROR: no existe el diseno {ruta_diseno}", file=sys.stderr)
        print("       Crealo a partir del anexo de la orden del modelo. Ver disenos/README.md", file=sys.stderr)
        return 2

    try:
        diseno = Diseno.cargar(ruta_diseno)
    except (ErrorDiseno, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR en el diseno: {exc}", file=sys.stderr)
        return 2

    bruto = json.loads(ruta_diseno.read_text(encoding="utf-8"))
    if not diseno.verificado:
        print("=" * 78, file=sys.stderr)
        print(f"AVISO — diseno del modelo {diseno.modelo} NO VERIFICADO", file=sys.stderr)
        print(bruto.get("aviso", ""), file=sys.stderr)
        for pendiente in bruto.get("pendiente_verificacion", []):
            print(f"  - {pendiente}", file=sys.stderr)
        print(f"Fuente a contrastar: {diseno.fuente}", file=sys.stderr)
        print("=" * 78, file=sys.stderr)
        if not args.acepto_diseno_no_verificado:
            print("Generacion abortada. Verifica el diseno o repite con --acepto-diseno-no-verificado.", file=sys.stderr)
            return 3

    declarante = json.loads(args.declarante.read_text(encoding="utf-8"))
    declarante.setdefault("ejercicio", args.ejercicio)
    declarante["declaracion_complementaria"] = "C" if args.complementaria else ""
    declarante["declaracion_sustitutiva"] = "S" if args.sustitutiva else ""
    declarante["numero_identificativo_anterior"] = args.identificativo_anterior
    if args.periodo:
        declarante["periodo"] = args.periodo.upper()

    valido, motivo = validar_nif(declarante.get("nif_declarante", ""))
    if not valido:
        print(f"ERROR: NIF del declarante invalido — {motivo}", file=sys.stderr)
        return 2

    filas = leer_detalle(args.detalle)
    if not filas:
        print("ERROR: el fichero de detalle no contiene registros", file=sys.stderr)
        return 2

    campos_detalle = {c.nombre for c in diseno.registros["2"]}
    campos_nif = [c for c in ("nif_perceptor", "nif_declarado") if c in campos_detalle]
    if campos_nif and not args.sin_validar_nif:
        incidencias = comprobar_nifs(filas, campos_nif)
        if incidencias:
            print("ERROR: NIF invalidos en el detalle:", file=sys.stderr)
            for incidencia in incidencias[:40]:
                print(f"  - {incidencia}", file=sys.stderr)
            if len(incidencias) > 40:
                print(f"  ... y {len(incidencias) - 40} mas", file=sys.stderr)
            print("Corrigelos o repite con --sin-validar-nif si son NIF extranjeros.", file=sys.stderr)
            return 2

    # Totales del registro de cabecera.
    campo_importe = args.campo_importe_total or next(
        (n for n in ("percepcion_integra", "importe_anual", "base_imponible") if n in campos_detalle), ""
    )
    campo_retencion = args.campo_retencion_total or (
        "retenciones_practicadas" if "retenciones_practicadas" in campos_detalle else ""
    )

    total_importe = sum(a_centimos(f.get(campo_importe)) for f in filas) if campo_importe else 0
    total_retencion = sum(a_centimos(f.get(campo_retencion)) for f in filas) if campo_retencion else 0

    for nombre, valor in (
        ("numero_total_percepciones", len(filas)),
        ("numero_total_perceptores", len(filas)),
        ("numero_total_personas", len(filas)),
        ("numero_total_operadores", len(filas)),
    ):
        declarante.setdefault(nombre, valor)
    for nombre, valor in (
        ("importe_total_percepciones", total_importe / 100),
        ("importe_total_operaciones", total_importe / 100),
        ("importe_total_retenciones", total_retencion / 100),
    ):
        declarante.setdefault(nombre, valor)

    try:
        lineas = [construir_registro(diseno, "1", declarante)]
        for indice, fila in enumerate(filas, start=1):
            contexto = dict(declarante)
            contexto.update({k: v for k, v in fila.items() if v is not None})
            contexto["ejercicio"] = args.ejercicio
            contexto["nif_declarante"] = declarante["nif_declarante"]
            try:
                lineas.append(construir_registro(diseno, "2", contexto))
            except ErrorDato as exc:
                print(f"ERROR en la fila {indice} del detalle: {exc}", file=sys.stderr)
                return 2
    except (ErrorDato, ErrorDiseno) as exc:
        print(f"ERROR generando el fichero: {exc}", file=sys.stderr)
        return 2

    destino = escribir_fichero(args.salida, lineas)

    incidencias = validar_fichero(destino, diseno.longitud)
    print(f"Fichero generado: {destino}")
    print(f"  Modelo:      {diseno.modelo}")
    print(f"  Ejercicio:   {args.ejercicio}")
    print(f"  Registros:   1 cabecera + {len(filas)} de detalle")
    print(f"  Total base:  {total_importe / 100:,.2f} EUR".replace(",", "@").replace(".", ",").replace("@", "."))
    if campo_retencion:
        print(f"  Total reten: {total_retencion / 100:,.2f} EUR".replace(",", "@").replace(".", ",").replace("@", "."))
    if incidencias:
        print("\nINCIDENCIAS DE VALIDACION:")
        for incidencia in incidencias:
            print(f"  - {incidencia}")
        return 1
    print("\nValidacion estructural: correcta.")
    print("SIGUIENTE PASO: importa el fichero en el formulario del modelo en la sede")
    print("electronica de la AEAT y revisa el resultado antes de presentar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
