---
description: Consulta de IVA: sujeción, localización, exenciones, deducibilidad y regímenes
argument-hint: <la duda, la operación o el cliente>
---

**$ARGUMENTS**

Carga la skill `iva` y trabaja con ella.

Antes de responder:

- ¿Qué operación es y entre quiénes?
- ¿Dónde se localiza? Es donde más se falla
- ¿Hay inversión del sujeto pasivo?
- ¿El IVA soportado es deducible y en qué porcentaje?

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
