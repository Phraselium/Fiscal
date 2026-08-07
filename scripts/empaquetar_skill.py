#!/usr/bin/env python3
"""Empaqueta el plugin como una Skill de claude.ai (.zip listo para subir).

Claude Code y claude.ai no soportan lo mismo:

                      Claude Code    claude.ai
  Skills                  si            si
  Comandos de barra       si            NO
  Subagentes              si            NO
  Scripts en Python       si            si (con biblioteca estandar)

Por eso este empaquetador **consolida** las 34 skills, los 27 comandos y los 2
agentes en UNA sola skill con navegacion interna, en lugar de exigir 34 subidas:

    asesoria-fiscal-es/
      SKILL.md                  enrutador: que hay y donde esta
      referencias/              el conocimiento, un fichero por materia
      flujos/                   los comandos convertidos en procedimientos
      revision/                 los agentes convertidos en procedimientos
      scripts/  datos/  disenos/

Uso
---
    python3 scripts/empaquetar_skill.py
    python3 scripts/empaquetar_skill.py --salida ~/Descargas
    python3 scripts/empaquetar_skill.py --sin-comprimir   # deja la carpeta

Despues: claude.ai -> Ajustes -> Capacidades -> Skills -> Subir skill.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOMBRE = "asesoria-fiscal-es"

# Orden de presentacion en el enrutador: el marco primero, luego el flujo de trabajo.
ORDEN_MATERIAS = [
    "asesoria-fiscal", "consultas-por-impuesto", "modelos-aeat", "control-de-cartera",
    "entrada-de-documentos", "generacion-de-entregables", "procedimientos-y-plazos",
    "gestion-del-despacho",
]


def sin_frontmatter(texto: str) -> tuple[dict, str]:
    if not texto.startswith("---\n"):
        return {}, texto
    _, fm, cuerpo = texto.split("---\n", 2)
    campos = {}
    for linea in fm.splitlines():
        if ": " in linea and not linea.startswith(" "):
            clave, valor = linea.split(": ", 1)
            campos[clave.strip()] = valor.strip()
    return campos, cuerpo.lstrip("\n")


def rutas_relativas(texto: str) -> str:
    """En claude.ai no existe CLAUDE_PLUGIN_ROOT: todo cuelga de la carpeta de la skill."""
    texto = texto.replace('"${CLAUDE_PLUGIN_ROOT:-.}"/', "")
    texto = texto.replace("${CLAUDE_PLUGIN_ROOT:-.}/", "")
    texto = texto.replace("$CLAUDE_PLUGIN_ROOT/", "")
    return texto.replace("${CLAUDE_PLUGIN_ROOT}/", "")


def construir(destino: Path) -> Path:
    paquete = destino / NOMBRE
    if paquete.exists():
        shutil.rmtree(paquete)
    (paquete / "referencias").mkdir(parents=True)
    (paquete / "flujos").mkdir()
    (paquete / "revision").mkdir()

    # --- Materias: cuerpo de cada skill + su detalle, en un solo fichero ---
    materias: dict[str, str] = {}
    for ruta in sorted(RAIZ.glob("skills/*/SKILL.md")):
        nombre = ruta.parent.name
        campos, cuerpo = sin_frontmatter(ruta.read_text(encoding="utf-8"))
        (paquete / "referencias" / f"{nombre}.md").write_text(
            rutas_relativas(cuerpo), encoding="utf-8")
        # El detalle de cada materia conserva su propio fichero, para no cargarlo entero.
        for detalle in sorted(ruta.parent.glob("references/*.md")):
            sub = paquete / "referencias" / nombre
            sub.mkdir(exist_ok=True)
            (sub / detalle.name).write_text(
                rutas_relativas(detalle.read_text(encoding="utf-8")), encoding="utf-8")
        materias[nombre] = campos.get("description", "")

    # --- Comandos -> flujos de trabajo ---
    flujos: dict[str, str] = {}
    for ruta in sorted(RAIZ.glob("commands/*.md")):
        if ruta.stem == "fiscal":
            continue  # su contenido es el propio enrutador
        campos, cuerpo = sin_frontmatter(ruta.read_text(encoding="utf-8"))
        cuerpo = rutas_relativas(cuerpo).replace("**$ARGUMENTS**", "").replace("$ARGUMENTS", "lo pedido")
        encabezado = (f"# {campos.get('description', ruta.stem)}\n\n"
                      f"> Procedimiento. En claude.ai se activa pidiendolo con palabras: "
                      f"«{campos.get('argument-hint', '').strip('<>[]') or ruta.stem}».\n\n")
        (paquete / "flujos" / f"{ruta.stem}.md").write_text(encabezado + cuerpo, encoding="utf-8")
        flujos[ruta.stem] = campos.get("description", "")

    # --- Agentes -> procedimientos de revision y redaccion ---
    revisiones: dict[str, str] = {}
    for ruta in sorted(RAIZ.glob("agents/*.md")):
        campos, cuerpo = sin_frontmatter(ruta.read_text(encoding="utf-8"))
        cuerpo = rutas_relativas(cuerpo)
        encabezado = (f"# {ruta.stem}\n\n> En claude.ai no hay subagentes: aplica este "
                      f"procedimiento tu mismo cuando corresponda.\n\n")
        (paquete / "revision" / f"{ruta.stem}.md").write_text(encabezado + cuerpo, encoding="utf-8")
        revisiones[ruta.stem] = campos.get("description", "").split(".")[0]

    # --- Codigo y datos ---
    for carpeta in ("scripts", "datos", "disenos", "ejemplos", "config"):
        origen = RAIZ / carpeta
        if not origen.exists():
            continue
        shutil.copytree(origen, paquete / carpeta, ignore=shutil.ignore_patterns(
            "__pycache__", "*.pyc", "nombres_privados.txt",
            # Herramientas de desarrollo del repositorio: no sirven dentro de la skill.
            "empaquetar_skill.py", "comprobar_privacidad.py"))
    for script in (paquete / "scripts").rglob("*.py"):
        script.write_text(rutas_relativas(script.read_text(encoding="utf-8")), encoding="utf-8")

    (paquete / "SKILL.md").write_text(
        enrutador(materias, flujos, revisiones), encoding="utf-8")
    return paquete


def enrutador(materias, flujos, revisiones) -> str:
    def filas(indice: dict[str, str], carpeta: str, orden: list[str] | None = None) -> str:
        claves = ([k for k in (orden or []) if k in indice]
                  + sorted(k for k in indice if k not in (orden or [])))
        return "\n".join(
            f"| `{carpeta}/{k}.md` | {indice[k].split(':')[0] if ':' in indice[k] else indice[k][:70]} |"
            for k in claves)

    return f"""---
