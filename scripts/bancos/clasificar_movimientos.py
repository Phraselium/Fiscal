#!/usr/bin/env python3
"""Asigna a cada movimiento bancario su contrapartida contable.

Las reglas se aplican EN ORDEN y gana la primera que case. Cada una devuelve la
subcuenta de contrapartida, un concepto de 25 caracteres, el nombre de la regla y
si el movimiento hay que revisarlo a mano.

Regla de prudencia: lo que no tenga respaldo en el historico del cliente va a la
cuenta puente. Es mejor entregar 300 movimientos en la 555 que 300 mal imputados.

Los traspasos entre cuentas propias se resuelven en una PASADA GLOBAL al final,
nunca movimiento a movimiento: si no, se duplican o se pierden apuntes y los
bancos dejan de cuadrar.

Uso
---
    python3 scripts/bancos/clasificar_movimientos.py \\
        --movimientos movimientos.json --diccionario dicc.json \\
        --cuentas cuentas.json --salida clasificado.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diccionario_diario import Diccionario, sin_acentos  # noqa: E402

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
         "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

# Patrones para sacar el nombre del tercero del texto del extracto.
PATRONES_TERCERO = [
    re.compile(r"TRANSFERENCIA\s+INMEDIATA\s+A\s+FAVOR\s+DE\s+(.+)"),
    re.compile(r"TRANSFERENCIA\s+OTRA\s+ENTIDAD.*?BENEF[:.]?\s*(.+)"),
    re.compile(r"ABONO\s+TRANSFERENCIA\s+DE\s+(.+)"),
    re.compile(r"TRANSFERENCIAS?\s+A\s+(.+)"),
    re.compile(r"TRANSFERENCIAS?\s+(.+)"),
    re.compile(r"PAGO\s+PUNTUAL\s+RECIBO\s+DE\s+(.+)"),
    re.compile(r"ADEUDO\s+RECIBO\s+(.+)"),
    re.compile(r"RECIBO\s+(.+?)(?:\s+N[ºO°]\s*RECIBO.*)?$"),
    re.compile(r"COMPRA\s+TARJ\.?\s*[\d*]*\s+(.+?)(?:,.*)?$"),
    re.compile(r"PAGO\s+MOVIL\s+EN\s+(.+?)(?:,.*)?$"),
    re.compile(r"COMPRA\s+(.+?)(?:,.*)?$"),
    re.compile(r"ELECTRICIDAD\s+(.+?)(?:\s*-.*)?$"),
]

R = {  # patrones de deteccion, compilados una vez
    "tpv_abono": re.compile(r"(ABONO\s+TPV|LIQUIDACION\s+REMESA\s+DE\s+COMERCIOS|FACT\.?TPV)"),
    "tpv_comision": re.compile(r"(COMISIONES?\s+\d{6,}|COMI\.?TPV)"),
    "comision": re.compile(r"(COMISION|COMIS\.|GASTOS?\s+(?:DE\s+)?(?:ADMIN|MANTENIM|CORREO)|"
                           r"LIQUIDACION\s+(?:DE\s+)?CONTRATO|GESTION\s+DE\s+DEVOLUC|"
                           r"CUOTA\s+(?:DE\s+)?MANTENIM|CUSTODIA)"),
    "retrocesion": re.compile(r"RETROCESION"),
    "intereses": re.compile(r"(LIQUIDACION\s+DE\s+INTERESES|INTERESES\s+(?:A\s+FAVOR|DEUDORES|"
                            r"ACREEDORES)|ABONO\s+INTERESES)"),
    "tgss": re.compile(r"(TGSS|SEGUROS?\s+SOCIALES?|TESORERIA\s+GENERAL|"
                       r"TESORERIA\s+DE\s+LA\s+SEGURIDAD\s+SOCIAL|SEG\.?\s?SOC)"),
    "autonomos": re.compile(r"(AUTONOMO|RETA|CUOTA\s+AUTONOM)"),
    "nomina": re.compile(r"(NOMINA|FINIQUITO|ADELANTO\s+NOMINA|PAGO\s+DE\s+NOMINAS)"),
    "efectivo": re.compile(r"(INGRESO\s+(?:DE\s+)?EFECTIVO|RETIRADA\s+(?:DE\s+)?EFECTIVO|"
                           r"CAJERO|REINTEGRO|DEPOSITO\s+AUDITADO|INGRESO\s+EN\s+EFECTIVO)"),
    "traspaso": re.compile(r"(TRASPASO|TRANSFERENCIA\s+ENTRE\s+CUENTAS|"
                           r"TRASPASO\s+ENTRE\s+CUENTAS)"),
    "ayuntamiento": re.compile(r"(AYUNTAMIENTO|AYTO|TASAS?\s+MUNICIPAL|"
                               r"ORGANISMO\s+AUTONOMO\s+MUNICIPAL|SUMA\s+GESTION)"),
    "combustible": re.compile(r"(ESTACION\s+(?:DE\s+)?SERVICIO|E\.?S\.?\s+|GASOLINERA|"
                              r"REPSOL|CEPSA|GALP|BP\s|SHELL|PETROPRIX|BALLENOIL)"),
    "valores": re.compile(r"(BROKER|CUSTODIA\s+(?:DE\s+)?VALORES|CUPON|DIVIDENDO|"
                          r"SUSCRIPCION\s+(?:DE\s+)?FONDO|VALORES)"),
    "tarjeta": re.compile(r"(COMPRA\s+TARJ|PAGO\s+MOVIL|COMPRA\s+EN\s|TARJETA)"),
}

# Impuestos: texto del extracto → modelo. El orden importa.
IMPUESTOS = [
    (re.compile(r"\b(MOD(?:ELO)?\.?\s*111|RETENCION(?:ES)?\s+(?:DE\s+)?TRABAJO)\b"), "111"),
    (re.compile(r"\b(MOD(?:ELO)?\.?\s*115|RETENCION(?:ES)?\s+(?:DE\s+)?ARRENDAM)\b"), "115"),
    (re.compile(r"\b(MOD(?:ELO)?\.?\s*123|RETENCION(?:ES)?\s+(?:DE\s+)?CAPITAL)\b"), "123"),
    (re.compile(r"\b(MOD(?:ELO)?\.?\s*303|IVA\s+(?:TRIMESTRAL|MENSUAL)?)\b"), "303"),
    (re.compile(r"\b(MOD(?:ELO)?\.?\s*202|PAGO\s+FRACCIONADO)\b"), "202"),
    (re.compile(r"\b(MOD(?:ELO)?\.?\s*200|IMPUESTO\s+(?:SOBRE\s+)?SOCIEDADES)\b"), "200"),
    (re.compile(r"\b(AEAT|AGENCIA\s+TRIBUTARIA|HACIENDA\s+PUBLICA)\b"), ""),
]


@dataclass
class Cuentas:
    """Las subcuentas que usa el mapeo. Se piden al usuario o salen del historico."""
    bancos: dict[str, str] = field(default_factory=dict)   # nombre de banco → subcuenta 572*
    puente: str = "5550000"
    caja: str = "5700000"
    servicios_bancarios: str = "6260000"
    gastos_financieros: str = "6620000"
    ingresos_financieros: str = "7690000"
    seguridad_social: str = "4760000"
    autonomos: str = "4760001"
    remuneraciones: str = "4650000"
    tributos: str = "6310000"
    socios: str = "5510000"
    hp_acreedora: str = "4750000"       # se completa con el modelo: 4751000, 4753000…
    modelos: dict[str, str] = field(default_factory=dict)

    @classmethod
    def desde_json(cls, ruta: Path) -> "Cuentas":
        d = json.loads(Path(ruta).read_text(encoding="utf-8"))
        base = cls()
        for k, v in d.items():
            if hasattr(base, k):
                setattr(base, k, v)
        return base

    def del_modelo(self, modelo: str) -> str:
        if modelo in self.modelos:
            return self.modelos[modelo]
        return {"111": "4751000", "115": "4751500", "123": "4751200",
                "303": "4770000", "200": "4752000", "202": "4730000"}.get(
                    modelo, self.hp_acreedora)


@dataclass
class Clasificado:
    banco: str
    fecha: date
    texto: str
    importe: float
    subcuenta_banco: str
    contrapartida: str
    concepto: str
    regla: str
    revisar: bool = False
    motivo_revision: str = ""
    contabilizado_en_otro: bool = False   # traspaso ya recogido por su pareja
    fichero: str = ""
    fila: int = 0

    def como_dict(self) -> dict:
        d = asdict(self)
        d["fecha"] = self.fecha.isoformat()
        return d


def recortar(texto: str, largo: int = 25) -> str:
    return sin_acentos(texto)[:largo].strip()


def mes_de(fecha: date) -> str:
    """Periodo de una liquidacion que se paga al mes siguiente."""
    mes = fecha.month - 1 or 12
    ano = fecha.year if fecha.month > 1 else fecha.year - 1
    return f"{MESES[mes - 1][:3]}/{ano % 100:02d}"


def extraer_tercero(texto: str) -> str:
    for patron in PATRONES_TERCERO:
        m = patron.search(texto)
        if m:
            nombre = m.group(1).strip(" .,-")
            nombre = re.sub(r"\s+N[ºO°]?\s*(RECIBO|FACTURA|MANDATO).*$", "", nombre)
            nombre = re.sub(r"\s{2,}", " ", nombre)
            if len(nombre) >= 3:
                return nombre
    return texto


def nombre_empleado(texto: str, empleados: set[str]) -> str | None:
    palabras = set(re.findall(r"[A-ZÑÇ]{4,}", sin_acentos(texto)))
    coincidencias = palabras & empleados
    return sorted(coincidencias)[0] if coincidencias else None


def clasificar_uno(mov, cuentas: Cuentas, dicc: Diccionario,
                   socios: set[str], comercios: dict[str, str]) -> Clasificado:
    texto = sin_acentos(mov["texto"] if isinstance(mov, dict) else mov.texto)
    importe = mov["importe"] if isinstance(mov, dict) else mov.importe
    banco = mov["banco"] if isinstance(mov, dict) else mov.banco
    fecha = mov["fecha"] if isinstance(mov, dict) else mov.fecha
    if isinstance(fecha, str):
        fecha = datetime.fromisoformat(fecha).date()
    subcta_banco = cuentas.bancos.get(banco, cuentas.puente)

    def salida(contra, concepto, regla, revisar=False, motivo=""):
        return Clasificado(
            banco=banco, fecha=fecha, texto=texto, importe=importe,
            subcuenta_banco=subcta_banco, contrapartida=contra,
            concepto=recortar(concepto), regla=regla, revisar=revisar,
            motivo_revision=motivo,
            fichero=(mov.get("fichero", "") if isinstance(mov, dict) else mov.fichero),
            fila=(mov.get("fila", 0) if isinstance(mov, dict) else mov.fila))

    # 1 · Abono de remesa de TPV
    if R["tpv_abono"].search(texto):
        return salida(cuentas.caja, "ABONO REMESA TPV", "1-tpv-abono")

    # 2 · Comision de TPV
    if R["tpv_comision"].search(texto):
        return salida(cuentas.servicios_bancarios, "COMIS VAR REMESAS", "2-tpv-comision")

    # 3 · Comisiones y gastos bancarios.
    # Si el texto es una liquidacion de intereses, manda la regla 5 aunque mencione
    # comisiones: «LIQUIDACION DE INTERESES Y COMISIONES» es lo que escriben los bancos.
    if R["comision"].search(texto) and not R["intereses"].search(texto):
        return salida(cuentas.servicios_bancarios, "COMIS VARIAS", "3-comisiones")

    # 4 · Retrocesion
    if R["retrocesion"].search(texto):
        return salida(cuentas.servicios_bancarios, "RETROC COMISIONES", "4-retrocesion")

    # 5 · Intereses
    if R["intereses"].search(texto):
        cuenta = cuentas.ingresos_financieros if importe > 0 else cuentas.gastos_financieros
        return salida(cuenta, "ABONO INTERESES", "5-intereses")

    # 6 · Seguridad Social
    if R["tgss"].search(texto):
        cuenta = cuentas.autonomos if R["autonomos"].search(texto) else cuentas.seguridad_social
        return salida(cuenta, f"P/SEG.SOC.{mes_de(fecha)}", "6-seguridad-social",
                      revisar=True, motivo="periodo de la liquidación deducido de la fecha")

    # 7 · Nominas
    if R["nomina"].search(texto):
        quien = nombre_empleado(texto, dicc.empleados) or ""
        return salida(cuentas.remuneraciones,
                      f"P/NOMINAS MES {quien}".strip(), "7-nominas")

    # 8 · Efectivo
    if R["efectivo"].search(texto):
        concepto = "TRASP DE CJA" if importe > 0 else "TRASP A CJA"
        return salida(cuentas.caja, concepto, "8-efectivo")

    # 9 · Socios
    if socios and (quien := nombre_empleado(texto, socios)):
        return salida(cuentas.socios, f"P/S.CTA.SOCIO {quien}", "9-socios",
                      revisar=True, motivo="movimiento con socio")

    # 10 · Traspaso entre cuentas propias: se resuelve en la pasada global
    if R["traspaso"].search(texto):
        return salida(cuentas.puente, "TRASPASO BANCOS", "10-traspaso-pendiente")

    # 11 · Impuestos
    for patron, modelo in IMPUESTOS:
        if patron.search(texto):
            if not modelo:
                return salida(cuentas.hp_acreedora, "P/AEAT", "11-impuesto-sin-modelo",
                              revisar=True, motivo="AEAT sin modelo identificable")
            return salida(cuentas.del_modelo(modelo), f"P/MOD {modelo}", "11-impuesto")

    # 12 · Ayuntamiento
    if R["ayuntamiento"].search(texto):
        return salida(cuentas.tributos, "P/REC.AYUNTAMIENTO", "12-ayuntamiento")

    # 13 · Combustible
    if R["combustible"].search(texto):
        cuenta, aprox = dicc.buscar_tercero(texto)
        if cuenta:
            return salida(cuenta, "P/S.FRA.COMBUSTIBLE", "13-combustible", revisar=aprox,
                          motivo="coincidencia aproximada" if aprox else "")
        return salida(cuentas.puente, "P/S.FRA.COMBUSTIBLE", "13-combustible-sin-cuenta",
                      revisar=True, motivo="combustible sin cuenta en el histórico")

    # 14 · Valores e inversiones
    if R["valores"].search(texto):
        cuenta, aprox = dicc.buscar_tercero(texto)
        if cuenta:
            return salida(cuenta, recortar(texto), "14-valores", revisar=True,
                          motivo="operación de valores: confirmar tratamiento")
        return salida(cuentas.puente, recortar(texto), "14-valores-sin-cuenta",
                      revisar=True, motivo="operación de valores sin cuenta")

    tercero = extraer_tercero(texto)

    # 15 bis · Tarjeta: solo si el comercio esta en la lista blanca validada
    if R["tarjeta"].search(texto):
        clave = sin_acentos(tercero)[:30]
        for comercio, cuenta in comercios.items():
            if comercio and comercio in clave:
                return salida(cuenta, f"P/S.FRA.{tercero}"[:25], "15-tarjeta-lista-blanca",
                              revisar=True, motivo="compra con tarjeta imputada a proveedor")
        return salida(cuentas.puente, recortar(texto), "15-tarjeta-no-validada",
                      revisar=True,
                      motivo="compra con tarjeta: comercio no validado por el usuario")

    # 15 · Proveedor del diccionario
    cuenta, aprox = dicc.buscar_tercero(tercero)
    if cuenta:
        motivo = "coincidencia aproximada" if aprox else ""
        revisar = aprox
        if importe > 0:
            revisar = True
            motivo = "cobro contra cuenta de proveedor: ¿rappel, devolución u otro cliente?"
        return salida(cuenta, f"P/S.FRA.{tercero}"[:25], "15-proveedor", revisar, motivo)

    # 16 · Transferencia a nombre de un empleado conocido
    if (quien := nombre_empleado(tercero, dicc.empleados)):
        return salida(cuentas.remuneraciones, f"P/NOMINAS MES {quien}", "16-empleado",
                      revisar=True, motivo="reconocido solo por nombre de pila")

    # 17 · Sin identificar
    return salida(cuentas.puente, recortar(texto), "17-sin-identificar",
                  revisar=True, motivo="sin respaldo en el histórico")


def resolver_traspasos(movimientos: list[Clasificado], cuentas: Cuentas,
                       dias: int = 5) -> int:
    """Pasada GLOBAL: empareja cargo y abono de un traspaso entre cuentas propias.

    Genera un solo asiento, el del lado del pago, con la otra cuenta bancaria como
    contrapartida. El otro movimiento se marca como ya contabilizado y queda fuera
    del fichero, pero se recoge en el informe.
    """
    pendientes = [m for m in movimientos if m.regla == "10-traspaso-pendiente"]
    emparejados = 0
    usados: set[int] = set()

    for i, uno in enumerate(pendientes):
        if id(uno) in usados or uno.importe >= 0:
            continue
        for otro in pendientes:
            if id(otro) in usados or otro is uno or otro.importe <= 0:
                continue
            if otro.subcuenta_banco == uno.subcuenta_banco:
                continue
            if abs(otro.importe + uno.importe) > 0.005:
                continue
            if abs((otro.fecha - uno.fecha).days) > dias:
                continue
            # El asiento se hace por el lado del pago.
            uno.contrapartida = otro.subcuenta_banco
            uno.regla = "10-traspaso"
            uno.revisar = False
            uno.motivo_revision = ""
            otro.contabilizado_en_otro = True
            otro.contrapartida = uno.subcuenta_banco
            otro.regla = "10-traspaso-pareja"
            usados.update({id(uno), id(otro)})
            emparejados += 1
            break

    for m in pendientes:
        if id(m) not in usados:
            m.contrapartida = cuentas.puente
            m.regla = "10-traspaso-sin-pareja"
            m.revisar = True
            m.motivo_revision = ("traspaso sin pareja: la contrapartida puede caer en el "
                                 "periodo siguiente")
    return emparejados


def clasificar(movimientos: list, cuentas: Cuentas, dicc: Diccionario,
               socios: set[str] | None = None,
               comercios: dict[str, str] | None = None) -> list[Clasificado]:
    salida = [clasificar_uno(m, cuentas, dicc, socios or set(), comercios or {})
              for m in movimientos]
    resolver_traspasos(salida, cuentas)
    return salida


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--movimientos", required=True, type=Path)
    ap.add_argument("--diccionario", required=True, type=Path)
    ap.add_argument("--cuentas", type=Path, help="JSON con las subcuentas a usar")
    ap.add_argument("--socios", default="", help="Apellidos de socios, separados por coma")
    ap.add_argument("--comercios", type=Path, help="Lista blanca comercio→subcuenta")
    ap.add_argument("--salida", required=True, type=Path)
    args = ap.parse_args()

    bruto = json.loads(args.movimientos.read_text(encoding="utf-8"))
    movimientos = []
    for extracto in (bruto if isinstance(bruto, list) else [bruto]):
        movimientos.extend(extracto.get("movimientos", []) if isinstance(extracto, dict)
                           else [])
    if not movimientos:
        movimientos = bruto if isinstance(bruto, list) else []

    dicc = Diccionario.desde_dict(json.loads(args.diccionario.read_text(encoding="utf-8")))
    cuentas = Cuentas.desde_json(args.cuentas) if args.cuentas else Cuentas()
    socios = {sin_acentos(s) for s in args.socios.split(",") if s.strip()}
    comercios = (json.loads(args.comercios.read_text(encoding="utf-8"))
                 if args.comercios else {})

    resultado = clasificar(movimientos, cuentas, dicc, socios, comercios)

    a_contabilizar = [c for c in resultado if not c.contabilizado_en_otro]
    en_puente = [c for c in a_contabilizar if c.contrapartida == cuentas.puente]
    a_revisar = [c for c in a_contabilizar if c.revisar]

    print(f"{len(resultado)} movimientos · {len(a_contabilizar)} generan asiento\n")
    from collections import Counter
    for regla, n in Counter(c.regla for c in resultado).most_common():
        print(f"  {n:5}  {regla}")

    pct = len(en_puente) / len(a_contabilizar) * 100 if a_contabilizar else 0
    print(f"\n  En cuenta puente {cuentas.puente}: {len(en_puente)} ({pct:.1f} % del total)")
    print(f"  Marcados para revisar:        {len(a_revisar)}")

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(json.dumps([c.como_dict() for c in resultado],
                                      ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nEscrito {args.salida}")
    print("Nada está contabilizado: queda pendiente de revisar e importar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
