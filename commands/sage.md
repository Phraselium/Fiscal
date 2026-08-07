---
description: Sage Despachos: migración desde ContaPlus, importación y qué no cubre
argument-hint: <la tarea: migrar, importar, cuadrar…>
---

**$ARGUMENTS**

Carga la skill `sage-despachos` y trabaja con ella.

Antes de responder:

- Recuerda: Sage genera y presenta los modelos; el plugin prepara y cuadra
- Si es migración: recorre el checklist cliente a cliente
- Si es importación: enseña un extracto y el total antes de cargar nada
- Cuadra siempre lo que Sage saque antes de presentarlo

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
