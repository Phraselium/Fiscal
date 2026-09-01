#!/usr/bin/env python3
"""Deduce los criterios de imputacion del diario contable del ejercicio anterior.

Todo el criterio sale del historico del PROPIO cliente. Nada de criterios
genericos: si un movimiento no tiene respaldo en su diario, va a la cuenta puente.

Que se extrae
-------------
1. Concepto → contrapartida. Se agrupa el diario por ASIEN. Dentro de cada
   asiento, para cada linea cuya SUBCTA sea de tesoreria (57*), se busca la linea
   con el MISMO CONCEPTO y el importe exactamente contrario: esa es su
   contrapartida. El emparejamiento por importe es imprescindible porque los
   asientos agrupan varios pagos del dia y el campo CONTRA viene casi siempre
   vacio.

2. Nombre de tercero → subcuenta. De las lineas 400*/410* (excluidas las
   transitorias 4009*) se limpia el concepto de prefijos y numeros de factura y
   se trocea en palabras de 4 o mas letras. Cada palabra apunta a una subcuenta.
   Se acepta cuando es unanime, o cuando gana con >=60 % y al menos 2 apariciones.

3. Empleados. De los conceptos «P/NOMINAS MES <NOMBRE>» salen los nombres que
   aparecen en nomina, para reconocer despues las transferencias a empleados.

4. Cuentas de banco y su saldo de cierre, para cuadrar contra los extractos.

Uso
---
    python3 scripts/bancos/diccionario_diario.py XDIARIO_2025.dbf
    python3 scripts/bancos/diccionario_diario.py XDIARIO_2025.dbf --json dicc.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_documento as ld  # noqa: E402

# Palabras que NO identifican a un tercero: municipios, formas juridicas y
# genericos de razon social. Son la primera fuente de errores de imputacion.
PARADAS = {
    "VALENCIA", "ALBORAYA", "MADRID", "BARCELONA", "SEVILLA", "ZARAGOZA", "MALAGA",
    "MURCIA", "BILBAO", "ALICANTE", "CORDOBA", "VALLADOLID", "GIJON", "GRANADA",
    "PATERNA", "BURJASSOT", "TORRENT", "MISLATA", "CATARROJA", "MANISES", "SAGUNTO",
    "CENTRO", "GRUPO", "DISTRIBUCIONES", "DISTRIBUCION", "MAYORISTA", "BAZAR", "PUNT",
    "SOCIEDAD", "LIMITADA", "ANONIMA", "COMERCIAL", "COMERCIO", "SERVICIOS", "SERVICIO",
    "ESPANA", "ESPANOLA", "IBERICA", "NACIONAL", "GENERAL", "SUMINISTROS", "SUMINISTRO",
    "PRODUCTOS", "PRODUCTO", "MATERIALES", "MATERIAL", "EMPRESA", "COMPANIA", "HERMANOS",
    "NUEVA", "NUEVO", "GESTION", "GESTIONES", "ASESORIA", "CONSULTING", "SOLUCIONES",
    "FACTURA", "FACTURAS", "RECIBO", "RECIBOS", "PAGO", "PAGOS", "COBRO", "COBROS",
    "MES", "MESES", "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO",
    "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE", "TOTAL", "VARIOS",
}

# Prefijos del concepto que no forman parte del nombre del tercero.
RE_PREFIJOS = re.compile(
    r"^(P/S\.?FRA\.?|S/FRA\.?|P/FRA\.?|N/FRA\.?|FRA\.?|REC\.?|RECIBO|P/REC\.?|"
    r"PAGO|COBRO|TRANSF\.?|TRANSFERENCIA)\s*", re.I)
RE_NUMEROS = re.compile(r"\b\d[\d./-]*\b")
RE_PALABRA = re.compile(r"[A-ZÑÇ]{4,}")
RE_NOMINA = re.compile(r"P/NOMINAS?\s+MES\s+(.+)", re.I)

# Asientos que no reflejan operaciones: apertura, regularizacion y cierre.
RE_NO_OPERATIVO = re.compile(r"(APERTURA|REGULARIZ|CIERRE|ASIENTO DE APERTURA)", re.I)

CUOTA_MINIMA = 0.60
APARICIONES_MINIMAS = 2


def sin_acentos(texto) -> str:
    if texto is None:
        return ""
    t = unicodedata.normalize("NFD", str(texto).upper())
    return "".join(c for c in t if unicodedata.category(c) != "Mn").strip()


def es_parada(palabra: str) -> bool:
    """Compara contra PARADAS ignorando el plural.

    En la lista basta con poner el singular: GENERAL cubre tambien GENERALES, y
    SERVICIO cubre SERVICIOS. Sin esto, el plural se colaria como identificador
    de tercero, que es justo lo que mas errores de imputacion provoca.
    """
    if palabra in PARADAS:
        return True
    for sufijo in ("ES", "S"):
        if palabra.endswith(sufijo) and palabra[:-len(sufijo)] in PARADAS:
            return True
    return False


def tokens(concepto: str) -> list[str]:
    """Palabras del concepto que pueden identificar a un tercero."""
    limpio = RE_PREFIJOS.sub("", sin_acentos(concepto))
    limpio = RE_NUMEROS.sub(" ", limpio)
    return [p for p in RE_PALABRA.findall(limpio) if not es_parada(p)]


def es_tesoreria(subcta: str) -> bool:
    return str(subcta).startswith("57")


def es_banco(subcta: str) -> bool:
    return str(subcta).startswith("572")


def es_proveedor_o_acreedor(subcta: str) -> bool:
    s = str(subcta)
    return (s.startswith("400") or s.startswith("410")) and not s.startswith("4009")


class Diccionario:
    def __init__(self) -> None:
        self.concepto_a_contrapartida: dict[str, str] = {}
        self.token_a_subcuenta: dict[str, str] = {}
        self.empleados: set[str] = set()
        self.bancos: dict[str, float] = {}          # subcuenta 572* → saldo de cierre
        self.longitud_subcuenta: int = 0
        self.subcuentas: set[str] = set()
        self.conceptos_por_subcuenta: dict[str, list[str]] = defaultdict(list)
        self.avisos: list[str] = []

    def como_dict(self) -> dict:
        return {
            "concepto_a_contrapartida": self.concepto_a_contrapartida,
            "token_a_subcuenta": self.token_a_subcuenta,
            "empleados": sorted(self.empleados),
            "bancos": self.bancos,
            "longitud_subcuenta": self.longitud_subcuenta,
            "subcuentas": sorted(self.subcuentas),
            "avisos": self.avisos,
        }

    @classmethod
    def desde_dict(cls, d: dict) -> "Diccionario":
        x = cls()
        x.concepto_a_contrapartida = d.get("concepto_a_contrapartida", {})
        x.token_a_subcuenta = d.get("token_a_subcuenta", {})
        x.empleados = set(d.get("empleados", []))
        x.bancos = d.get("bancos", {})
        x.longitud_subcuenta = d.get("longitud_subcuenta", 0)
        x.subcuentas = set(d.get("subcuentas", []))
        x.avisos = d.get("avisos", [])
        return x

    def buscar_tercero(self, texto: str, umbral: float = 0.85) -> tuple[str | None, bool]:
        """Devuelve (subcuenta, fue_aproximada). Lo aproximado siempre se revisa.

        Tres pasadas, de mas a menos fiable:
          1. Coincidencia exacta de palabra.
          2. Coincidencia por PREFIJO. El campo CONCEPTO del XDIARIO son 25
             caracteres, asi que los nombres largos llegan truncados al historico:
             «P/S.FRA.ASEGURADORA GENERAL» se guarda como «...GENER». Sin esta
             pasada, el proveedor no se reconoceria nunca.
          3. difflib con corte 0,85, que resuelve las erratas del banco
             (AYVENS/AYWENS, DISCALMAQ/DIVALMARQ).

        Las pasadas 2 y 3 devuelven «aproximada»: el movimiento se marca para revisar.
        """
        palabras = tokens(texto)
        for palabra in palabras:
            if palabra in self.token_a_subcuenta:
                return self.token_a_subcuenta[palabra], False

        for palabra in palabras:
            for token, cuenta in self.token_a_subcuenta.items():
                if len(token) >= 5 and palabra.startswith(token):
                    return cuenta, True

        import difflib
        candidatos = list(self.token_a_subcuenta)
        for palabra in palabras:
            parecidas = difflib.get_close_matches(palabra, candidatos, n=1, cutoff=umbral)
            if parecidas:
                return self.token_a_subcuenta[parecidas[0]], True
        return None, False


def construir(ruta_diario: Path) -> Diccionario:
    """El diario del ejercicio anterior, venga en DBF de ContaPlus o en CSV de Sage."""
    dicc = Diccionario()
    lineas = list(ld.leer(ruta_diario))
    if not lineas:
        raise SystemExit(f"{ruta_diario.name} no tiene registros")

    campos = set(lineas[0])
    for obligatorio in ("ASIEN", "SUBCTA", "CONCEPTO"):
        if obligatorio not in campos:
            raise SystemExit(
                f"{ruta_diario.name} no parece un diario contable: falta {obligatorio}.\n"
                f"Campos encontrados: {', '.join(sorted(campos))[:200]}\n"
                "Si es un CSV, comprueba que la cabecera nombre las columnas de asiento, "
                "cuenta y concepto.")

    def debe(l):
        return float(l.get("EURODEBE") or 0)

    def haber(l):
        return float(l.get("EUROHABER") or 0)

    # Longitud de subcuenta del plan del cliente: la manda el historico.
    longitudes = Counter(len(str(l["SUBCTA"]).strip())
                         for l in lineas if str(l["SUBCTA"]).strip())
    dicc.longitud_subcuenta = longitudes.most_common(1)[0][0] if longitudes else 0

    asientos: dict[int, list[dict]] = defaultdict(list)
    for l in lineas:
        subcta = str(l["SUBCTA"]).strip()
        if not subcta:
            continue
        dicc.subcuentas.add(subcta)
        asientos[int(l["ASIEN"] or 0)].append(l)
        dicc.conceptos_por_subcuenta[subcta].append(str(l["CONCEPTO"]).strip())

    # --- 1. Concepto → contrapartida ------------------------------------
    votos: dict[str, Counter] = defaultdict(Counter)
    operativos = 0
    for numero, grupo in asientos.items():
        if any(RE_NO_OPERATIVO.search(str(l["CONCEPTO"])) for l in grupo):
            continue
        operativos += 1
        for linea in grupo:
            if not es_tesoreria(linea["SUBCTA"]):
                continue
            concepto = sin_acentos(linea["CONCEPTO"])
            importe = debe(linea) - haber(linea)
            if not concepto or abs(importe) < 0.005:
                continue
            for otra in grupo:
                if otra is linea or es_tesoreria(otra["SUBCTA"]):
                    continue
                if sin_acentos(otra["CONCEPTO"]) != concepto:
                    continue
                if abs((debe(otra) - haber(otra)) + importe) < 0.005:
                    votos[concepto][str(otra["SUBCTA"]).strip()] += 1
                    break
    for concepto, cuenta in votos.items():
        dicc.concepto_a_contrapartida[concepto] = cuenta.most_common(1)[0][0]

    if not operativos:
        dicc.avisos.append(
            "Todos los asientos del historico parecen de apertura, regularizacion o "
            "cierre: no hay criterios que deducir.")

    # --- 2. Token → subcuenta de tercero --------------------------------
    por_token: dict[str, Counter] = defaultdict(Counter)
    for linea in lineas:
        subcta = str(linea["SUBCTA"]).strip()
        if not es_proveedor_o_acreedor(subcta):
            continue
        for palabra in tokens(linea["CONCEPTO"]):
            por_token[palabra][subcta] += 1
    for palabra, cuentas in por_token.items():
        total = sum(cuentas.values())
        cuenta, veces = cuentas.most_common(1)[0]
        if len(cuentas) == 1 or (veces / total >= CUOTA_MINIMA and veces >= APARICIONES_MINIMAS):
            dicc.token_a_subcuenta[palabra] = cuenta

    # --- 3. Empleados ----------------------------------------------------
    for linea in lineas:
        m = RE_NOMINA.match(sin_acentos(linea["CONCEPTO"]))
        if m:
            for palabra in RE_PALABRA.findall(m.group(1)):
                if palabra not in PARADAS:
                    dicc.empleados.add(palabra)

    # --- 4. Bancos y saldo de cierre -------------------------------------
    saldos: dict[str, float] = defaultdict(float)
    for numero, grupo in asientos.items():
        if any(RE_NO_OPERATIVO.search(str(l["CONCEPTO"])) for l in grupo):
            continue
        for linea in grupo:
            subcta = str(linea["SUBCTA"]).strip()
            if es_banco(subcta):
                saldos[subcta] += debe(linea) - haber(linea)
    dicc.bancos = {k: round(v, 2) for k, v in sorted(saldos.items())}

    if not dicc.bancos:
        dicc.avisos.append("No hay ninguna subcuenta 572* con movimiento en el historico.")
    if len(dicc.token_a_subcuenta) < 5:
        dicc.avisos.append(
            f"Solo {len(dicc.token_a_subcuenta)} terceros identificables: el historico es "
            "corto o los conceptos no llevan nombre. Iran muchos movimientos a la puente.")
    return dicc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xdiario", type=Path,
                    help="Diario del ejercicio anterior (.dbf de ContaPlus o .csv de Sage)")
    ap.add_argument("--json", type=Path)
    ap.add_argument("--limite", type=int, default=25)
    args = ap.parse_args()

    if not args.xdiario.exists():
        print(f"No existe {args.xdiario}", file=sys.stderr)
        return 2

    d = construir(args.xdiario)

    print(f"Diccionario deducido de {args.xdiario.name} "
          f"[{ld.nombre_formato(args.xdiario)}]\n")
    print(f"  Longitud de subcuenta:    {d.longitud_subcuenta} dígitos")
    print(f"  Subcuentas en el plan:    {len(d.subcuentas)}")
    print(f"  Conceptos con criterio:   {len(d.concepto_a_contrapartida)}")
    print(f"  Terceros identificables:  {len(d.token_a_subcuenta)}")
    print(f"  Empleados en nómina:      {len(d.empleados)}")

    print(f"\n  Cuentas bancarias y saldo de cierre:")
    for cuenta, saldo in d.bancos.items():
        print(f"      {cuenta:<14}{saldo:>14,.2f}".replace(",", "."))

    if d.empleados:
        print(f"\n  Empleados: {', '.join(sorted(d.empleados)[:12])}"
              + (" …" if len(d.empleados) > 12 else ""))

    print(f"\n  Muestra de terceros:")
    for palabra, cuenta in sorted(d.token_a_subcuenta.items())[:args.limite]:
        print(f"      {palabra:<26}→ {cuenta}")
    if len(d.token_a_subcuenta) > args.limite:
        print(f"      … y {len(d.token_a_subcuenta) - args.limite} más")

    for aviso in d.avisos:
        print(f"\n  ⚠ {aviso}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(d.como_dict(), ensure_ascii=False, indent=2),
                             encoding="utf-8")
        print(f"\nEscrito {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
