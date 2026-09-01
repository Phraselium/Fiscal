#!/usr/bin/env python3
"""Pruebas de la skill bancos-a-contaplus, con datos ficticios de principio a fin.

El caso monta cuatro extractos con formatos distintos, un diario historico
pequeno y un fichero muestra, y recorre el flujo entero hasta el DBF y su
verificacion.

Trampas incluidas a proposito:
  · un traspaso entre cuentas propias (no puede duplicar apuntes)
  · una cuenta bancaria nueva que no esta en el historico
  · un movimiento de importe cero (no genera asiento)
  · un comercio que solo casa por el nombre del municipio (debe ir a la puente)

    python3 tests/test_bancos_contaplus.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "scripts" / "bancos"))

from lib_dbf import crear_estructura, escribir, leer, leer_estructura  # noqa: E402
import diccionario_diario as dd  # noqa: E402
import clasificar_movimientos as cm  # noqa: E402
import generar_xdiario as gx  # noqa: E402
import verificar_xdiario as vx  # noqa: E402
import leer_extractos as le  # noqa: E402
import informe_revision as ir  # noqa: E402

CAMPOS = [
    ("ASIEN", "N", 6, 0), ("FECHA", "D", 8, 0), ("SUBCTA", "C", 12, 0),
    ("CONTRA", "C", 12, 0), ("CONCEPTO", "C", 25, 0),
    ("EURODEBE", "N", 16, 2), ("EUROHABER", "N", 16, 2),
    ("PTADEBE", "N", 16, 2), ("PTAHABER", "N", 16, 2),
    ("MONEDAUSO", "C", 1, 0), ("NIC", "C", 1, 0), ("FACTURA", "N", 8, 0),
    ("BASEIMPO", "N", 16, 2), ("IVA", "N", 5, 2), ("DOCUMENTO", "C", 10, 0),
]

BANCO_A = "5720001"      # Banco Uno, en el historico
BANCO_B = "5720002"      # Banco Dos, en el historico
BANCO_NUEVO = "5720003"  # cuenta nueva: no aparece en el historico
PUENTE = "5550000"


def apunte(asien, fecha, subcta, contra, concepto, debe=0.0, haber=0.0):
    return {"ASIEN": asien, "FECHA": fecha, "SUBCTA": subcta, "CONTRA": contra,
            "CONCEPTO": concepto, "EURODEBE": debe, "EUROHABER": haber,
            "PTADEBE": 0, "PTAHABER": 0, "MONEDAUSO": "2", "NIC": "E",
            "FACTURA": 0, "BASEIMPO": 0, "IVA": 0, "DOCUMENTO": ""}


def historico() -> list[dict]:
    """Diario del ejercicio anterior. Nombres inventados."""
    f = date(2025, 6, 10)
    filas = []
    # Asiento de apertura: debe descartarse para los saldos y los criterios.
    filas += [apunte(1, date(2025, 1, 1), BANCO_A, "", "ASIENTO DE APERTURA", 5000.00, 0),
              apunte(1, date(2025, 1, 1), "1000000", "", "ASIENTO DE APERTURA", 0, 5000.00)]

    # Pagos a proveedores. El CONTRA va vacio a proposito: hay que emparejar por importe.
    proveedores = [
        ("4000010", "P/S.FRA.NORTE MAQUINARIA", 1210.00),
        ("4000011", "P/S.FRA.ELECTRICA DEL SUR", 342.50),
        ("4000012", "P/S.FRA.PANADERIA LA ESPIGA", 88.20),
        ("4100005", "P/S.FRA.ASEGURADORA GENERAL", 450.00),
    ]
    n = 2
    for cuenta, concepto, importe in proveedores:
        # Se repiten dos veces para que el token supere el minimo de apariciones.
        for _ in range(2):
            filas += [apunte(n, f, cuenta, "", concepto, importe, 0),
                      apunte(n, f, BANCO_A, "", concepto, 0, importe)]
            n += 1

    filas += [apunte(n, f, "4650000", "", "P/NOMINAS MES GARCIA", 1500.00, 0),
              apunte(n, f, BANCO_A, "", "P/NOMINAS MES GARCIA", 0, 1500.00)]
    n += 1
    filas += [apunte(n, f, "4650000", "", "P/NOMINAS MES MARTINEZ", 1400.00, 0),
              apunte(n, f, BANCO_A, "", "P/NOMINAS MES MARTINEZ", 0, 1400.00)]
    n += 1
    filas += [apunte(n, f, "6260000", "", "COMIS VARIAS", 12.00, 0),
              apunte(n, f, BANCO_B, "", "COMIS VARIAS", 0, 12.00)]
    n += 1
    # Un cobro para que el Banco Dos tenga saldo.
    filas += [apunte(n, f, BANCO_B, "", "COBRO CLIENTE", 3000.00, 0),
              apunte(n, f, "4300001", "", "COBRO CLIENTE", 0, 3000.00)]
    return filas


def saldo_de(filas, cuenta) -> float:
    return round(sum(l["EURODEBE"] - l["EUROHABER"] for l in filas
                     if l["SUBCTA"] == cuenta and "APERTURA" not in l["CONCEPTO"]), 2)


class TestBancosAContaplus(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        cls.estructura = crear_estructura(CAMPOS)
        cls.filas_hist = historico()

        cls.xdiario_ant = cls.dir / "XDIARIO_2025.DBF"
        escribir(cls.xdiario_ant, cls.estructura, cls.filas_hist)

        # El fichero muestra tiene la MISMA estructura, sin registros.
        cls.muestra = cls.dir / "MUESTRA.DBF"
        escribir(cls.muestra, cls.estructura, [])

        cls.dicc = dd.construir(cls.xdiario_ant)

        cls.cuentas = cm.Cuentas(
            bancos={"BancoUno": BANCO_A, "BancoDos": BANCO_B, "BancoNuevo": BANCO_NUEVO},
            puente=PUENTE)

        cls.movimientos = cls._movimientos()
        cls.clasificados = cm.clasificar(cls.movimientos, cls.cuentas, cls.dicc,
                                         socios=set(), comercios={})

        cls.salida = cls.dir / "XDIARIO.DBF"
        registros, cls.ceros = gx.construir_asientos(
            [c.como_dict() for c in cls.clasificados], cls.estructura,
            asiento_inicial=1, longitud_subcuenta=7)
        escribir(cls.salida, cls.estructura, registros)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @staticmethod
    def _movimientos() -> list[dict]:
        def m(banco, dia, texto, importe, fila):
            return {"banco": banco, "fecha": date(2026, 3, dia).isoformat(),
                    "texto": texto, "importe": importe, "fichero": f"{banco}.xlsx",
                    "fila": fila}
        return [
            m("BancoUno", 2, "ADEUDO RECIBO ELECTRICA DEL SUR SL", -342.50, 10),
            m("BancoUno", 3, "TRANSFERENCIA A NORTE MAQUINARIA SL", -1210.00, 11),
            m("BancoUno", 4, "RECIBO ASEGURADORA GENERAL Nº RECIBO 000447112", -450.00, 12),
            m("BancoUno", 5, "TRANSFERENCIA A NOMINA MES MARZO GARCIA", -1500.00, 13),
            m("BancoUno", 6, "LIQUIDACION REMESA DE COMERCIOS 0012345", 2400.00, 14),
            m("BancoUno", 7, "COMISIONES 0012345 REMESA", -18.00, 15),
            # Comercio que solo casa por el municipio: debe acabar en la puente.
            m("BancoUno", 8, "COMPRA TARJ. 5402 FERRETERIA VALENCIA, VALENCIA", -75.30, 16),
            # Importe cero: no genera asiento.
            m("BancoUno", 9, "APUNTE INFORMATIVO SIN IMPORTE", 0.00, 17),
            # Traspaso entre cuentas propias: cargo aqui, abono en BancoDos.
            m("BancoUno", 10, "TRASPASO A CUENTA PROPIA", -800.00, 18),
            m("BancoDos", 10, "TRASPASO DESDE CUENTA PROPIA", 800.00, 20),
            m("BancoDos", 11, "LIQUIDACION DE INTERESES Y COMISIONES", -12.00, 21),
            m("BancoDos", 12, "PAGO MODELO 303 AEAT", -1300.00, 22),
            m("BancoNuevo", 15, "INGRESO EFECTIVO EN CAJERO", 500.00, 30),
        ]

    # --- El diccionario deducido del historico ---------------------------

    def test_deduce_la_longitud_de_subcuenta_del_plan(self):
        self.assertEqual(self.dicc.longitud_subcuenta, 7)

    def test_descarta_el_asiento_de_apertura_al_calcular_saldos(self):
        self.assertEqual(self.dicc.bancos[BANCO_A], saldo_de(self.filas_hist, BANCO_A))
        self.assertNotIn(BANCO_NUEVO, self.dicc.bancos, "la cuenta nueva no está en el histórico")

    def test_empareja_concepto_con_contrapartida_por_importe(self):
        """El campo CONTRA va vacío: el criterio sale del importe contrario."""
        self.assertEqual(
            self.dicc.concepto_a_contrapartida.get("P/S.FRA.ELECTRICA DEL SUR"), "4000011")

    def test_identifica_terceros_por_sus_palabras(self):
        self.assertEqual(self.dicc.token_a_subcuenta.get("ELECTRICA"), "4000011")
        self.assertEqual(self.dicc.token_a_subcuenta.get("ASEGURADORA"), "4100005")

    def test_descarta_municipios_y_genericos_como_tokens(self):
        for parada in ("VALENCIA", "DISTRIBUCIONES", "GRUPO", "CENTRO"):
            self.assertNotIn(parada, self.dicc.token_a_subcuenta,
                             f"'{parada}' no identifica a ningún tercero")

    def test_reconoce_conceptos_truncados_a_25_caracteres(self):
        """«P/S.FRA.INDUSTRIAS DEL METAL» se guarda truncado como «...INDUST».

        Sin la pasada por prefijo ese proveedor no se reconocería nunca. La
        coincidencia es aproximada, así que el movimiento se marca para revisar.
        """
        d = dd.Diccionario()
        d.token_a_subcuenta = {"INDUST": "4000020"}
        cuenta, aproximada = d.buscar_tercero("INDUSTRIAS DEL METAL SL")
        self.assertEqual(cuenta, "4000020")
        self.assertTrue(aproximada, "por prefijo es aproximada: hay que revisarla")

    def test_el_prefijo_exige_al_menos_cinco_letras(self):
        """Un prefijo corto casaría con demasiadas cosas."""
        d = dd.Diccionario()
        d.token_a_subcuenta = {"NORT": "4000010"}
        self.assertEqual(d.buscar_tercero("NORTEAMERICANA SL")[0], None)

    def test_las_palabras_genericas_no_identifican_a_nadie(self):
        """GENERAL, SERVICIOS o DISTRIBUCIONES casarían con media cartera."""
        d = dd.Diccionario()
        d.token_a_subcuenta = {"ASEGURADORA": "4100005"}
        self.assertEqual(dd.tokens("SERVICIOS GENERALES DEL SUR SL"), [],
                         "solo palabras genéricas: no hay nada que identificar")

    def test_saca_los_empleados_de_las_nominas(self):
        self.assertIn("GARCIA", self.dicc.empleados)
        self.assertIn("MARTINEZ", self.dicc.empleados)

    # --- Clasificacion ----------------------------------------------------

    def _por_fila(self, fila: int) -> cm.Clasificado:
        return next(c for c in self.clasificados if c.fila == fila)

    def test_reglas_prioritarias(self):
        casos = {10: ("4000011", "15-proveedor"),
                 11: ("4000010", "15-proveedor"),
                 12: ("4100005", "15-proveedor"),
                 13: ("4650000", "7-nominas"),
                 14: (self.cuentas.caja, "1-tpv-abono"),
                 15: (self.cuentas.servicios_bancarios, "2-tpv-comision"),
                 21: (self.cuentas.gastos_financieros, "5-intereses"),
                 22: (self.cuentas.del_modelo("303"), "11-impuesto")}
        for fila, (cuenta, regla) in casos.items():
            c = self._por_fila(fila)
            with self.subTest(fila=fila, texto=c.texto[:40]):
                self.assertEqual(c.contrapartida, cuenta)
                self.assertEqual(c.regla, regla)

    def test_el_comercio_que_solo_casa_por_municipio_va_a_la_puente(self):
        c = self._por_fila(16)
        self.assertEqual(c.contrapartida, PUENTE)
        self.assertTrue(c.revisar)

    def test_el_traspaso_genera_un_solo_asiento(self):
        pago = self._por_fila(18)
        cobro = self._por_fila(20)
        self.assertEqual(pago.regla, "10-traspaso")
        self.assertEqual(pago.contrapartida, BANCO_B, "la contrapartida es el otro banco")
        self.assertTrue(cobro.contabilizado_en_otro, "el otro lado no genera asiento")

    def test_el_ingreso_en_cajero_va_a_caja(self):
        self.assertEqual(self._por_fila(30).contrapartida, self.cuentas.caja)

    def test_conceptos_de_25_caracteres_o_menos(self):
        for c in self.clasificados:
            self.assertLessEqual(len(c.concepto), 25, c.concepto)

    # --- El fichero generado ---------------------------------------------

    def test_el_importe_cero_no_genera_asiento(self):
        self.assertEqual(len(self.ceros), 1)
        self.assertEqual(self.ceros[0]["fila"], 17)

    def test_numero_de_asientos(self):
        """13 movimientos − 1 de importe cero − 1 lado de traspaso = 11 asientos."""
        registros = list(leer(self.salida))
        self.assertEqual(len(registros), 22)
        self.assertEqual(len({r["ASIEN"] for r in registros}), 11)

    def test_las_subcuentas_se_ajustan_a_la_longitud_del_plan(self):
        for r in leer(self.salida):
            self.assertEqual(len(str(r["SUBCTA"]).strip()), 7)

    def test_signo_del_extracto_a_debe_o_haber(self):
        """Cargo: contrapartida al debe, banco al haber. Abono: al revés."""
        registros = list(leer(self.salida))
        pago = [r for r in registros if r["CONCEPTO"].startswith("P/S.FRA.ELECTRICA")]
        debe = next(r for r in pago if r["EURODEBE"] > 0)
        haber = next(r for r in pago if r["EUROHABER"] > 0)
        self.assertEqual(debe["SUBCTA"], "4000011")
        self.assertEqual(haber["SUBCTA"], BANCO_A)

    # --- Las diez verificaciones del paso 9 -------------------------------

    def _informe(self):
        # El saldo final del extracto incluye TODOS los movimientos de esa cuenta,
        # incluido el lado del traspaso que no genera asiento propio: el dinero se
        # movió igual, y el asiento del otro lado ya lo recoge por su contrapartida.
        def final(cuenta):
            return round(self.dicc.bancos.get(cuenta, 0.0)
                         + sum(c.importe for c in self.clasificados
                               if c.subcuenta_banco == cuenta), 2)
        saldos_final = {BANCO_A: final(BANCO_A), BANCO_B: final(BANCO_B),
                        BANCO_NUEVO: final(BANCO_NUEVO)}
        return vx.verificar(self.salida, self.muestra,
                            {**self.dicc.bancos, BANCO_NUEVO: 0.0}, saldos_final,
                            self.dicc.subcuentas,
                            (date(2026, 1, 1), date(2026, 12, 31)))

    # --- El README que acompaña al DBF ------------------------------------

    def _readme(self) -> str:
        return ir.readme(
            [c.como_dict() for c in self.clasificados],
            {"bancos": {"BancoUno": BANCO_A, "BancoDos": BANCO_B,
                        "BancoNuevo": BANCO_NUEVO},
             "puente": PUENTE},
            self._informe().como_dict(),
            {**self.dicc.bancos, BANCO_NUEVO: 0.0},
            saldos_final={},
            asientos=11, titulo="Cliente de prueba", fichero="XDIARIO.DBF")

    def test_el_readme_avisa_de_que_no_esta_contabilizado(self):
        texto = self._readme()
        self.assertIn("pendiente de revisar e importar", texto)
        self.assertIn("No está contabilizado", texto)

    def test_el_readme_lleva_el_cuadre_descompuesto(self):
        """Sin fórmulas de Excel, el cuadre se tiene que poder rehacer a ojo."""
        texto = self._readme()
        for columna in ("Saldo inicial", "Cargos", "Abonos", "Saldo calculado",
                        "Diferencia"):
            with self.subTest(columna=columna):
                self.assertIn(columna, texto)

    def test_el_readme_nombra_la_cuenta_que_hay_que_dar_de_alta(self):
        cabeza = self._readme().split("## Cuadre por banco")[0]
        self.assertIn(BANCO_NUEVO, cabeza,
                      "la cuenta nueva sale en los pasos previos a importar")

    def test_el_readme_da_el_texto_original_de_lo_que_va_a_la_puente(self):
        seccion = self._readme().split("## Movimientos a revisar")[1]
        self.assertIn("FERRETERIA VALENCIA", seccion,
                      "el texto original permite localizar el movimiento en el banco")

    def test_el_readme_recoge_el_otro_lado_del_traspaso(self):
        texto = self._readme()
        self.assertIn("no generan asiento propio", texto)
        self.assertIn("TRASPASO DESDE CUENTA PROPIA", texto)

    def test_el_readme_dice_el_porcentaje_sin_identificar(self):
        self.assertRegex(self._readme(), r"\d+ \(\d+\.\d % del total\)")

    def test_el_readme_distingue_descuadre_de_saldo_desconocido(self):
        """Que falte el saldo del extracto no es un descuadre: es una comprobación menos."""
        clas = [{"banco": "B", "importe": -100.0, "regla": "17-sin-identificar",
                 "contrapartida": PUENTE, "concepto": "X", "texto": "X",
                 "fecha": "2026-03-01", "subcuenta_banco": BANCO_A}]
        cuentas = {"bancos": {"B": BANCO_A}, "puente": PUENTE}

        sin_saldo = "\n".join(ir.seccion_cuadre(clas, cuentas, {BANCO_A: 500.0}, {}))
        self.assertIn("No se ha podido comprobar el cuadre", sin_saldo)
        self.assertNotIn("La diferencia no es cero", sin_saldo)

        cuadra = "\n".join(ir.seccion_cuadre(clas, cuentas, {BANCO_A: 500.0},
                                             {BANCO_A: 400.0}))
        self.assertIn("La diferencia es cero", cuadra)

        descuadra = "\n".join(ir.seccion_cuadre(clas, cuentas, {BANCO_A: 500.0},
                                                {BANCO_A: 999.0}))
        self.assertIn("La diferencia no es cero", descuadra)
        self.assertIn("No importes el fichero", descuadra)

    def test_los_pasos_previos_concuerdan_en_numero(self):
        """El README lo lee una persona: «Reimputar 1 el movimiento» no se entrega."""
        texto = self._readme()
        for chapuza in ("1 el ", "1 los ", "(s)", "1 subcuentas"):
            with self.subTest(chapuza=chapuza):
                self.assertNotIn(chapuza, texto)

    def test_las_barras_del_texto_no_parten_la_tabla(self):
        fila = ir.tabla(["A", "B"], [["con | barra", "x"]])[2]
        self.assertIn("con \\| barra", fila, "la barra del contenido va escapada")
        # Descontadas las escapadas, solo quedan los tres separadores de dos celdas.
        self.assertEqual(fila.replace("\\|", "").count("|"), 3)

    def test_el_entregable_ya_no_es_excel_ni_correo(self):
        fuente = (RAIZ / "scripts" / "bancos" / "informe_revision.py").read_text(
            encoding="utf-8")
        for rastro in ("openpyxl", "--correo", ".xlsx"):
            with self.subTest(rastro=rastro):
                self.assertNotIn(rastro, fuente)

    def test_las_diez_verificaciones_pasan(self):
        inf = self._informe()
        self.assertTrue(inf.correcto,
                        "fallan: " + "; ".join(f"{t} — {d}" for t, d in inf.fallos))

    def test_cubre_las_diez_comprobaciones(self):
        inf = self._informe()
        for numero in range(1, 11):
            with self.subTest(comprobacion=numero):
                self.assertTrue(any(t.startswith(f"{numero} ") or t.startswith(f"{numero}b")
                                    for t in inf.ok),
                                f"no se ha ejecutado la comprobación {numero}")

    def test_avisa_de_las_cuentas_que_hay_que_dar_de_alta(self):
        inf = self._informe()
        avisos = " ".join(inf.avisos)
        self.assertIn(BANCO_NUEVO, avisos, "la cuenta nueva debe salir para darla de alta")

    def test_detecta_un_descuadre_por_banco(self):
        """El cuadre es la comprobación que de verdad importa: tiene que fallar si falla."""
        inf = vx.verificar(self.salida, self.muestra,
                           {**self.dicc.bancos, BANCO_NUEVO: 0.0},
                           {BANCO_A: 999999.99}, self.dicc.subcuentas, None)
        self.assertFalse(inf.correcto)
        self.assertTrue(any("Cuadre por banco" in t for t, _ in inf.fallos))

    def test_detecta_un_asiento_descuadrado(self):
        malo = self.dir / "MALO.DBF"
        escribir(malo, self.estructura, [
            apunte(1, date(2026, 3, 1), "4000010", BANCO_A, "PRUEBA", 100.00, 0),
            apunte(1, date(2026, 3, 1), BANCO_A, "4000010", "PRUEBA", 0, 90.00)])
        inf = vx.verificar(malo, self.muestra)
        self.assertFalse(inf.correcto)
        self.assertTrue(any("Debe = haber" in t for t, _ in inf.fallos))

    def test_detecta_estructura_distinta_a_la_muestra(self):
        otra = crear_estructura(CAMPOS[:8])
        distinto = self.dir / "OTRA.DBF"
        escribir(distinto, otra, [])
        inf = vx.verificar(distinto, self.muestra)
        self.assertTrue(any("Estructura idéntica" in t for t, _ in inf.fallos))

    # --- Lectura de extractos de cuatro bancos ---------------------------

    def test_localiza_la_cabecera_en_cuatro_formatos(self):
        """Cada banco pone la cabecera en una fila distinta; se busca, no se asume."""
        formatos = {
            "ibercaja": (6, ["Fecha Oper", "Concepto", "Descripción", "Importe", "Saldo"]),
            "bbva": (15, ["F. CONTABLE", "CONCEPTO", "BENEFICIARIO/ORDENANTE", "IMPORTE", "SALDO"]),
            "santander": (7, ["Fecha Operación", "Concepto", "Importe", "Saldo"]),
            "sabadell": (8, ["F. Operativa", "Concepto", "Importe", "Saldo"]),
        }
        for banco, (fila_cab, columnas) in formatos.items():
            with self.subTest(banco=banco):
                rejilla = [["ES9121000418450200051332"] if i == 1 else []
                           for i in range(fila_cab)]
                rejilla.append(columnas)
                rejilla.append(["15/03/2026"] + ["PAGO DE PRUEBA"] * (len(columnas) - 3)
                               + ["-100,50", "1.000,00"])
                numero, mapa = le.localizar_cabecera(rejilla)
                self.assertEqual(numero, fila_cab)
                self.assertTrue({"fecha", "texto", "importe"} <= set(mapa))

    def test_saldo_inicial_se_deduce_del_primer_movimiento(self):
        e = le.Extracto("X", "", "", "x.csv", [
            le.Movimiento("X", "", date(2026, 3, 1), "UNO", -100.0, 900.0, "x.csv", 2),
            le.Movimiento("X", "", date(2026, 3, 2), "DOS", 50.0, 950.0, "x.csv", 3)])
        self.assertEqual(e.saldo_inicial, 1000.0)
        self.assertEqual(e.saldo_final, 950.0)

    # --- Prudencia --------------------------------------------------------

    def test_ningun_movimiento_se_pierde(self):
        con_asiento = sum(1 for c in self.clasificados
                          if not c.contabilizado_en_otro and abs(c.importe) >= 0.005)
        traspasos = sum(1 for c in self.clasificados if c.contabilizado_en_otro)
        self.assertEqual(con_asiento + traspasos + len(self.ceros), len(self.movimientos))

    def test_lo_dudoso_queda_marcado(self):
        for c in self.clasificados:
            if c.contrapartida == PUENTE and not c.contabilizado_en_otro:
                with self.subTest(texto=c.texto[:40]):
                    self.assertTrue(c.revisar, "todo lo que va a la puente se revisa")
                    self.assertTrue(c.motivo_revision, "y dice por qué")


if __name__ == "__main__":
    unittest.main(verbosity=2 if "-v" in sys.argv else 1)
