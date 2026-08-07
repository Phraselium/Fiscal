---
description: Consulta de IRPF: rentas, reducciones, mínimos y deducciones autonómicas
argument-hint: <la duda o el contribuyente>
---

**$ARGUMENTS**

Carga la skill `irpf` y trabaja con ella.

Antes de responder:

- Residencia fiscal y **CCAA** de residencia habitual
- Cómo se califica la renta y a qué base va
- Individual vs. conjunta: calcula las dos
- Deducciones autonómicas, una a una

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
