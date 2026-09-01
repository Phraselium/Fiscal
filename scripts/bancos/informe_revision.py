#!/usr/bin/env python3
"""README de revision que acompaña al XDIARIO.DBF.

Un solo fichero de texto al lado del DBF. Quien lo recibe tiene que poder, sin
abrir nada más:

    · saber que el fichero NO esta contabilizado y que falta revisarlo,
    · comprobar el cuadre de cada banco sumando a mano las cifras que se le dan,
    · ver que subcuentas hay que dar de alta antes de importar,
    · localizar en su extracto cada movimiento que hay que mirar,
    · y saber que decisiones de criterio quedan pendientes.

Todas las cifras salen del propio mapeo. Ninguna se escribe a mano. El cuadre se
publica descompuesto —saldo inicial, cargos, abonos, saldo calculado, saldo del
extracto y diferencia— para que la suma se pueda rehacer con los ojos.

Uso
---
    python3 scripts/bancos/informe_revision.py --clasificado clasificado.json \\
        --diccionario dicc.json --cuentas cuentas.json --extractos movimientos.json \\
        --verificacion verificacion.json --salida salidas/README.md
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

PUENTE_POR_DEFECTO = "5550000"

DECISIONES = (
    "¿Las compras con tarjeta van a compras (600) o a gastos? Cargarlas contra la "
    "cuenta del proveedor descuadra su saldo si no hay factura detrás.",
    "Confirmar el periodo de las liquidaciones de Seguridad Social: se ha deducido "
    "de la fecha de cargo.",
    "Confirmar el tratamiento de las operaciones de valores e inversiones.",
    "Revisar los cobros imputados contra cuentas de proveedor: pueden ser rappels, "
    "devoluciones o clientes distintos.",
)

COMO_SE_HA_HECHO = (
    "Los criterios de imputación salen del XDIARIO del ejercicio anterior del propio "
    "cliente: concepto → contrapartida emparejando por importe dentro de cada asiento, "
    "y nombre de tercero → subcuenta a partir de las líneas 400*/410*.",
    "Lo que no tiene respaldo en ese histórico va a la cuenta puente. No se ha "
    "inventado ninguna cuenta ni ningún importe.",
    "Los traspasos entre cuentas propias se han emparejado en una pasada global por "
    "importe contrario, cuentas distintas y fecha dentro de ±5 días. Solo generan un "
    "asiento, el del lado del pago.",
    "Las compras con tarjeta solo se imputan a un proveedor si el comercio está en la "
    "lista blanca validada. El resto va a la puente.",
)


# --- formato -------------------------------------------------------------

def eur(valor: float | None) -> str:
    """Importe en formato español. None se marca, no se disfraza de cero."""
    if valor is None:
        return "—"
    entero = f"{abs(valor):,.2f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return f"-{entero}" if valor < 0 else entero


def plural(n: int, singular: str, plural_: str) -> str:
    return f"{n} {singular if n == 1 else plural_}"


def celda(texto) -> str:
    """La barra vertical parte una tabla markdown: se escapa."""
    return str(texto).replace("|", "\\|").replace("\n", " ").strip()


def tabla(columnas: list[str], filas: list[list], derecha: set[int] = frozenset()) -> list[str]:
    if not filas:
        return ["_Ninguno._", ""]
    sep = ["---:" if i in derecha else "---" for i in range(len(columnas))]
    salida = ["| " + " | ".join(columnas) + " |", "| " + " | ".join(sep) + " |"]
    salida += ["| " + " | ".join(celda(c) for c in fila) + " |" for fila in filas]
    return salida + [""]


# --- secciones -----------------------------------------------------------

def vivos_de(clasificados: list[dict]) -> list[dict]:
    """Los que generan asiento: sin el otro lado de los traspasos ni los de importe cero."""
    return [c for c in clasificados
            if not c.get("contabilizado_en_otro") and abs(c["importe"]) >= 0.005]


def cuentas_a_dar_de_alta(verificacion: dict) -> list[str]:
    return sorted({c.strip()
                   for a in (verificacion or {}).get("avisos", []) if "dar de alta" in a
                   for c in a.split(":")[-1].split(",") if c.strip()})


def seccion_cuadre(clasificados, cuentas, saldos_hist, saldos_final) -> list[str]:
    filas, descuadres, sin_saldo = [], [], []
    for banco, subcuenta in sorted(cuentas.get("bancos", {}).items()):
        movs = [c for c in clasificados
                if c["banco"] == banco and not c.get("contabilizado_en_otro")]
        inicial = saldos_hist.get(subcuenta, 0.0)
        cargos = round(sum(c["importe"] for c in movs if c["importe"] < 0), 2)
        abonos = round(sum(c["importe"] for c in movs if c["importe"] > 0), 2)
        calculado = round(inicial + cargos + abonos, 2)
        extracto = saldos_final.get(subcuenta)
        diferencia = None if extracto is None else round(calculado - extracto, 2)
        if diferencia is None:
            sin_saldo.append(banco)
        elif abs(diferencia) >= 0.005:
            descuadres.append(banco)
        filas.append([banco, subcuenta, eur(inicial), eur(cargos), eur(abonos),
                      eur(calculado), eur(extracto), eur(diferencia)])

    lineas = ["## Cuadre por banco", ""]
    lineas += tabla(["Banco", "Subcuenta", "Saldo inicial", "Cargos", "Abonos",
                     "Saldo calculado", "Saldo del extracto", "Diferencia"],
                    filas, derecha={2, 3, 4, 5, 6, 7})
    lineas += ["`Saldo calculado = saldo inicial + cargos + abonos`. El saldo inicial es el "
               "cierre del histórico; el del extracto, el que trae el banco.", ""]
    if descuadres:
        lineas += [f"> **La diferencia no es cero en: {', '.join(descuadres)}.** "
                   "No importes el fichero: o el histórico no está cerrado, o faltan "
                   "movimientos en el extracto.", ""]
    if sin_saldo:
        # Sin saldo final del extracto no hay descuadre: hay comprobacion que falta.
        lineas += [f"> **No se ha podido comprobar el cuadre de: {', '.join(sin_saldo)}.** "
                   "El extracto no traía saldo final. Cuadra esas cuentas a mano antes "
                   "de importar.", ""]
    if not descuadres and not sin_saldo:
        lineas += ["La diferencia es cero en todas las cuentas: el fichero cuadra al "
                   "céntimo con los extractos y con el cierre del ejercicio anterior.", ""]
    return lineas


def seccion_verificacion(verificacion: dict) -> list[str]:
    if not verificacion:
        return ["## Verificación automática", "",
                "> **No se ha ejecutado.** No entregues el fichero sin pasar "
                "`verificar_xdiario.py`.", ""]
    lineas = ["## Verificación automática", ""]
    fallos = verificacion.get("fallos") or []
    pruebas = verificacion.get("ok", [])
    if verificacion.get("correcto") and not fallos:
        lineas += [f"Pasa la verificación completa: {plural(len(pruebas), 'prueba', 'pruebas')}, "
                   "ninguna fallida.", ""]
    else:
        lineas += ["> **El fichero NO ha pasado la verificación. No lo importes.**", ""]
        # verificar_xdiario serializa cada fallo como {"prueba": ..., "detalle": ...};
        # en memoria es una tupla. Se aceptan las dos formas.
        lineas += tabla(["Comprobación", "Fallo"],
                        [[f["prueba"], f.get("detalle", "")] if isinstance(f, dict)
                         else list(f) for f in fallos])
    def orden(t: str):
        cabeza = t.split(" ")[0]
        return (int("".join(d for d in cabeza if d.isdigit()) or 0), cabeza)

    for prueba in sorted(pruebas, key=orden):
        lineas.append(f"- {prueba}")
    return lineas + [""]


def seccion_contenido(clasificados, cuentas, asientos) -> list[str]:
    puente = cuentas.get("puente", PUENTE_POR_DEFECTO)
    vivos = vivos_de(clasificados)
    en_puente = [c for c in vivos if c["contrapartida"] == puente]
    marcados = [c for c in vivos if c.get("revisar")]
    pct = len(en_puente) / len(vivos) * 100 if vivos else 0.0
    cero = [c for c in clasificados
            if not c.get("contabilizado_en_otro") and abs(c["importe"]) < 0.005]

    filas = [
        ["Movimientos leídos de los extractos", len(clasificados)],
        ["Asientos generados", asientos],
        ["Apuntes", asientos * 2],
        ["Traspasos entre cuentas propias emparejados",
         sum(1 for c in clasificados if c["regla"] == "10-traspaso")],
        ["Movimientos de importe cero (sin asiento)", len(cero)],
        [f"Movimientos en la cuenta puente {puente}",
         f"{len(en_puente)} ({pct:.1f} % del total)"],
        ["Movimientos marcados para revisar", len(marcados)],
    ]
    return ["## Qué contiene el fichero", ""] + tabla(["Concepto", ""], filas, derecha={1})


def seccion_por_regla(clasificados) -> list[str]:
    por_regla = defaultdict(lambda: [0, 0.0])
    for c in clasificados:
        por_regla[c["regla"]][0] += 1
        por_regla[c["regla"]][1] += abs(c["importe"])
    filas = [[regla, n, eur(round(importe, 2))]
             for regla, (n, importe) in sorted(por_regla.items(), key=lambda x: -x[1][0])]
    return (["## Cómo se ha imputado", "",
             "Cada regla lleva el número que tiene en `references/reglas-de-imputacion.md`.",
             ""]
            + tabla(["Regla aplicada", "Movimientos", "Importe"], filas, derecha={1, 2}))


def seccion_puente(clasificados, cuentas) -> list[str]:
    puente = cuentas.get("puente", PUENTE_POR_DEFECTO)
    en_puente = [c for c in vivos_de(clasificados) if c["contrapartida"] == puente]
    por_motivo = defaultdict(lambda: [0, 0.0])
    for c in en_puente:
        clave = c.get("motivo_revision") or c["regla"]
        por_motivo[clave][0] += 1
        por_motivo[clave][1] += abs(c["importe"])
    filas = [[motivo, n, eur(round(importe, 2))]
             for motivo, (n, importe) in sorted(por_motivo.items(), key=lambda x: -x[1][0])]
    return ([f"## Cuenta puente {puente}, por motivo", "",
             "Se ha preferido dejar estos movimientos en la puente antes que imputarlos "
             "sin respaldo en el histórico del cliente.", ""]
            + tabla(["Motivo", "Movimientos", "Importe"], filas, derecha={1, 2}))


def seccion_tarjeta(clasificados) -> list[str]:
    tarjeta = [c for c in vivos_de(clasificados) if c["regla"].startswith("15-tarjeta")]
    if not tarjeta:
        return ["## Compras con tarjeta", "",
                "No hay compras con tarjeta en el periodo.", ""]
    filas = [[c["texto"][:70], c["contrapartida"],
              "validado" if c["regla"].endswith("lista-blanca") else "no validado → puente"]
             for c in sorted(tarjeta, key=lambda x: -abs(x["importe"]))[:40]]
    return (["## Compras con tarjeta", "",
             "Solo se imputan a un proveedor las de comercios validados. Cargar una compra "
             "con tarjeta contra la cuenta del proveedor **descuadra su saldo** si no hay "
             "factura detrás.", ""]
            + tabla(["Texto del extracto", "Cuenta", "Estado"], filas))


def seccion_revisar(clasificados, cuentas) -> list[str]:
    puente = cuentas.get("puente", PUENTE_POR_DEFECTO)
    filas_mov = [c for c in vivos_de(clasificados)
                 if c.get("revisar") or c["contrapartida"] == puente]
    filas = [[c["fecha"], c["banco"], eur(c["importe"]), c["contrapartida"],
              c["regla"], c.get("motivo_revision", ""), c["texto"][:80]]
             for c in sorted(filas_mov, key=lambda x: (x["fecha"], -abs(x["importe"])))]
    return (["## Movimientos a revisar", "",
             "Los que van a la cuenta puente y los marcados. Se da el **texto original del "
             "extracto** para poder localizar cada uno en el banco.", ""]
            + tabla(["Fecha", "Banco", "Importe", "Cuenta asignada", "Regla", "Motivo",
                     "Texto original del extracto"], filas, derecha={2}))


def seccion_traspasos(clasificados) -> list[str]:
    fuera = [c for c in clasificados if c.get("contabilizado_en_otro")]
    if not fuera:
        return []
    filas = [[c["fecha"], c["banco"], eur(c["importe"]), c["texto"][:70]] for c in fuera]
    return (["## Movimientos que no generan asiento propio", "",
             "Es el otro lado de un traspaso entre cuentas propias: el asiento ya está "
             "hecho desde la cuenta que paga, con la otra cuenta bancaria como "
             "contrapartida. Aparecen aquí para que no parezca que se han perdido.", ""]
            + tabla(["Fecha", "Banco", "Importe", "Texto del extracto"], filas, derecha={2}))


def seccion_pasos(clasificados, cuentas, verificacion) -> list[str]:
    puente = cuentas.get("puente", PUENTE_POR_DEFECTO)
    vivos = vivos_de(clasificados)
    en_puente = [c for c in vivos if c["contrapartida"] == puente]
    marcados = [c for c in vivos if c.get("revisar") and c["contrapartida"] != puente]
    nuevas = cuentas_a_dar_de_alta(verificacion)

    pasos = []
    if nuevas:
        pasos.append(f"**Dar de alta {plural(len(nuevas), 'subcuenta', 'subcuentas')}** "
                     "en el plan contable: "
                     + ", ".join(f"`{c}`" for c in nuevas)
                     + ". Sin esto la importación falla.")
    else:
        pasos.append("Comprobar el plan contable: todas las subcuentas usadas ya existen, "
                     "no hay que dar ninguna de alta.")
    if en_puente:
        cuantos = ("el movimiento" if len(en_puente) == 1
                   else f"los {len(en_puente)} movimientos")
        pasos.append(f"**Reimputar {cuantos} de la cuenta puente `{puente}`**, "
                     "en «Movimientos a revisar».")
    if marcados:
        cuantos = ("el movimiento imputado pero marcado" if len(marcados) == 1
                   else f"los {len(marcados)} movimientos imputados pero marcados")
        pasos.append(f"**Revisar {cuantos}**: coincidencias aproximadas, cobros contra "
                     "cuentas de proveedor y reconocimientos por nombre de pila.")
    pasos.append("**Resolver las decisiones de criterio** del final de este documento.")
    pasos.append("**Importar el `XDIARIO.DBF`** en ContaPlus y comprobar el cuadre de "
                 "bancos contra los extractos.")
    return (["## Qué hay que hacer antes de importar", ""]
            + [f"{i}. {p}" for i, p in enumerate(pasos, 1)] + [""])


def readme(clasificados, cuentas, verificacion, saldos_hist, saldos_final,
           asientos: int, titulo: str, fichero: str) -> str:
    lineas = [f"# {titulo}", "",
              "> **Este fichero está pendiente de revisar e importar. No está "
              "contabilizado.**", "",
              f"`{fichero}` contiene {asientos} asientos ({asientos * 2} apuntes), "
              "generados a partir de los extractos bancarios del periodo. La contrapartida "
              "de cada movimiento se ha deducido del diario contable del ejercicio anterior "
              "del propio cliente: no se ha aplicado ningún criterio genérico.", ""]
    lineas += seccion_pasos(clasificados, cuentas, verificacion)
    lineas += seccion_cuadre(clasificados, cuentas, saldos_hist, saldos_final)
    lineas += seccion_verificacion(verificacion)
    lineas += seccion_contenido(clasificados, cuentas, asientos)
    lineas += seccion_por_regla(clasificados)
    lineas += seccion_puente(clasificados, cuentas)
    lineas += seccion_revisar(clasificados, cuentas)
    lineas += seccion_traspasos(clasificados)
    lineas += seccion_tarjeta(clasificados)
    lineas += ["## Decisiones de criterio pendientes", ""]
    lineas += [f"- {d}" for d in DECISIONES] + [""]
    lineas += ["## Cómo se ha hecho el trabajo", ""]
    lineas += [f"- {d}" for d in COMO_SE_HA_HECHO] + [""]
    return "\n".join(lineas).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clasificado", required=True, type=Path)
    ap.add_argument("--cuentas", type=Path)
    ap.add_argument("--diccionario", type=Path)
    ap.add_argument("--extractos", type=Path)
    ap.add_argument("--verificacion", type=Path)
    ap.add_argument("--salida", required=True, type=Path,
                    help="README.md que acompaña al DBF")
    ap.add_argument("--titulo", default="XDIARIO para importar en ContaPlus")
    ap.add_argument("--fichero", default="XDIARIO.DBF",
                    help="nombre del DBF al que acompaña este README")
    args = ap.parse_args()

    def cargar(ruta, defecto):
        if ruta and ruta.exists():
            return json.loads(ruta.read_text(encoding="utf-8"))
        return defecto

    clasificados = json.loads(args.clasificado.read_text(encoding="utf-8"))
    cuentas = cargar(args.cuentas, {})
    verificacion = cargar(args.verificacion, {})
    saldos_hist = {k: float(v)
                   for k, v in cargar(args.diccionario, {}).get("bancos", {}).items()}

    saldos_final = {}
    mapa = cuentas.get("bancos", {})
    for e in cargar(args.extractos, []):
        subcuenta = mapa.get(e.get("banco"))
        if subcuenta and e.get("saldo_final") is not None:
            saldos_final[subcuenta] = float(e["saldo_final"])

    asientos = len(vivos_de(clasificados))
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(
        readme(clasificados, cuentas, verificacion, saldos_hist, saldos_final,
               asientos, args.titulo, args.fichero), encoding="utf-8")

    puente = cuentas.get("puente", PUENTE_POR_DEFECTO)
    en_puente = sum(1 for c in vivos_de(clasificados) if c["contrapartida"] == puente)
    print(f"README de revisión: {args.salida}")
    print(f"  {asientos} asientos · {en_puente} movimientos en la cuenta puente")
    print("\nSe entregan dos ficheros: el DBF y este README. "
          "El fichero no está contabilizado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