name: asesoria-fiscal-es
description: Asesoría fiscal española para despacho profesional. IRPF, IVA, Sociedades, retenciones, informativas, Intrastat, procedimientos con la AEAT, control de cartera y generación de ficheros en el diseño de registro oficial. Úsala para cualquier consulta fiscal española, cálculo o revisión de impuestos, notificación de Hacienda o gestión de la cartera de clientes.
license: MIT
---

# Asesoría fiscal española

Conocimiento y herramientas para el trabajo diario de un despacho fiscal en España.
Todas las rutas de este documento son **relativas a la carpeta de esta skill**.

## Cómo usar esta skill

1. **Lee siempre primero** `referencias/asesoria-fiscal.md`. Son las reglas de
   trabajo: jerarquía de fuentes, prohibición de inventar cifras y formato de los
   entregables. Se aplican por encima de todo lo demás.
2. Localiza la materia en las tablas de abajo y **lee solo el fichero que necesites**.
   No cargues todas las referencias: son unas 300 KB.
3. Si la tarea encaja con un flujo de trabajo, sigue el de `flujos/`.
4. Antes de dar por bueno un entregable, aplica `revision/revisor-fiscal.md`.

## Las tres reglas que no se saltan

**No memorices cifras: consúltalas.**
```bash
python3 scripts/parametros.py buscar iva
python3 scripts/parametros.py ver is.tipo.microempresa
python3 scripts/parametros.py revisar     # qué NO es fiable
```
Lo que salga `volatil` o `sin_verificar` **no se usa en un entregable sin contrastarlo**.
Escribe `⚠️ SIN VERIFICAR — contrastar en <fuente>` junto al dato.

**No inventes referencias.** Cita el artículo concreto. Si no estás seguro del número de
una consulta de la DGT o del ECLI de una sentencia, describe el criterio sin numerarlo.

**Nada se presenta ante la AEAT.** Esta skill prepara, calcula y cuadra. Presentar es un
acto humano con certificado. Nunca digas que una declaración «se ha presentado».

