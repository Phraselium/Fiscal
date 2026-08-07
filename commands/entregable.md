---
description: Genera un fichero, un Excel, un informe o un escrito
argument-hint: <qué: fichero 190 | excel | informe | escrito> <cliente> <periodo>
---

**$ARGUMENTS**

Carga `generacion-de-entregables`.

| Qué piden | Cómo |
|---|---|
| Fichero de una informativa | `scripts/generar_informativa.py` |
| Intrastat | `scripts/generar_intrastat.py` |
| **Excel** de un informe, cuadre o listado | `scripts/generar_excel.py` |
| Validar un fichero antes de subirlo | `scripts/validar_fichero.py` |
| Informe, nota interna o escrito a Hacienda | Plantillas de la skill |

Todos como `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/<script>.py`; empieza por `--help`.

**Antes de generar, cuadra.** Si un cuadre no sale, para y explica la diferencia: no
produzcas un fichero descuadrado.

Los diseños de registro están marcados como borradores y el generador aborta salvo que se
acepte expresamente. Si generas así, **dilo en la respuesta**: el fichero debe pasar por
el validador de la sede antes de darlo por bueno.

Informa siempre de la ruta del resultado, sus totales y el siguiente paso. Nunca digas
que se ha presentado nada.
