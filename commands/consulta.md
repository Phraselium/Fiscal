---
description: Resuelve una duda fiscal con la norma que la sostiene
argument-hint: <la duda, la operación o el cliente>
---

**$ARGUMENTS**

Carga `asesoria-fiscal` y, según la materia, el fichero que toque de
`consultas-por-impuesto/references/`.

Aplica el método: HECHOS → CALIFICACIÓN → SUJECIÓN → DEVENGO → BASE → TIPO Y CUOTA →
OBLIGACIONES → RIESGO → RECOMENDACIÓN.

Antes de calcular, asegúrate de tener: **ejercicio**, **CCAA** si hay IRPF, ISD, ITP o
Patrimonio, y **régimen del contribuyente**. Si falta algo que cambie la respuesta,
pregúntalo.

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar
<ámbito>`, nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal.

Responde con la **conclusión primero** y el artículo que la sostiene. Si hay posición
discutible, cuantifica el riesgo. Si piden nota para el expediente o comunicación al
cliente, usa `/entregable`.
