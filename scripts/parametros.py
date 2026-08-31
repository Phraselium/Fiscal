#!/usr/bin/env python3
"""Consulta los parametros fiscales y avisa de los que no son fiables.

Las skills NO memorizan cifras. Cuando necesites un tipo, un umbral o un limite,
consultalo aqui. Si el parametro esta marcado 'volatil' o 'sin_verificar', el
script lo dice y hay que contrastarlo en fuente oficial antes de usarlo en un
entregable.

    python3 scripts/parametros.py buscar iva.tipo
    python3 scripts/parametros.py ver retenciones.profesionales
    python3 scripts/parametros.py revisar          # lo que NO es fiable
    python3 scripts/parametros.py revisar --caducados
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

RUTA = Path(__file__).resolve().parent.parent / "datos" / "parametros.json"

SEMAFORO = {
    "estable": "OK  ",
    "verificado": "OK  ",
    "sin_verificar": "?   ",
    "volatil": "!!  ",
}


def cargar() -> dict:
    if not RUTA.exists():
        print(f"No existe {RUTA}", file=sys.stderr)
        raise SystemExit(2)
    return json.loads(RUTA.read_text(encoding="utf-8"))


def meses_desde(texto: str | None) -> int | None:
    if not texto:
        return None
    try:
        d = datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        return None
    hoy = date.today()
    return (hoy.year - d.year) * 12 + hoy.month - d.month


def formatear_valor(entrada: dict) -> str:
    valor = entrada.get("valor")
    if valor is None:
        return "SIN VALOR"
    unidad = entrada.get("unidad", "")
    if isinstance(valor, (list, dict)):
        return f"{json.dumps(valor, ensure_ascii=False)} {unidad}".strip()
    return f"{valor} {unidad}".strip()


def mostrar(clave: str, entrada: dict, detalle: bool = True) -> None:
    estado = entrada.get("estado", "sin_verificar")
    print(f"{SEMAFORO.get(estado, '    ')}{clave}")
    print(f"      valor:  {formatear_valor(entrada)}")
    print(f"      estado: {estado}")
    if not detalle:
        return
    for campo, etiqueta in (
        ("fuente", "fuente"), ("desde", "desde"), ("verificado_el", "verif."),
        ("url", "url"), ("nota", "nota"),
    ):
        if entrada.get(campo):
            texto = str(entrada[campo])
            if campo == "nota" and len(texto) > 76:
                lineas = []
                actual = ""
                for palabra in texto.split():
                    if len(actual) + len(palabra) > 76:
                        lineas.append(actual)
                        actual = palabra
                    else:
                        actual = f"{actual} {palabra}".strip()
                lineas.append(actual)
                print(f"      {etiqueta}:  {lineas[0]}")
                for l in lineas[1:]:
                    print(f"             {l}")
            else:
                print(f"      {etiqueta}:  {texto}")
    if estado == "volatil":
        print("      >>> NO USAR SIN VERIFICAR EN FUENTE OFICIAL <<<")
    elif estado == "sin_verificar":
        print("      >>> Contrastar antes de incluirlo en un entregable <<<")


def cmd_ver(datos: dict, args) -> int:
    entrada = datos.get(args.clave)
    if entrada is None:
        similares = [k for k in datos if not k.startswith("_") and args.clave.lower() in k.lower()]
        print(f"No existe el parametro '{args.clave}'.", file=sys.stderr)
        if similares:
            print("Quizas: " + ", ".join(similares[:10]), file=sys.stderr)
        return 1
    mostrar(args.clave, entrada)
    return 0


def cmd_buscar(datos: dict, args) -> int:
    termino = args.termino.lower()
    encontrados = {
        k: v for k, v in datos.items()
        if not k.startswith("_") and (
            termino in k.lower()
            or termino in str(v.get("fuente", "")).lower()
            or termino in str(v.get("nota", "")).lower()
        )
    }
    if not encontrados:
        print(f"Sin coincidencias para '{args.termino}'.")
        print("Prefijos: iva, irpf, is, retenciones, informativas, intrastat, lgt,")
        print("facturacion, verifactu, patrimonio, isd, reta, dietas, iae")
        return 1
    print(f"{len(encontrados)} parametros\n")
    for clave, entrada in sorted(encontrados.items()):
        mostrar(clave, entrada, detalle=args.detalle)
        print()
    return 0


def cmd_revisar(datos: dict, args) -> int:
    meta = datos.get("_meta", {})
    caducidad = meta.get("meses_caducidad_por_defecto", 12)
    volatiles, sin_verificar, caducados = [], [], []

    for clave, entrada in datos.items():
        if clave.startswith("_"):
            continue
        estado = entrada.get("estado")
        if estado == "volatil":
            volatiles.append(clave)
        elif estado == "sin_verificar":
            sin_verificar.append(clave)
        elif estado == "verificado":
            antiguedad = meses_desde(entrada.get("verificado_el"))
            if antiguedad is not None and antiguedad >= caducidad:
                caducados.append((clave, antiguedad))

    if args.caducados:
        if not caducados:
            print(f"Ningun parametro verificado supera los {caducidad} meses.")
            return 0
        print(f"{len(caducados)} parametros verificados hace mas de {caducidad} meses:\n")
        for clave, meses in sorted(caducados, key=lambda x: -x[1]):
            print(f"  {meses:3} meses  {clave}")
        return 1

    print(f"Revision de {RUTA.name} — revisado el {meta.get('revisado_el', '?')}")
    print(f"Ejercicio de referencia: {meta.get('ejercicio_referencia', '?')}\n")

    print(f"!!  VOLATILES ({len(volatiles)}) — cambian cada ejercicio, verificar SIEMPRE:")
    for clave in sorted(volatiles):
        nota = datos[clave].get("nota", "")
        print(f"      {clave:<44} {nota[:60]}")

    print(f"\n?   SIN VERIFICAR ({len(sin_verificar)}) — del conocimiento del modelo, contrastar:")
    for clave in sorted(sin_verificar):
        print(f"      {clave:<44} {formatear_valor(datos[clave])[:44]}")

    if caducados:
        print(f"\n    CADUCADOS ({len(caducados)}) — verificados hace mas de {caducidad} meses:")
        for clave, meses in sorted(caducados, key=lambda x: -x[1]):
            print(f"      {clave:<44} hace {meses} meses")

    fiables = sum(1 for k, v in datos.items() if not k.startswith("_") and v.get("estado") in ("estable", "verificado"))
    total = sum(1 for k in datos if not k.startswith("_"))
    print(f"\n  Fiables sin reverificar: {fiables}/{total}")
    print("  Usa /verificar normativa para contrastar los volatiles y sin verificar.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)
    p = sub.add_parser("ver"); p.add_argument("clave")
    p = sub.add_parser("buscar"); p.add_argument("termino"); p.add_argument("--detalle", action="store_true", default=True)
    p = sub.add_parser("revisar"); p.add_argument("--caducados", action="store_true")
    args = ap.parse_args()
    datos = cargar()
    return {"ver": cmd_ver, "buscar": cmd_buscar, "revisar": cmd_revisar}[args.comando](datos, args)


if __name__ == "__main__":
    raise SystemExit(main())
