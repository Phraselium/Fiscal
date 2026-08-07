#!/usr/bin/env python3
"""Cuadra los modelos de un cliente entre si y contra la contabilidad.

Es la comprobacion que evita la mayoria de los requerimientos, y la que hay que
hacer SIEMPRE antes de presentar, aunque el modelo lo haya calculado Sage: el
enlace fiscal es tan bueno como la contabilidad de la que sale.

Entrada
-------
Un JSON con las cifras del periodo. Solo hacen falta las que quieras cuadrar:
las comprobaciones para las que falten datos se omiten y se dicen al final.

    {
      "cliente": "EJEMPLO CLIENTE SL", "ejercicio": 2025, "periodo": "4T",
      "m303": [
        {"periodo": "1T", "casilla_27": 12500.00, "casilla_45": 8200.00,
         "casilla_59": 15000.00, "casilla_67": 0, "casilla_72": 0,
         "casilla_10_11": 4000.00, "casilla_36_37": 4000.00},
        ...
      ],
      "m390": {"iva_devengado": 50000.00, "iva_deducible": 33000.00,
               "volumen_operaciones": 620000.00, "entregas_intracomunitarias": 60000.00},
      "m111": [{"periodo": "1T", "base": 45000.00, "retenciones": 6750.00}, ...],
      "m190": {"base": 180000.00, "retenciones": 27000.00},
      "m115": [...], "m180": {...}, "m123": [...], "m193": {...},
      "m349": [{"periodo": "1T", "clave_E": 15000.00, "clave_A": 4000.00}, ...],
      "contabilidad": {"cifra_negocios": 620000.00, "cuenta_621": 24000.00,
                       "gasto_personal": 180000.00},
      "intrastat": {"expedicion": 55000.00, "introduccion": 12000.00}
    }

Uso
---
    python3 scripts/cuadrar.py --datos cliente-2025.json
    python3 scripts/cuadrar.py --datos cliente-2025.json --tolerancia 0.05
    python3 scripts/cuadrar.py --plantilla > cliente-2025.json

Codigos de salida: 0 todo cuadra · 1 hay descuadres · 2 error de entrada.
"""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path

PLANTILLA = {
    "cliente": "", "ejercicio": 2025, "periodo": "4T",
    "m303": [{"periodo": "1T", "casilla_27": 0, "casilla_45": 0, "casilla_59": 0,
              "casilla_60": 0, "casilla_67": 0, "casilla_72": 0,
              "casilla_10_11": 0, "casilla_36_37": 0}],
    "m390": {"iva_devengado": 0, "iva_deducible": 0, "volumen_operaciones": 0,
             "entregas_intracomunitarias": 0},
    "m111": [{"periodo": "1T", "base": 0, "retenciones": 0}],
    "m190": {"base": 0, "retenciones": 0},
    "m115": [{"periodo": "1T", "base": 0, "retenciones": 0}],
    "m180": {"base": 0, "retenciones": 0},
    "m123": [{"periodo": "1T", "base": 0, "retenciones": 0}],
    "m193": {"base": 0, "retenciones": 0},
    "m349": [{"periodo": "1T", "clave_E": 0, "clave_A": 0}],
    "contabilidad": {"cifra_negocios": 0, "cuenta_621": 0, "gasto_personal": 0},
    "intrastat": {"expedicion": 0, "introduccion": 0},
}


def d(valor) -> Decimal:
    if valor is None or valor == "":
        return Decimal("0")
    if isinstance(valor, str):
        valor = valor.replace(".", "").replace(",", ".").replace("€", "").strip()
    return Decimal(str(valor))


def euros(v: Decimal) -> str:
    return f"{v:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".") + " €"


class Informe:
    def __init__(self, tolerancia: Decimal):
        self.tolerancia = tolerancia
        self.ok: list[str] = []
        self.fallos: list[tuple[str, str, Decimal]] = []
        self.omitidas: list[str] = []

    def comparar(self, titulo: str, izq: Decimal, der: Decimal, etq_izq: str, etq_der: str,
                 norma: str = "") -> None:
        diff = izq - der
        if abs(diff) <= self.tolerancia:
            self.ok.append(f"{titulo}: {euros(izq)}")
        else:
            detalle = (f"{etq_izq} = {euros(izq)}   vs   {etq_der} = {euros(der)}"
                       f"   →  diferencia {euros(diff)}")
            if norma:
                detalle += f"\n        {norma}"
            self.fallos.append((titulo, detalle, abs(diff)))

    def omitir(self, titulo: str, motivo: str) -> None:
        self.omitidas.append(f"{titulo} — falta {motivo}")


