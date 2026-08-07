---
description: Declaraciones informativas y facturación: umbrales, requisitos, SII y VeriFactu
argument-hint: <el modelo o la duda>
---

**$ARGUMENTS**

Carga la skill `informativas-y-facturacion` y trabaja con ella.

Antes de responder:

- Qué informativa corresponde y su umbral
- Qué se incluye y qué está ya informado por otra vía
- Si es facturación: requisitos del art. 6 RD 1619/2012
- Si es VeriFactu: verifica la fecha, se ha aplazado dos veces

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
