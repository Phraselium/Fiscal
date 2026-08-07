---
description: Contrasta normativa, diseños de registro y privacidad
argument-hint: [normativa | diseno <modelo> | privacidad]
---

**$ARGUMENTS**

**normativa** — `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py revisar` saca
los `volatil` y `sin_verificar`. Contrástalos en el BOE, la sede de la AEAT, los manuales
prácticos del ejercicio, la Orden anual de módulos, la Ley de Presupuestos (interés de
demora) y el boletín de la CCAA. Actualiza `datos/parametros.json` con `valor`,
`"estado": "verificado"`, `verificado_el` y `fuente`. **No cambies un valor que no hayas
podido verificar**: márcalo como pendiente.

**diseno** — localiza el anexo de diseños de registro de la orden del modelo, contrasta
campo a campo, corrige `disenos/<modelo>.json` y prueba generando un fichero. Márcalo
`"verificado": true` solo si has contrastado todos los bloques. El validador de la sede
es la comprobación definitiva.

**privacidad** — `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py`
revisa que no se filtren datos de clientes. Con `--historial` busca en los commits;
con `--instalar-hook` lo deja automático en cada commit.