## Materias

Cada materia tiene su fichero, y las más extensas una subcarpeta con el detalle. Lee
solo lo que necesites: el conjunto son unas 300 KB.

| Fichero | Contenido |
|---|---|
{filas(materias, 'referencias', ORDEN_MATERIAS)}

`referencias/consultas-por-impuesto/` tiene un fichero por impuesto, y
`referencias/modelos-aeat/` uno por modelo.

## Flujos de trabajo

| Fichero | Para qué |
|---|---|
{filas(flujos, 'flujos')}

## Revisión y redacción

| Fichero | Para qué |
|---|---|
{filas(revisiones, 'revision')}

## Herramientas

Todas funcionan con la biblioteca estándar de Python 3.10+, salvo donde se indica.

| Script | Para qué |
|---|---|
| `scripts/parametros.py` | Tipos, umbrales y límites, con su estado de fiabilidad |
| `scripts/calcular_plazos.py` | Vencimientos, periodo voluntario, recargos de los arts. 27 y 28 LGT |
| `scripts/cuadrar.py` | Cuadrar modelos entre sí y contra la contabilidad |
| `scripts/lib/validaciones.py` | Validar NIF, NIE, CIF, NIF-IVA, IBAN, código NC8 |
| `scripts/generar_informativa.py` | Fichero de una informativa en diseño de registro |
| `scripts/generar_intrastat.py` | Fichero Intrastat para el portal de Aduanas |
| `scripts/validar_fichero.py` | Validar y descomponer un fichero generado |
| `scripts/control.py` | Control de cartera sobre un Control.xlsx — **necesita `openpyxl`** |

Empieza cualquier script por `--help`: todos lo tienen y explican su entrada.

## Antes de responder

Determina, y pregunta si falta algo que cambie el resultado:

- **Ejercicio fiscal**: la respuesta cambia cada año.
- **Territorio**: común, foral (Álava, Bizkaia, Gipuzkoa, Navarra), Canarias (IGIC) o
  Ceuta y Melilla (IPSI). En territorio foral la normativa estatal **no** aplica: avisa
  y detente.
- **CCAA** si hay IRPF, ISD, ITP o Patrimonio de por medio.
- **Régimen del contribuyente** y cifra de negocios del año anterior.

## Método

```
HECHOS → CALIFICACIÓN → SUJECIÓN → DEVENGO → BASE → TIPO Y CUOTA
      → OBLIGACIONES (modelo, plazo, forma) → RIESGO → RECOMENDACIÓN
```

Ante una posición discutible, cuantifica: cuota + recargo o sanción + intereses =
exposición total, y la probabilidad de comprobación con su motivo.

## Datos de clientes

Alta sensibilidad económica. No los reproduzcas fuera de su contexto y anonimiza en
plantillas y ejemplos. Los despachos son sujetos obligados de la Ley 10/2010: ante
indicios de operativa sospechosa, señálalo al responsable de cumplimiento en lugar de
tratarlo como un problema técnico.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", type=Path, default=RAIZ / "dist")
    ap.add_argument("--sin-comprimir", action="store_true")
    args = ap.parse_args()

    args.salida.mkdir(parents=True, exist_ok=True)
    paquete = construir(args.salida)

    ficheros = sorted(p for p in paquete.rglob("*") if p.is_file())
    tamano = sum(p.stat().st_size for p in ficheros)

    print(f"Skill construida: {paquete}")
    print(f"  {len(ficheros)} ficheros · {tamano / 1024:.0f} KB")
    for carpeta in ("referencias", "flujos", "revision", "scripts", "datos", "disenos"):
        n = len(list((paquete / carpeta).rglob("*.*"))) if (paquete / carpeta).exists() else 0
        if n:
            print(f"      {carpeta:<14}{n:3} ficheros")

    if args.sin_comprimir:
        return 0

    zip_destino = args.salida / f"{NOMBRE}.zip"
    with zipfile.ZipFile(zip_destino, "w", zipfile.ZIP_DEFLATED) as z:
        for fichero in ficheros:
            z.write(fichero, fichero.relative_to(args.salida))
    shutil.rmtree(paquete)

    print(f"\nPaquete: {zip_destino}  ({zip_destino.stat().st_size / 1024:.0f} KB)")
    print("\nPara instalarlo en claude.ai:")
    print("  Ajustes → Capacidades → Skills → Subir skill → elige este .zip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
