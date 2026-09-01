#!/usr/bin/env python3
"""Verifica el documento de importacion generado. Obligatorio antes de entregar.

Vale para los dos formatos -XDIARIO.DBF de ContaPlus y CSV de Sage 50- porque
los dos se releen como registros canonicos. Las comprobaciones son las mismas.

Diez comprobaciones. Si falla una sola, el fichero NO se entrega.

     1  El formato es identico al del fichero muestra
     2  Todos los asientos tienen exactamente dos apuntes consecutivos
     3  Cada asiento tiene uno al debe y otro al haber
     4  Ningun importe negativo en EURODEBE, EUROHABER, PTADEBE ni PTAHABER
     5  Debe = haber en cada asiento y en el total del fichero
     6  CONTRA cruzado correctamente en los dos apuntes
     7  Numeracion correlativa, sin huecos ni repeticiones
     8  Fechas dentro del periodo, conceptos no vacios y de 25 caracteres o menos
     9  Cuadre por banco: saldo de cierre historico + apuntes = saldo final del extracto
    10  Relectura del fichero para confirmar que el programa podra leerlo

Uso
---
    python3 scripts/bancos/verificar_xdiario.py salidas/XDIARIO.DBF \\
        --muestra MUESTRA.DBF --diccionario dicc.json \\
        --extractos movimientos.json --periodo 2026-01-01:2026-12-31

    python3 scripts/bancos/verificar_xdiario.py salidas/XDIARIO.csv \\
        --muestra MUESTRA_SAGE.csv --diccionario dicc.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_documento as ld  # noqa: E402

TOLERANCIA = 0.005


class Informe:
    def __init__(self) -> None:
        self.ok: list[str] = []
        self.fallos: list[tuple[str, str]] = []
        self.avisos: list[str] = []

    def comprobar(self, titulo: str, condicion: bool, detalle: str = "") -> bool:
        if condicion:
            self.ok.append(titulo)
        else:
            self.fallos.append((titulo, detalle))
        return condicion

    @property
    def correcto(self) -> bool:
        return not self.fallos

    def como_dict(self) -> dict:
        return {"correcto": self.correcto,
                "ok": self.ok,
                "fallos": [{"prueba": t, "detalle": d} for t, d in self.fallos],
                "avisos": self.avisos}


def euros(v: float) -> str:
    return f"{v:,.2f} €".replace(",", "@").replace(".", ",").replace("@", ".")


def verificar(ruta: Path, muestra: Path | None = None,
              saldos_historicos: dict[str, float] | None = None,
              saldos_extracto: dict[str, float] | None = None,
              plan: set[str] | None = None,
              periodo: tuple[date, date] | None = None) -> Informe:
    inf = Informe()

    # 10 · Relectura (se hace primero: si no se puede leer, no hay nada que verificar)
    try:
        registros = list(ld.leer(ruta))
        formato = ld.leer_formato(ruta)
        inf.comprobar("10 · El fichero se relee correctamente", True)
    except Exception as exc:
        inf.comprobar("10 · El fichero se relee correctamente", False, str(exc))
        return inf

    # 1 · Estructura idéntica a la del fichero muestra. Se comprueba lo primero,
    # antes incluso de mirar si hay registros: un fichero con la estructura mal
    # es inservible aunque venga vacío.
    if muestra and muestra.exists():
        if ld.es_csv(muestra) != ld.es_csv(ruta):
            inf.comprobar("1 · Estructura idéntica al fichero muestra", False,
                          f"la muestra es {ld.nombre_formato(muestra)} y el fichero "
                          f"generado {ld.nombre_formato(ruta)}")
        else:
            diferencias = formato.coincide_con(ld.leer_formato(muestra))
            inf.comprobar("1 · Estructura idéntica al fichero muestra", not diferencias,
                          "; ".join(diferencias[:6]))
    else:
        inf.avisos.append("Sin fichero muestra: no se ha podido comparar la estructura")

    if not registros:
        inf.comprobar("El fichero tiene registros", False, "está vacío")
        return inf

    # Agrupar por asiento
    asientos: dict[int, list[dict]] = defaultdict(list)
    for i, r in enumerate(registros):
        asientos[int(r.get("ASIEN") or 0)].append({**r, "_pos": i})

    # 2 · Dos apuntes consecutivos
    malos = [n for n, g in asientos.items() if len(g) != 2]
    inf.comprobar("2 · Dos apuntes por asiento", not malos,
                  f"asientos con distinto número de apuntes: {sorted(malos)[:10]}")
    no_consecutivos = [n for n, g in asientos.items()
                       if len(g) == 2 and g[1]["_pos"] != g[0]["_pos"] + 1]
    inf.comprobar("2b · Los dos apuntes van seguidos", not no_consecutivos,
                  f"asientos con apuntes separados: {sorted(no_consecutivos)[:10]}")

    # 3 · Uno al debe y otro al haber
    mal_signo = []
    for n, g in asientos.items():
        if len(g) != 2:
            continue
        debes = [float(x.get("EURODEBE") or 0) for x in g]
        haberes = [float(x.get("EUROHABER") or 0) for x in g]
        if not ((debes[0] > 0 and haberes[1] > 0 and haberes[0] == 0 and debes[1] == 0) or
                (haberes[0] > 0 and debes[1] > 0 and debes[0] == 0 and haberes[1] == 0)):
            mal_signo.append(n)
    inf.comprobar("3 · Un apunte al debe y otro al haber", not mal_signo,
                  f"asientos mal formados: {sorted(mal_signo)[:10]}")

    # 4 · Sin importes negativos
    negativos = [int(r.get("ASIEN") or 0) for r in registros
                 if any(float(r.get(c) or 0) < 0
                        for c in ("EURODEBE", "EUROHABER", "PTADEBE", "PTAHABER"))]
    inf.comprobar("4 · Ningún importe negativo", not negativos,
                  f"asientos con importe negativo: {sorted(set(negativos))[:10]}")

    # 5 · Debe = haber
    descuadrados = []
    for n, g in asientos.items():
        d = sum(float(x.get("EURODEBE") or 0) for x in g)
        h = sum(float(x.get("EUROHABER") or 0) for x in g)
        if abs(d - h) > TOLERANCIA:
            descuadrados.append((n, round(d - h, 2)))
    inf.comprobar("5 · Debe = haber en cada asiento", not descuadrados,
                  f"descuadres: {descuadrados[:8]}")
    total_debe = sum(float(r.get("EURODEBE") or 0) for r in registros)
    total_haber = sum(float(r.get("EUROHABER") or 0) for r in registros)
    inf.comprobar("5b · Debe = haber en el total del fichero",
                  abs(total_debe - total_haber) <= TOLERANCIA,
                  f"debe {euros(total_debe)} vs haber {euros(total_haber)}")

    # 6 · CONTRA cruzado
    mal_contra = []
    for n, g in asientos.items():
        if len(g) != 2:
            continue
        a, b = g
        if (str(a.get("CONTRA", "")).strip() != str(b.get("SUBCTA", "")).strip()
                or str(b.get("CONTRA", "")).strip() != str(a.get("SUBCTA", "")).strip()):
            mal_contra.append(n)
    inf.comprobar("6 · CONTRA cruzado en los dos apuntes", not mal_contra,
                  f"asientos con CONTRA incorrecto: {sorted(mal_contra)[:10]}")

    # 7 · Numeración correlativa
    numeros = sorted(asientos)
    huecos = [n for n in range(numeros[0], numeros[-1] + 1) if n not in asientos]
    inf.comprobar("7 · Numeración correlativa sin huecos", not huecos,
                  f"faltan los asientos {huecos[:12]}")

    # 8 · Fechas y conceptos
    if periodo:
        fuera = [int(r.get("ASIEN") or 0) for r in registros
                 if isinstance(r.get("FECHA"), date)
                 and not (periodo[0] <= r["FECHA"] <= periodo[1])]
        inf.comprobar("8 · Fechas dentro del periodo", not fuera,
                      f"asientos fuera de periodo: {sorted(set(fuera))[:10]}")
    vacios = [int(r.get("ASIEN") or 0) for r in registros
              if not str(r.get("CONCEPTO", "")).strip()]
    largos = [int(r.get("ASIEN") or 0) for r in registros
              if len(str(r.get("CONCEPTO", ""))) > 25]
    inf.comprobar("8b · Conceptos no vacíos y de 25 caracteres o menos",
                  not vacios and not largos,
                  f"vacíos {sorted(set(vacios))[:6]} · largos {sorted(set(largos))[:6]}")

    # 9 · Cuadre por banco
    if saldos_historicos and saldos_extracto:
        movimiento: dict[str, float] = defaultdict(float)
        for r in registros:
            cuenta = str(r.get("SUBCTA", "")).strip()
            if cuenta in saldos_historicos or cuenta in saldos_extracto:
                movimiento[cuenta] += (float(r.get("EURODEBE") or 0)
                                       - float(r.get("EUROHABER") or 0))
        fallos = []
        for cuenta, final in saldos_extracto.items():
            inicial = saldos_historicos.get(cuenta, 0.0)
            calculado = round(inicial + movimiento.get(cuenta, 0.0), 2)
            if abs(calculado - final) > 0.01:
                fallos.append(f"{cuenta}: {euros(inicial)} + apuntes = {euros(calculado)}, "
                              f"extracto {euros(final)}, diferencia "
                              f"{euros(round(calculado - final, 2))}")
        inf.comprobar("9 · Cuadre por banco al céntimo", not fallos, " | ".join(fallos))
    else:
        inf.avisos.append("Sin saldos de referencia: NO se ha podido cuadrar por banco. "
                          "Es la comprobación más importante; no entregues sin ella.")

    # Subcuentas que no existen en el plan
    if plan:
        usadas = {str(r.get("SUBCTA", "")).strip() for r in registros}
        nuevas = sorted(usadas - plan)
        if nuevas:
            inf.avisos.append("Subcuentas que hay que dar de alta antes de importar: "
                              + ", ".join(nuevas))
    return inf


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichero", type=Path)
    ap.add_argument("--muestra", type=Path)
    ap.add_argument("--diccionario", type=Path, help="Para el saldo de cierre histórico")
    ap.add_argument("--extractos", type=Path, help="Para el saldo final de cada extracto")
    ap.add_argument("--cuentas", type=Path, help="Mapa banco → subcuenta")
    ap.add_argument("--periodo", help="AAAA-MM-DD:AAAA-MM-DD")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    if not args.fichero.exists():
        print(f"No existe {args.fichero}", file=sys.stderr)
        return 2

    historicos: dict[str, float] = {}
    plan: set[str] = set()
    if args.diccionario and args.diccionario.exists():
        d = json.loads(args.diccionario.read_text(encoding="utf-8"))
        historicos = {k: float(v) for k, v in d.get("bancos", {}).items()}
        plan = set(d.get("subcuentas", []))

    finales: dict[str, float] = {}
    if args.extractos and args.extractos.exists() and args.cuentas and args.cuentas.exists():
        mapa = json.loads(args.cuentas.read_text(encoding="utf-8")).get("bancos", {})
        for e in json.loads(args.extractos.read_text(encoding="utf-8")):
            cuenta = mapa.get(e.get("banco"))
            if cuenta and e.get("saldo_final") is not None:
                finales[cuenta] = float(e["saldo_final"])

    periodo = None
    if args.periodo and ":" in args.periodo:
        desde, hasta = args.periodo.split(":", 1)
        periodo = (datetime.fromisoformat(desde).date(), datetime.fromisoformat(hasta).date())

    inf = verificar(args.fichero, args.muestra, historicos, finales, plan, periodo)

    print(f"VERIFICACIÓN — {args.fichero.name}\n")
    for titulo in inf.ok:
        print(f"  ✓ {titulo}")
    for titulo, detalle in inf.fallos:
        print(f"  ✗ {titulo}")
        if detalle:
            print(f"        {detalle}")
    for aviso in inf.avisos:
        print(f"  ⚠ {aviso}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(inf.como_dict(), ensure_ascii=False, indent=2),
                             encoding="utf-8")

    print()
    if inf.correcto:
        print("Verificación superada. Pasa el informe y los movimientos de mayor importe")
        print("al agente revisor-fiscal antes de entregar.")
        return 0
    print("NO ENTREGAR: hay comprobaciones que fallan. Corrígelas y vuelve a generar.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
