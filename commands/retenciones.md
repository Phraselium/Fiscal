---
description: Retenciones e ingresos a cuenta: quién retiene, a qué tipo y en qué modelo
argument-hint: <la operación, el perceptor o el modelo>
---

**$ARGUMENTS**

Carga la skill `retenciones-y-censos` y trabaja con ella.

Antes de responder:

- Quién paga y en calidad de qué (¿ejerce actividad económica?)
- Naturaleza de la renta y tipo aplicable
- Modelo periódico y su resumen anual
- Recuerda: las retenciones son deuda **inaplazable**

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
