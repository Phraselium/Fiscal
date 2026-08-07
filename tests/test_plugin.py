#!/usr/bin/env python3
"""Suite de pruebas del plugin. Sin dependencias mas alla de openpyxl.

    python3 tests/test_plugin.py          # todo
    python3 tests/test_plugin.py -v       # detalle de cada prueba

Cubre lo que puede romperse en silencio y costar dinero: validacion de
identificadores, parseo del control, cuadres entre modelos, generacion de
ficheros de longitud fija, computo de plazos y la comprobacion de privacidad.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

from lib.registro import (  # noqa: E402
    Diseno, ErrorDiseno, ImporteAmbiguo, a_centimos, a_decimal, construir_registro,
    escribir_fichero, normalizar_texto, validar_fichero,
)
from lib.validaciones import (  # noqa: E402
    validar_codigo_nc8, validar_iban, validar_nif, validar_nif_iva,
)
import calcular_plazos as cp  # noqa: E402
import cuadrar  # noqa: E402
import control  # noqa: E402


class TestValidaciones(unittest.TestCase):
    def test_nif_persona_fisica(self):
        self.assertTrue(validar_nif("12345678Z")[0])
        self.assertFalse(validar_nif("12345678A")[0], "letra de control incorrecta")

    def test_nie(self):
        self.assertTrue(validar_nif("X1234567L")[0])
        self.assertFalse(validar_nif("X1234567A")[0])

    def test_cif(self):
        self.assertTrue(validar_nif("B12345674")[0])
        self.assertFalse(validar_nif("B12345670")[0])

    def test_nif_longitud_y_basura(self):
        for malo in ("1234567Z", "", "ABCDEFGHI", "123456789012"):
            self.assertFalse(validar_nif(malo)[0], f"'{malo}' no deberia validar")

    def test_nif_iva(self):
        self.assertTrue(validar_nif_iva("FR12345678901")[0])
        self.assertFalse(validar_nif_iva("US123456789")[0], "EE.UU. no es Estado miembro")
        self.assertFalse(validar_nif_iva("ES12345678A")[0], "NIF espanol incorrecto")

    def test_iban(self):
        self.assertTrue(validar_iban("ES9121000418450200051332")[0])
        self.assertFalse(validar_iban("ES9121000418450200051333")[0])

    def test_nc8(self):
        self.assertTrue(validar_codigo_nc8("84713000")[0])
        self.assertFalse(validar_codigo_nc8("8471300")[0], "debe tener 8 digitos")


class TestRegistro(unittest.TestCase):
    def test_normalizacion_conserva_enye(self):
        self.assertEqual(normalizar_texto("Muñoz Peña"), "MUÑOZ PEÑA")
        self.assertEqual(normalizar_texto("José Ángel"), "JOSE ANGEL")

    def test_importes_a_centimos(self):
        self.assertEqual(a_centimos("1.234,56"), 123456)
        self.assertEqual(a_centimos(1234.56), 123456)
        self.assertEqual(a_centimos("0"), 0)
        self.assertEqual(a_centimos(None), 0)
        self.assertEqual(a_centimos("-500,00"), -50000)
        self.assertEqual(a_centimos("1.234.567,89"), 123456789)

    def test_formato_ingles_no_se_multiplica_por_cien(self):
        """Regresion: '1234.56' se leia como 123456 EUR (error x100)."""
        self.assertEqual(a_centimos("1234.56"), 123456)
        self.assertEqual(a_decimal("0.75"), cuadrar.Decimal("0.75"))

    def test_importe_ambiguo_se_rechaza(self):
        """'1.234' puede ser 1234 o 1,234: hay que fallar, no adivinar."""
        for ambiguo in ("1.234", "0.005", "12.500"):
            with self.subTest(valor=ambiguo):
                with self.assertRaises(ImporteAmbiguo):
                    a_centimos(ambiguo)

    def test_redondeo_medio_arriba(self):
        self.assertEqual(a_centimos("0,005"), 1, "0,005 EUR debe redondear a 1 centimo")
        self.assertEqual(a_centimos("0,004"), 0)

    def test_todos_los_disenos_cubren_250(self):
        for ruta in sorted((RAIZ / "disenos").glob("*.json")):
            with self.subTest(diseno=ruta.name):
                d = Diseno.cargar(ruta)  # comprobar() falla si hay hueco o solape
                self.assertEqual(d.longitud, 250)
                self.assertIn("1", d.registros)
                self.assertIn("2", d.registros)

    def test_diseno_con_hueco_falla(self):
        malo = {"modelo": "999", "longitud": 250, "registros": {"1": [
            {"nombre": "a", "desde": 1, "hasta": 1, "tipo": "C", "valor": "1"},
            {"nombre": "b", "desde": 3, "hasta": 250, "tipo": "X"},  # hueco en 2
        ]}}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(malo, f)
            ruta = Path(f.name)
        with self.assertRaises(ErrorDiseno):
            Diseno.cargar(ruta)
        ruta.unlink()

    def test_registro_generado_mide_250(self):
        d = Diseno.cargar(RAIZ / "disenos" / "190.json")
        datos = {
            "ejercicio": "2025", "nif_declarante": "B12345674",
            "denominacion_declarante": "RAZON SOCIAL DE PRUEBA SL",
            "telefono_contacto": "911234567", "persona_contacto": "CONTACTO",
            "numero_identificativo": "1900000000001",
            "numero_total_percepciones": 1, "importe_total_percepciones": 1000,
            "importe_total_retenciones": 150,
        }
        linea = construir_registro(d, "1", datos)
        self.assertEqual(len(linea), 250)
        self.assertTrue(linea.startswith("11902025B12345674"))

    def test_signo_negativo(self):
        d = Diseno.cargar(RAIZ / "disenos" / "190.json")
        base = {
            "ejercicio": "2025", "nif_declarante": "B12345674",
            "denominacion_declarante": "X", "telefono_contacto": "911234567",
            "persona_contacto": "X", "numero_identificativo": "1900000000001",
            "numero_total_percepciones": 1, "importe_total_retenciones": 0,
        }
        pos = construir_registro(d, "1", {**base, "importe_total_percepciones": 100})
        neg = construir_registro(d, "1", {**base, "importe_total_percepciones": -100})
        self.assertEqual(pos[144], " ", "positivo: signo en blanco")
        self.assertEqual(neg[144], "N", "negativo: signo 'N'")
        self.assertEqual(pos[145:160], neg[145:160], "el importe se graba en valor absoluto")

    def test_fichero_valido_en_latin1_con_crlf(self):
        d = Diseno.cargar(RAIZ / "disenos" / "190.json")
        datos = {
            "ejercicio": "2025", "nif_declarante": "B12345674",
            "denominacion_declarante": "MUÑOZ Y PEÑA SL", "telefono_contacto": "911234567",
            "persona_contacto": "CONTACTO", "numero_identificativo": "1900000000001",
            "numero_total_percepciones": 1, "importe_total_percepciones": 1000,
            "importe_total_retenciones": 150,
        }
        with tempfile.TemporaryDirectory() as tmp:
            destino = escribir_fichero(Path(tmp) / "190.txt", [construir_registro(d, "1", datos)])
            self.assertEqual(validar_fichero(destino, 250), [])
            self.assertIn(b"\r\n", destino.read_bytes())
            self.assertIn("MUÑOZ", destino.read_bytes().decode("iso-8859-1"))


class TestPlazos(unittest.TestCase):
    def test_meses_de_fecha_a_fecha(self):
        self.assertEqual(cp.sumar_meses(date(2026, 9, 15), 1), date(2026, 10, 15))

    def test_mes_sin_dia_equivalente(self):
        self.assertEqual(cp.sumar_meses(date(2026, 1, 31), 1), date(2026, 2, 28))

    def test_dias_habiles_saltan_fin_de_semana(self):
        # Viernes 7/8/2026 + 1 habil = lunes 10.
        self.assertEqual(cp.sumar_habiles(date(2026, 8, 7), 1, set()), date(2026, 8, 10))

    def test_festivos_se_excluyen(self):
        festivo = {date(2026, 8, 10)}
        self.assertEqual(cp.sumar_habiles(date(2026, 8, 7), 1, festivo), date(2026, 8, 11))

    def test_periodo_voluntario_art_62_2(self):
        # Notificado el 3 (dia <= 15) -> hasta el 20 del mes siguiente.
        self.assertEqual(cp.sumar_meses(date(2026, 10, 1), 1).replace(day=20), date(2026, 11, 20))
        # Notificado el 20 (dia > 15) -> hasta el 5 del segundo mes siguiente.
        self.assertEqual(cp.sumar_meses(date(2026, 10, 1), 2).replace(day=5), date(2026, 12, 5))


class TestCuadres(unittest.TestCase):
    def _informe(self, datos):
        inf = cuadrar.Informe(cuadrar.Decimal("0.01"))
        cuadrar.cuadrar(datos, inf)
        return inf

    def test_detecta_aib_sin_deducir(self):
        inf = self._informe({"m303": [
            {"periodo": "1T", "casilla_10_11": 3000, "casilla_36_37": 0}]})
        self.assertTrue(any("AIB" in t for t, _, _ in inf.fallos))

    def test_aib_correcta_no_da_fallo(self):
        inf = self._informe({"m303": [
            {"periodo": "1T", "casilla_10_11": 3000, "casilla_36_37": 3000}]})
        self.assertFalse(any("AIB" in t for t, _, _ in inf.fallos))

    def test_detecta_arrastre_de_compensacion_roto(self):
        inf = self._informe({"m303": [
            {"periodo": "1T", "casilla_72": 500},
            {"periodo": "2T", "casilla_67": 0}]})
        self.assertTrue(any("casilla 67" in t for t, _, _ in inf.fallos))

    def test_detecta_111_190_descuadrado(self):
        inf = self._informe({
            "m111": [{"periodo": "1T", "base": 45000, "retenciones": 6750}],
            "m190": {"base": 50000, "retenciones": 6750}})
        self.assertTrue(any("111 ↔ 190 bases" in t for t, _, _ in inf.fallos))

    def test_intrastat_no_puede_superar_al_349(self):
        inf = self._informe({
            "m349": [{"periodo": "1T", "clave_E": 10000}],
            "intrastat": {"expedicion": 15000}})
        self.assertTrue(any("Intrastat" in t for t, _, _ in inf.fallos))

    def test_falta_de_datos_no_se_cuenta_como_cuadre(self):
        inf = self._informe({"m303": [{"periodo": "1T", "casilla_27": 100}]})
        self.assertTrue(inf.omitidas, "debe declarar lo que no ha podido comprobar")

    def test_tolerancia_absorbe_redondeos(self):
        inf = cuadrar.Informe(cuadrar.Decimal("0.01"))
        cuadrar.cuadrar({
            "m111": [{"periodo": "1T", "base": 1000.00, "retenciones": 150.00}],
            "m190": {"base": 1000.01, "retenciones": 150.00}}, inf)
        self.assertFalse(any("bases" in t for t, _, _ in inf.fallos))


class TestControl(unittest.TestCase):
    """Usa una matriz sintetica: nunca datos reales del despacho."""

    @classmethod
    def setUpClass(cls):
        openpyxl = __import__("openpyxl")
        cls.tmp = tempfile.TemporaryDirectory()
        cls.ruta = Path(cls.tmp.name) / "ControlPrueba.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "2T-2026"
        ws.append(["CONTROL DE PRUEBA"]); ws.append([]); ws.append([]); ws.append([])
        ws.append(["NOMBRE", "111", "303", "347", "390", "200/24", "202", "BANCO / Obs."])
        ws.append(["CLIENTE UNO SL", "Presentado [env]", "Presentado", "Pendiente",
                   "No aplica", "Pendiente [+]", "No aplica", "observacion de prueba"])
        ws.append(["ABC", "Revisar", "Presentado [neg]", "Pendiente", "Pendiente",
                   "Pendiente", "Pendiente", ""])
        ws.append(["CLIENTE TRES SL", "Baja", "Baja", "Sin dato", "Baja", "Baja", "Baja", ""])
        cal = wb.create_sheet("Calendario")
        cal.append(["Concepto", "Modelos", "Periodo", "Fecha límite", "Estado"])
        cal.append(["Autoliquidaciones 2T", "111·303", "2T-2026", date(2026, 7, 20), "Pendiente"])
        cal.append(["Impuesto sobre Sociedades", "200", "2025", date(2026, 7, 27), "Pendiente"])
        alq = wb.create_sheet("Alquileres")
        alq.append(["Inmueble", "ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
                    "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"])
        alq.append(["LOCAL DE PRUEBA", "Facturado", "Pendiente", "Facturado", "", "", "",
                    "", "", "", "", "", ""])
        wb.save(cls.ruta)
        cls.ctl = control.cargar(cls.ruta)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_lee_todos_los_clientes(self):
        self.assertEqual(len(self.ctl.clientes), 3)

    def test_no_descarta_nombres_cortos(self):
        """Regresion: una heuristica de longitud hacia desaparecer clientes."""
        self.assertIn("ABC", self.ctl.clientes)

    def test_parsea_estado_y_marcas(self):
        c = next(c for c in self.ctl.celdas if c.cliente == "CLIENTE UNO SL" and c.modelo == "111")
        self.assertEqual(c.estado, "Presentado")
        self.assertEqual(c.marcas, ["env"])

    def test_marcas_multiples(self):
        estado, marcas = control.parsear_celda("Presentado [T, env]")
        self.assertEqual(estado, "Presentado")
        self.assertEqual(marcas, ["T", "env"])

    def test_estado_sin_marcas(self):
        self.assertEqual(control.parsear_celda("Pendiente"), ("Pendiente", []))

    def test_celda_vacia(self):
        self.assertEqual(control.parsear_celda(None), ("", []))

    def test_accionables(self):
        vivos = [c for c in self.ctl.celdas if c.accionable]
        self.assertTrue(vivos)
        self.assertTrue(all(c.estado not in ("Presentado", "No aplica", "Baja") for c in vivos))

    def test_columna_observaciones_no_es_modelo(self):
        self.assertNotIn("BANCO / Obs.", self.ctl.modelos)
        self.assertIn("observacion de prueba", self.ctl.observaciones.get("CLIENTE UNO SL", ""))

    def test_filtrado(self):
        self.assertEqual(len(self.ctl.filtrar(estado="Revisar")), 1)
        self.assertEqual(len(self.ctl.filtrar(modelo="303")), 3)
        self.assertTrue(self.ctl.filtrar(cliente="uno"), "la busqueda debe ignorar mayusculas")

    def test_vencimientos(self):
        self.assertEqual(len(self.ctl.vencimientos), 2)
        self.assertEqual(self.ctl.vencimientos[0]["fecha_limite"], date(2026, 7, 20))

    def test_alquileres(self):
        self.assertEqual(len(self.ctl.alquileres), 1)
        self.assertEqual(self.ctl.alquileres[0]["meses"]["FEB"], "Pendiente")

    def test_huecos_detecta_incoherencia(self):
        """CLIENTE UNO tiene 303 en flujo y 390 'No aplica'."""
        class Args:
            pass
        import io
        from contextlib import redirect_stdout
        salida = io.StringIO()
        with redirect_stdout(salida):
            control.cmd_huecos(self.ctl, Args())
        self.assertIn("390", salida.getvalue())


class TestParametros(unittest.TestCase):
    def setUp(self):
        self.datos = json.loads((RAIZ / "datos" / "parametros.json").read_text(encoding="utf-8"))

    def test_json_valido_y_con_meta(self):
        self.assertIn("_meta", self.datos)

    def test_todo_parametro_tiene_estado_conocido(self):
        validos = {"estable", "verificado", "sin_verificar", "volatil"}
        for clave, entrada in self.datos.items():
            if clave.startswith("_"):
                continue
            with self.subTest(parametro=clave):
                self.assertIn(entrada.get("estado"), validos)

    def test_los_volatiles_no_llevan_valor(self):
        """Un parametro volatil con valor invita a usarlo sin verificar."""
        for clave, entrada in self.datos.items():
            if entrada.get("estado") == "volatil":
                with self.subTest(parametro=clave):
                    self.assertIsNone(entrada.get("valor"),
                                      f"{clave} es volatil: no debe llevar valor fijo")

    def test_los_volatiles_explican_por_que(self):
        for clave, entrada in self.datos.items():
            if entrada.get("estado") == "volatil":
                with self.subTest(parametro=clave):
                    self.assertTrue(entrada.get("nota") or entrada.get("url"))

    def test_verificados_llevan_fecha(self):
        for clave, entrada in self.datos.items():
            if entrada.get("estado") == "verificado":
                with self.subTest(parametro=clave):
                    self.assertTrue(entrada.get("verificado_el"))

    def test_verifactu_no_dice_2026(self):
        """Regresion del error normativo corregido: el aplazamiento es a 2027."""
        v = self.datos["verifactu.fecha_obligatoriedad"]["valor"]
        self.assertTrue(v["contribuyentes_is"].startswith("2027"))
        self.assertTrue(v["resto_obligados"].startswith("2027"))


class TestEstructuraDelPlugin(unittest.TestCase):
    def test_skills_con_frontmatter_coherente(self):
        import re
        for ruta in sorted((RAIZ / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=ruta.parent.name):
                texto = ruta.read_text(encoding="utf-8")
                self.assertTrue(texto.startswith("---\n"))
                fm = texto.split("---\n")[1]
                nombre = re.search(r"^name: (.+)$", fm, re.M)
                self.assertIsNotNone(nombre)
                self.assertEqual(nombre.group(1).strip(), ruta.parent.name)
                self.assertIn("description:", fm)

    def test_comandos_y_agentes_con_description(self):
        for ruta in list((RAIZ / "commands").glob("*.md")) + list((RAIZ / "agents").glob("*.md")):
            with self.subTest(fichero=ruta.name):
                self.assertIn("description:", ruta.read_text(encoding="utf-8").split("---\n")[1])

    def test_sin_referencias_a_scripts_inexistentes(self):
        """Regresion: cuadrar.py estuvo referenciado sin existir."""
        import re
        patron = re.compile(r"scripts/[a-z_/]+\.py")
        for carpeta in ("skills", "commands", "agents"):
            for ruta in (RAIZ / carpeta).rglob("*.md"):
                for referencia in patron.findall(ruta.read_text(encoding="utf-8")):
                    with self.subTest(fichero=str(ruta.relative_to(RAIZ)), script=referencia):
                        self.assertTrue((RAIZ / referencia).exists(),
                                        f"{referencia} no existe")

    def test_plugin_json_valido(self):
        datos = json.loads((RAIZ / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        for campo in ("name", "version", "description"):
            self.assertIn(campo, datos)


class TestPrivacidad(unittest.TestCase):
    def test_el_repositorio_esta_limpio(self):
        r = subprocess.run([sys.executable, "scripts/comprobar_privacidad.py"],
                           cwd=RAIZ, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, f"hay datos privados versionados:\n{r.stdout}")

    def test_detecta_nif_real(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "fuga.md"
            f.write_text("NIF B58818501 del cliente", encoding="utf-8")
            import comprobar_privacidad as priv
            hallazgos = priv.revisar_texto(f, "fuga.md", [])
            self.assertTrue(any(h.tipo == "NIF/NIE/CIF VALIDO" for h in hallazgos))

    def test_no_marca_los_nif_de_ejemplo(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "ok.md"
            f.write_text("NIF de ejemplo 12345678Z y B12345674", encoding="utf-8")
            import comprobar_privacidad as priv
            hallazgos = priv.revisar_texto(f, "ejemplos/ok.md", [])
            self.assertFalse([h for h in hallazgos if h.tipo == "NIF/NIE/CIF VALIDO"])


if __name__ == "__main__":
    unittest.main(verbosity=2 if "-v" in sys.argv else 1)
