#!/usr/bin/env python3
"""Valida la estructura de un fichero de declaracion informativa ya generado.

Comprueba codificacion, longitud de registro, separadores, tipos de registro y,
si se indica el modelo, descompone el fichero campo a campo segun el diseno para
que puedas revisarlo antes de subirlo a la sede.

Uso
---
    python3 scripts/validar_fichero.py salidas/190-2025.txt
    python3 scripts/validar_fichero.py salidas/190-2025.txt --modelo 190 --detallar 3
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.registro import CODIFICACION, Diseno, validar_fichero  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def descomponer(diseno: Diseno, linea: str) -> list[tuple[str, str]]:
    tipo = linea[:1]
    campos = sorted(diseno.registros.get(tipo, []), key=lambda c: c.desde)
    return [(c.nombre, linea[c.desde - 1 : c.hasta]) for c in campos]


def main() -> int:
    analizador = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    analizador.add_argument("fichero", type=Path)
    analizador.add_argument("--modelo", help="Codigo del modelo para descomponer los campos")
    analizador.add_argument("--longitud", type=int, default=250)
    analizador.add_argument("--detallar", type=int, default=0, help="Numero de registros a descomponer")
    args = analizador.parse_args()

    if not args.fichero.exists():
        print(f"ERROR: no existe {args.fichero}", file=sys.stderr)
        return 2

    incidencias = validar_fichero(args.fichero, args.longitud)
    texto = args.fichero.read_bytes().decode(CODIFICACION, errors="replace")
    lineas = [l for l in texto.replace("\r\n", "\n").split("\n") if l]

    print(f"Fichero:   {args.fichero}")
    print(f"Registros: {len(lineas)}")
    print(f"Tamano:    {args.fichero.stat().st_size} bytes")

    if incidencias:
        print(f"\nINCIDENCIAS ({len(incidencias)}):")
        for incidencia in incidencias:
            print(f"  - {incidencia}")
    else:
        print("\nValidacion estructural: correcta.")

    if args.modelo and args.detallar:
        ruta = RAIZ / "disenos" / f"{args.modelo}.json"
        if not ruta.exists():
            print(f"\nNo hay diseno para el modelo {args.modelo}", file=sys.stderr)
        else:
            diseno = Diseno.cargar(ruta)
            for numero, linea in enumerate(lineas[: args.detallar], start=1):
                print(f"\n--- Registro {numero} (tipo {linea[:1]}) ---")
                for nombre, valor in descomponer(diseno, linea):
                    print(f"  {nombre:38} |{valor}|")

    print("\nRecuerda: la validacion definitiva la hace el formulario del modelo en la")
    print("sede electronica de la AEAT al importar el fichero.")
    return 1 if incidencias else 0


if __name__ == "__main__":
    raise SystemExit(main())
