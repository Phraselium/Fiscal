#!/usr/bin/env python3
"""Calcula plazos tributarios y recargos por presentacion extemporanea.

Subcomandos
-----------
plazo      Vencimiento de un plazo por meses o por dias habiles desde una notificacion.
voluntaria Plazo de ingreso en periodo voluntario del art. 62.2 LGT.
recargo    Recargo del art. 27 LGT por autoliquidacion extemporanea sin requerimiento.
ejecutivo  Recargos del periodo ejecutivo del art. 28 LGT.

Ejemplos
--------
    python3 scripts/calcular_plazos.py plazo --notificacion 15/09/2026 --meses 1
    python3 scripts/calcular_plazos.py plazo --notificacion 15/09/2026 --dias-habiles 10
    python3 scripts/calcular_plazos.py voluntaria --notificacion 03/10/2026
    python3 scripts/calcular_plazos.py recargo --fin-plazo 20/07/2026 \
        --presentacion 05/11/2026 --cuota 4500

Los festivos nacionales varian cada ano y los autonomicos y locales no se
contemplan: pasa los tuyos con --festivos DD/MM/AAAA,DD/MM/AAAA. Comprueba
siempre el calendario laboral aplicable antes de apurar un plazo.
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP


def leer_fecha(texto: str) -> date:
    dia, mes, ano = (int(p) for p in texto.split("/"))
    return date(ano, mes, dia)


def formatear(fecha: date) -> str:
    return fecha.strftime("%d/%m/%Y")


def es_habil(fecha: date, festivos: set[date]) -> bool:
    return fecha.weekday() < 5 and fecha not in festivos


def siguiente_habil(fecha: date, festivos: set[date]) -> date:
    while not es_habil(fecha, festivos):
        fecha += timedelta(days=1)
    return fecha


def sumar_meses(fecha: date, meses: int) -> date:
    mes = fecha.month - 1 + meses
    ano = fecha.year + mes // 12
    mes = mes % 12 + 1
    dia = fecha.day
    while True:
        try:
            return date(ano, mes, dia)
        except ValueError:
            dia -= 1


def sumar_habiles(fecha: date, dias: int, festivos: set[date]) -> date:
    contador = 0
    actual = fecha
    while contador < dias:
        actual += timedelta(days=1)
        if es_habil(actual, festivos):
            contador += 1
    return actual


def euros(valor: Decimal) -> str:
    texto = f"{valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".") + " EUR"


def cmd_plazo(args, festivos: set[date]) -> None:
    inicio = leer_fecha(args.notificacion)
    if args.meses:
        # Los plazos por meses se cuentan de fecha a fecha (art. 30.4 Ley 39/2015).
        vencimiento = sumar_meses(inicio, args.meses)
        base = f"{args.meses} mes(es) de fecha a fecha"
    else:
        vencimiento = sumar_habiles(inicio, args.dias_habiles, festivos)
        base = f"{args.dias_habiles} dias habiles"
    final = siguiente_habil(vencimiento, festivos)
    print(f"Notificacion:        {formatear(inicio)}")
    print(f"Computo:             {base} desde el dia siguiente")
    print(f"Vencimiento teorico: {formatear(vencimiento)}")
    print(f"Vencimiento efectivo: {formatear(final)}" + ("  (trasladado por inhabil)" if final != vencimiento else ""))
    interno = final - timedelta(days=1)
    for _ in range(4):
        while not es_habil(interno, festivos):
            interno -= timedelta(days=1)
        interno -= timedelta(days=1)
    print(f"Fecha limite interna:  {formatear(siguiente_habil(interno, festivos))}  (colchon de 5 dias habiles)")


def cmd_voluntaria(args, festivos: set[date]) -> None:
    notificacion = leer_fecha(args.notificacion)
    if notificacion.day <= 15:
        vencimiento = sumar_meses(date(notificacion.year, notificacion.month, 1), 1).replace(day=20)
        regla = "notificada del 1 al 15 -> hasta el 20 del mes siguiente"
    else:
        vencimiento = sumar_meses(date(notificacion.year, notificacion.month, 1), 2).replace(day=5)
        regla = "notificada del 16 al fin de mes -> hasta el 5 del segundo mes siguiente"
    final = siguiente_habil(vencimiento, festivos)
    print("Plazo de ingreso en periodo voluntario (art. 62.2 LGT)")
    print(f"  Notificacion: {formatear(notificacion)}")
    print(f"  Regla:        {regla}")
    print(f"  Vencimiento:  {formatear(final)}")


def cmd_recargo(args) -> None:
    fin = leer_fecha(args.fin_plazo)
    presentacion = leer_fecha(args.presentacion)
    cuota = Decimal(str(args.cuota))

    if presentacion <= fin:
        print("La presentacion esta en plazo: no procede recargo.")
        return

    meses = 0
    referencia = fin
    while sumar_meses(fin, meses + 1) <= presentacion:
        meses += 1
        referencia = sumar_meses(fin, meses)

    if meses >= 12:
        porcentaje = Decimal("15")
        nota = "15 % + intereses de demora desde el dia siguiente a los 12 meses"
    else:
        porcentaje = Decimal(meses + 1)
        nota = f"{meses + 1} % (1 % + 1 % por cada mes completo de retraso)"

    recargo = cuota * porcentaje / 100
    reducido = recargo * Decimal("0.75")

    print("Recargo por declaracion extemporanea sin requerimiento previo (art. 27 LGT)")
    print(f"  Fin del plazo voluntario: {formatear(fin)}")
    print(f"  Fecha de presentacion:    {formatear(presentacion)}")
    print(f"  Retraso:                  {(presentacion - fin).days} dias ({meses} meses completos)")
    print(f"  Recargo aplicable:        {nota}")
    print(f"  Cuota:                    {euros(cuota)}")
    print(f"  Recargo:                  {euros(recargo)}")
    print(f"  Recargo con reduccion 25 %: {euros(reducido)}  (art. 27.5: ingreso en plazo y sin recurso)")
    print(f"  Total a ingresar:         {euros(cuota + reducido)} con reduccion / {euros(cuota + recargo)} sin ella")
    if meses >= 12:
        print("\n  ATENCION: ademas se devengan intereses de demora desde el mes 13.")
        print("  Consulta el tipo de interes de demora de cada ejercicio en la Ley de Presupuestos.")
    print("\n  Presentar antes de recibir un requerimiento evita la sancion del art. 191 LGT.")


def cmd_ejecutivo(args) -> None:
    cuota = Decimal(str(args.cuota))
    filas = [
        ("Ejecutivo (pago antes de la providencia de apremio)", Decimal("5")),
        ("Apremio reducido (pago en el plazo del art. 62.5)", Decimal("10")),
        ("Apremio ordinario (+ intereses de demora)", Decimal("20")),
    ]
    print("Recargos del periodo ejecutivo (art. 28 LGT)")
    print(f"  Deuda: {euros(cuota)}\n")
    for descripcion, porcentaje in filas:
        recargo = cuota * porcentaje / 100
        print(f"  {porcentaje:>3} %  {descripcion}")
        print(f"         Recargo {euros(recargo)}  ->  total {euros(cuota + recargo)}")
    print("\n  Solo el recargo de apremio ordinario devenga ademas intereses de demora.")


def main() -> int:
    analizador = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    analizador.add_argument("--festivos", default="", help="Festivos adicionales separados por coma, DD/MM/AAAA")
    subcomandos = analizador.add_subparsers(dest="comando", required=True)

    p = subcomandos.add_parser("plazo")
    p.add_argument("--notificacion", required=True)
    grupo = p.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--meses", type=int)
    grupo.add_argument("--dias-habiles", type=int)

    p = subcomandos.add_parser("voluntaria")
    p.add_argument("--notificacion", required=True)

    p = subcomandos.add_parser("recargo")
    p.add_argument("--fin-plazo", required=True)
    p.add_argument("--presentacion", required=True)
    p.add_argument("--cuota", type=float, required=True)

    p = subcomandos.add_parser("ejecutivo")
    p.add_argument("--cuota", type=float, required=True)

    args = analizador.parse_args()
    festivos = {leer_fecha(f.strip()) for f in args.festivos.split(",") if f.strip()}

    if args.comando == "plazo":
        cmd_plazo(args, festivos)
    elif args.comando == "voluntaria":
        cmd_voluntaria(args, festivos)
    elif args.comando == "recargo":
        cmd_recargo(args)
    elif args.comando == "ejecutivo":
        cmd_ejecutivo(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
