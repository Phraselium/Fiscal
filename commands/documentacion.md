---
description: Documentación de clientes: Excel, papel y PDF escaneado a datos utilizables
argument-hint: <el cliente y el canal por el que envía>
---

**$ARGUMENTS**

Carga la skill `documentacion-de-clientes` y trabaja con ella.

Antes de responder:

- Monta el inventario de lo recibido contra lo esperado
- Comprueba la correlatividad de las series de facturas emitidas
- Valida aritmética y NIF de cada factura
- Entrega un listado de excepciones: nunca inventes un dato ilegible

Consulta las cifras con `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar <ámbito>`,
nunca de memoria. Lo que salga `volatil` o `sin_verificar` va marcado como tal en el
entregable.

Si falta un dato que cambia la respuesta —ejercicio, CCAA, régimen del contribuyente—
pregúntalo antes de calcular.
