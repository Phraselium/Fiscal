---
description: Patrimonio, herencias, donaciones, transmisiones y no residentes
argument-hint: <la operación o el contribuyente>
---

**$ARGUMENTS**

Carga la skill `patrimonio-sucesiones-y-no-residentes` y trabaja con ella.

Antes de responder:

- **CCAA competente** por su punto de conexión: sin esto no hay cálculo
- Si es donación: advierte del IRPF del donante
- Si es empresa familiar: documenta los requisitos del art. 4.Ocho IP
- Si es no residente: certificado de residencia y convenio aplicable

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
