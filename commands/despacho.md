---
description: Gestión del despacho: alta de clientes, encargo, blanqueo y conservación
argument-hint: <la tarea>
---

**$ARGUMENTS**

Carga la skill `gestion-de-despacho` y trabaja con ella.

Antes de responder:

- Si es un alta: diagnostica lo que se hereda ANTES de firmar
- Define el alcance por escrito, sobre todo lo excluido
- Obligaciones de PBC/FT: identificación y titular real
- Plazos de conservación: en la práctica, 10 años

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
