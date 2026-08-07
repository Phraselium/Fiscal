---
description: Consulta del Impuesto sobre Sociedades: ajustes, base, tipos y deducciones
argument-hint: <la duda o la entidad>
---

**$ARGUMENTS**

Carga la skill `impuesto-sociedades` y trabaja con ella.

Antes de responder:

- Ejercicio y cifra de negocios del año anterior (determina el tipo)
- Ajustes extracontables que procedan, con su artículo
- Verifica el tipo del ejercicio: está en calendario transitorio
- ¿Hay operaciones vinculadas? Entonces hay modelo 232 en noviembre

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
