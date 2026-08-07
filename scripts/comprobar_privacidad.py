#!/usr/bin/env python3
"""Impide que datos de clientes acaben en el repositorio.

El plugin es codigo publicable; los datos del despacho no lo son. Este script
revisa lo que esta a punto de subirse y falla si encuentra informacion que no
deberia salir de la oficina.

Que busca
---------
1. NIF, NIE y CIF con LETRA DE CONTROL VALIDA. Un identificador inventado para un
   ejemplo casi nunca valida; uno real, siempre. Es la senal mas fiable.
2. IBAN con digitos de control correctos.
3. Correos electronicos y telefonos espanoles.
4. Ficheros que no deben versionarse: .xlsx, .xls, .p12, .pfx, .pem, .key, y
   cualquier ruta bajo clientes/ o salidas/.
5. Nombres de la cartera, si existe datos/nombres_privados.txt (fichero local,
   ignorado por git: una linea por nombre o token a vigilar).
6. Placeholders de configuracion ya rellenos: si config/configuracion.md ya no
   tiene PENDIENTE_COMPLETAR, es que lleva datos reales del despacho.

Uso
---
    python3 scripts/comprobar_privacidad.py                 # ficheros versionados
    python3 scripts/comprobar_privacidad.py --staged        # solo lo que va a commit
    python3 scripts/comprobar_privacidad.py --historial     # todo el historial de git
    python3 scripts/comprobar_privacidad.py --instalar-hook # pre-commit automatico

Salida: 0 limpio · 1 hallazgos · 2 error.

Los ficheros de ejemplo bajo ejemplos/ estan permitidos, pero sus NIF deben ser
sinteticos: si alguno valida como NIF real, tambien se avisa.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.validaciones import validar_iban, validar_nif  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

EXTENSIONES_PROHIBIDAS = {".xlsx", ".xls", ".xlsm", ".xltx", ".p12", ".pfx", ".pem", ".key", ".ods"}
DIRECTORIOS_PROHIBIDOS = ("clientes/", "salidas/", "datos/privado/")
EXTENSIONES_TEXTO = {".md", ".py", ".json", ".csv", ".txt", ".yml", ".yaml", ".toml", ".cfg"}

# NIF/NIE/CIF candidatos. El filtro real es la letra de control.
RE_NIF = re.compile(r"\b([XYZ]?\d{7,8}[A-TV-Z]|[A-HJNP-SUVW]\d{7}[0-9A-J])\b", re.I)
RE_IBAN = re.compile(r"\b(ES\d{2}[ ]?(?:\d{4}[ ]?){5})\b", re.I)
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b")
RE_TELEFONO = re.compile(r"(?<!\d)(?:\+34[ -]?)?[6789]\d{2}[ -]?\d{3}[ -]?\d{3}(?!\d)")

# Identificadores sinteticos admitidos en ejemplos y documentacion.
# Las pruebas NO anaden vectores aqui: generan sus identificadores en tiempo de
# ejecucion, para que ningun NIF con letra valida aparezca literal en el codigo.
NIF_PERMITIDOS = {
    "12345678Z", "87654321X", "00000001R", "B12345674", "X1234567L", "00000000T",
}
IBAN_PERMITIDOS = {
    "ES9121000418450200051332",  # IBAN de ejemplo de la documentacion del algoritmo
}
EMAIL_PERMITIDOS = {"fiscal@ejemplo.es", "noreply@anthropic.com"}
TELEFONO_PERMITIDOS = {"911234567"}


class Hallazgo:
    def __init__(self, fichero: str, linea: int, tipo: str, valor: str, detalle: str = ""):
        self.fichero, self.linea, self.tipo, self.valor, self.detalle = (
            fichero, linea, tipo, valor, detalle)

    def __str__(self) -> str:
        d = f"  — {self.detalle}" if self.detalle else ""
        return f"  {self.tipo:<22} {self.fichero}:{self.linea}  «{self.valor}»{d}"


def hay_git() -> bool:
    try:
        r = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                           cwd=RAIZ, capture_output=True, text=True)
        return r.returncode == 0 and r.stdout.strip() == "true"
    except (OSError, FileNotFoundError):
        return False


def ficheros_del_arbol() -> list[str]:
    """Recorre el directorio cuando no hay git (plugin instalado, copia suelta)."""
    ignorar = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", "node_modules"}
    salida = []
    for ruta in RAIZ.rglob("*"):
        if not ruta.is_file():
            continue
        if any(parte in ignorar for parte in ruta.parts):
            continue
        salida.append(str(ruta.relative_to(RAIZ)))
    return sorted(salida)


def ficheros_versionados(staged: bool) -> list[str]:
    if not hay_git():
        if staged:
            print("No hay repositorio git: no existe 'staging' que comprobar.", file=sys.stderr)
            raise SystemExit(2)
        print("Sin repositorio git: se revisa el contenido del directorio.\n")
        return ficheros_del_arbol()
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"] if staged \
        else ["git", "ls-files"]
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"git ha fallado: {r.stderr.strip()}", file=sys.stderr)
        raise SystemExit(2)
    return [f for f in r.stdout.split("\n") if f.strip()]


def nombres_privados() -> list[str]:
    ruta = RAIZ / "datos" / "nombres_privados.txt"
    if not ruta.exists():
        return []
    return [l.strip().upper() for l in ruta.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def revisar_texto(ruta: Path, relativo: str, denylist: list[str]) -> list[Hallazgo]:
    hallazgos: list[Hallazgo] = []
    try:
        contenido = ruta.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return hallazgos
    es_ejemplo = relativo.startswith("ejemplos/")

    for numero, linea in enumerate(contenido.splitlines(), start=1):
        for bruto in RE_NIF.findall(linea):
            nif = bruto.upper().replace(" ", "")
            if nif in NIF_PERMITIDOS:
                continue
            valido, _ = validar_nif(nif)
            if valido:
                hallazgos.append(Hallazgo(
                    relativo, numero, "NIF/NIE/CIF VALIDO", nif,
                    "un identificador con letra de control correcta casi nunca es inventado"
                    + (" (y esto es un fichero de ejemplo)" if es_ejemplo else "")))

        for bruto in RE_IBAN.findall(linea):
            iban = bruto.replace(" ", "").upper()
            if iban in IBAN_PERMITIDOS:
                continue
            valido, _ = validar_iban(iban)
            if valido:
                hallazgos.append(Hallazgo(relativo, numero, "IBAN VALIDO", iban))

        for correo in RE_EMAIL.findall(linea):
            if correo.lower() in EMAIL_PERMITIDOS or correo.lower().endswith((
                    ".example", "@example.com", "@ejemplo.es")):
                continue
            if "agenciatributaria" in correo or "boe.es" in correo:
                continue
            hallazgos.append(Hallazgo(relativo, numero, "CORREO", correo))

        for tel in RE_TELEFONO.findall(linea):
            limpio = re.sub(r"[ -]", "", tel).removeprefix("+34")
            if limpio in TELEFONO_PERMITIDOS:
                continue
            # Evita falsos positivos con importes y numeros de norma.
            if re.search(r"[.,]\s*" + re.escape(tel) + r"|" + re.escape(tel) + r"\s*[.,]\d", linea):
                continue
            hallazgos.append(Hallazgo(relativo, numero, "TELEFONO", tel))

        alto = linea.upper()
        for nombre in denylist:
            if re.search(r"\b" + re.escape(nombre) + r"\b", alto):
                hallazgos.append(Hallazgo(
                    relativo, numero, "NOMBRE DE CARTERA", nombre,
                    "coincide con datos/nombres_privados.txt"))
    return hallazgos


def revisar(ficheros: list[str]) -> list[Hallazgo]:
    denylist = nombres_privados()
    hallazgos: list[Hallazgo] = []

    for relativo in ficheros:
        ruta = RAIZ / relativo
        sufijo = Path(relativo).suffix.lower()

        if sufijo in EXTENSIONES_PROHIBIDAS:
            hallazgos.append(Hallazgo(
                relativo, 0, "FICHERO PROHIBIDO", relativo,
                "hojas de calculo y certificados no se versionan nunca"))
            continue
        if any(relativo.startswith(d) for d in DIRECTORIOS_PROHIBIDOS):
            hallazgos.append(Hallazgo(
                relativo, 0, "RUTA PROHIBIDA", relativo,
                "contiene datos de clientes o ficheros generados"))
            continue
        if not ruta.exists() or sufijo not in EXTENSIONES_TEXTO:
            continue
        hallazgos.extend(revisar_texto(ruta, relativo, denylist))

    config = RAIZ / "config" / "configuracion.md"
    if config.exists() and str(config.relative_to(RAIZ)) in ficheros:
        if "PENDIENTE_COMPLETAR" not in config.read_text(encoding="utf-8"):
            hallazgos.append(Hallazgo(
                "config/configuracion.md", 0, "CONFIG RELLENA", "sin PENDIENTE_COMPLETAR",
                "parece llevar datos reales del despacho; no la subas rellena"))
    return hallazgos


def revisar_historial() -> list[Hallazgo]:
    if not hay_git():
        print("No hay repositorio git: no hay historial que revisar.", file=sys.stderr)
        raise SystemExit(2)
    denylist = nombres_privados()
    if not denylist:
        print("Para revisar el historial hace falta datos/nombres_privados.txt "
              "con los nombres a vigilar.", file=sys.stderr)
        return []
    hallazgos: list[Hallazgo] = []
    for nombre in denylist:
        r = subprocess.run(["git", "log", "--all", "--oneline", "-S", nombre],
                           cwd=RAIZ, capture_output=True, text=True)
        for linea in r.stdout.strip().splitlines():
            hallazgos.append(Hallazgo(
                "historial", 0, "NOMBRE EN COMMIT", nombre, linea.strip()))
    return hallazgos


HOOK = """#!/bin/sh
# Instalado por scripts/comprobar_privacidad.py --instalar-hook
python3 scripts/comprobar_privacidad.py --staged || {
    echo ""
    echo "Commit abortado: hay datos privados en lo que ibas a subir."
    echo "Corrigelo, o salta la comprobacion con: git commit --no-verify"
    exit 1
}
"""


def instalar_hook() -> int:
    destino = RAIZ / ".git" / "hooks" / "pre-commit"
    if not destino.parent.exists():
        print("No encuentro .git/hooks", file=sys.stderr)
        return 2
    if destino.exists() and "comprobar_privacidad" not in destino.read_text(encoding="utf-8"):
        print(f"Ya existe un pre-commit en {destino}. Anade esta linea a mano:", file=sys.stderr)
        print("  python3 scripts/comprobar_privacidad.py --staged || exit 1", file=sys.stderr)
        return 2
    destino.write_text(HOOK, encoding="utf-8")
    destino.chmod(0o755)
    print(f"Hook instalado en {destino}")
    print("A partir de ahora, cada commit se comprueba antes de crearse.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staged", action="store_true", help="Solo lo que va al commit")
    ap.add_argument("--historial", action="store_true", help="Busca en todo el historial de git")
    ap.add_argument("--instalar-hook", action="store_true")
    args = ap.parse_args()

    if args.instalar_hook:
        return instalar_hook()

    hallazgos = revisar_historial() if args.historial \
        else revisar(ficheros_versionados(args.staged))

    ambito = ("el historial" if args.historial
              else "los ficheros en staging" if args.staged
              else "los ficheros versionados")

    if not hallazgos:
        print(f"Privacidad: sin hallazgos en {ambito}.")
        if not nombres_privados() and not args.historial:
            print("\nSugerencia: crea datos/nombres_privados.txt (ignorado por git) con los")
            print("nombres de la cartera para que la comprobacion tambien los vigile.")
        return 0

    print(f"{len(hallazgos)} hallazgos en {ambito}:\n")
    por_tipo: dict[str, list[Hallazgo]] = {}
    for h in hallazgos:
        por_tipo.setdefault(h.tipo, []).append(h)
    for tipo in sorted(por_tipo):
        for h in por_tipo[tipo]:
            print(h)
    print("\nNo subas esto. Si algun hallazgo es un falso positivo, anade el valor a la")
    print("lista de permitidos de scripts/comprobar_privacidad.py y explica por que.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