def suma(lista, campo) -> Decimal:
    return sum((d(x.get(campo)) for x in lista or []), Decimal("0"))


def cuadrar(datos: dict, inf: Informe) -> None:
    m303 = datos.get("m303") or []
    m390 = datos.get("m390") or {}
    m349 = datos.get("m349") or []
    conta = datos.get("contabilidad") or {}

    # --- IVA -------------------------------------------------------------
    if m303 and m390:
        inf.comparar("390 devengado ↔ Σ 303 casilla 27",
                     d(m390.get("iva_devengado")), suma(m303, "casilla_27"),
                     "390", "Σ 303")
        inf.comparar("390 deducible ↔ Σ 303 casilla 45",
                     d(m390.get("iva_deducible")), suma(m303, "casilla_45"),
                     "390", "Σ 303")
    else:
        inf.omitir("390 ↔ Σ 303", "m303 o m390")

    if m390 and conta.get("cifra_negocios") is not None:
        inf.comparar("Volumen de operaciones del 390 ↔ cifra de negocios contable",
                     d(m390.get("volumen_operaciones")), d(conta.get("cifra_negocios")),
                     "390 cas. 108", "contabilidad",
                     "La diferencia debe explicarse por no sujetas, autoconsumos, "
                     "subvenciones no vinculadas al precio e ingresos financieros.")

    # Arrastre de compensaciones: casilla 67 de un periodo = casilla 72 del anterior.
    if len(m303) > 1:
        for anterior, actual in zip(m303, m303[1:]):
            inf.comparar(
                f"303 {actual.get('periodo','?')} casilla 67 ↔ "
                f"{anterior.get('periodo','?')} casilla 72",
                d(actual.get("casilla_67")), d(anterior.get("casilla_72")),
                f"cas. 67 {actual.get('periodo','?')}",
                f"cas. 72 {anterior.get('periodo','?')}")
    else:
        inf.omitir("Arrastre de compensaciones", "al menos dos periodos en m303")

    # AIB: devengado y deducible deben coincidir salvo prorrata.
    for p in m303:
        if p.get("casilla_10_11") is None or p.get("casilla_36_37") is None:
            continue
        inf.comparar(
            f"303 {p.get('periodo','?')}: AIB devengado ↔ deducible",
            d(p.get("casilla_10_11")), d(p.get("casilla_36_37")),
            "cas. 10-11", "cas. 36-37",
            "Salvo prorrata, la adquisicion intracomunitaria se autorrepercute Y se "
            "deduce por el mismo importe. Es el error nº 1 del 303.")

    # --- 303 ↔ 349 --------------------------------------------------------
    if m303 and m349:
        por_periodo = {x.get("periodo"): x for x in m349}
        for p in m303:
            q = por_periodo.get(p.get("periodo"))
            if not q:
                continue
            if p.get("casilla_59") is not None and q.get("clave_E") is not None:
                inf.comparar(
                    f"303 {p.get('periodo','?')} casilla 59 ↔ 349 clave E",
                    d(p.get("casilla_59")), d(q.get("clave_E")),
                    "303 cas. 59", "349 clave E",
                    "Entregas intracomunitarias de bienes. Un descuadre aqui genera "
                    "requerimiento automatico.")
    else:
        inf.omitir("303 ↔ 349", "m303 o m349")

    if m390 and m349:
        inf.comparar("390 entregas intracomunitarias ↔ Σ 349 clave E",
                     d(m390.get("entregas_intracomunitarias")), suma(m349, "clave_E"),
                     "390", "Σ 349")

    # --- Retenciones ------------------------------------------------------
    for periodico, anual, nombre, nota in (
        ("m111", "m190", "111 ↔ 190", "Revisa las claves: administradores van con clave E, "
                                      "dietas y rentas exentas con clave L."),
        ("m115", "m180", "115 ↔ 180", "Y contrasta la base con la cuenta 621 de arrendamientos."),
        ("m123", "m193", "123 ↔ 193", "Comprueba el devengo: la retencion de dividendos se "
                                      "devenga en la fecha de exigibilidad acordada."),
    ):
        lista, resumen = datos.get(periodico), datos.get(anual)
        if not lista or not resumen:
            inf.omitir(nombre, f"{periodico} o {anual}")
            continue
        inf.comparar(f"{nombre} bases", suma(lista, "base"), d(resumen.get("base")),
                     f"Σ {periodico[1:]}", anual[1:], nota)
        inf.comparar(f"{nombre} retenciones", suma(lista, "retenciones"),
                     d(resumen.get("retenciones")), f"Σ {periodico[1:]}", anual[1:])

    if datos.get("m115") and conta.get("cuenta_621") is not None:
        inf.comparar("Base del 115 ↔ cuenta 621 (arrendamientos)",
                     suma(datos["m115"], "base"), d(conta.get("cuenta_621")),
                     "Σ 115", "cuenta 621",
                     "Si la 621 es mayor, hay arrendamientos sin retencion: comprueba las "
                     "excepciones del art. 75.3.g RIRPF y su justificacion documental.")

    if datos.get("m111") and conta.get("gasto_personal") is not None:
        base111 = suma(datos["m111"], "base")
        if base111 > d(conta.get("gasto_personal")) + inf.tolerancia:
            inf.fallos.append((
                "Base del 111 mayor que el gasto de personal",
                f"Σ 111 = {euros(base111)}   vs   gasto de personal = "
                f"{euros(d(conta.get('gasto_personal')))}\n"
                "        Puede ser correcto si hay profesionales o administradores; "
                "verificalo.", base111 - d(conta.get("gasto_personal"))))
        else:
            inf.ok.append(f"Base del 111 dentro del gasto de personal: {euros(base111)}")

    # --- Intrastat --------------------------------------------------------
    intra = datos.get("intrastat") or {}
    if intra and m349:
        exp, clave_e = d(intra.get("expedicion")), suma(m349, "clave_E")
        if exp > clave_e + inf.tolerancia:
            inf.fallos.append((
                "Intrastat expedicion mayor que el 349 clave E",
                f"Intrastat = {euros(exp)}   vs   349 clave E = {euros(clave_e)}\n"
                "        Intrastat no puede superar al 349: el 349 incluye los bienes Y "
                "los servicios. Revisa que operaciones se han metido en Intrastat.",
                exp - clave_e))
        else:
            inf.ok.append(
                f"Intrastat expedicion ({euros(exp)}) no supera al 349 clave E "
                f"({euros(clave_e)}); la diferencia deberia ser servicios")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", type=Path)
    ap.add_argument("--tolerancia", type=float, default=0.01,
                    help="Diferencia admitida en euros por redondeos (por defecto 0,01)")
    ap.add_argument("--plantilla", action="store_true",
                    help="Imprime un JSON de ejemplo y termina")
    args = ap.parse_args()

    if args.plantilla:
        print(json.dumps(PLANTILLA, ensure_ascii=False, indent=2))
        return 0
    if not args.datos:
        ap.error("indica --datos <fichero.json> o usa --plantilla")
    if not args.datos.exists():
        print(f"No existe {args.datos}", file=sys.stderr)
        return 2

    try:
        datos = json.loads(args.datos.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"JSON invalido: {exc}", file=sys.stderr)
        return 2

    inf = Informe(Decimal(str(args.tolerancia)))
    try:
        cuadrar(datos, inf)
    except (TypeError, ValueError, AttributeError) as exc:
        print(f"Error procesando los datos: {exc}", file=sys.stderr)
        print("Comprueba la estructura con: python3 scripts/cuadrar.py --plantilla",
              file=sys.stderr)
        return 2

    cab = f"CUADRE — {datos.get('cliente', '?')}  ejercicio {datos.get('ejercicio', '?')}"
    print(cab)
    print("=" * len(cab))

    if inf.fallos:
        print(f"\nDESCUADRES ({len(inf.fallos)}) — de mayor a menor importe\n")
        for titulo, detalle, _ in sorted(inf.fallos, key=lambda x: -x[2]):
            print(f"  ✗ {titulo}")
            print(f"        {detalle}\n")

    if inf.ok:
        print(f"CUADRA ({len(inf.ok)})")
        for linea in inf.ok:
            print(f"  ✓ {linea}")

    if inf.omitidas:
        print(f"\nNO COMPROBADO ({len(inf.omitidas)}) — no es que cuadre, es que faltan datos")
        for linea in inf.omitidas:
            print(f"  · {linea}")

    print()
    if inf.fallos:
        print("Resuelve cada descuadre ANTES de presentar. Un descuadre explicable hay que")
        print("documentarlo en el expediente; uno inexplicable es un error.")
        return 1
    print("Sin descuadres en lo comprobado. Revisa la lista de 'no comprobado'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
