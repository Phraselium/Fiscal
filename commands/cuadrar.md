---
description: Cuadra los modelos de un cliente entre sí y contra la contabilidad
argument-hint: <cliente> <ejercicio>
---

**$ARGUMENTS**

Antes de responder:

- Genera la plantilla: `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py --plantilla`
- Rellénala con las cifras del cliente que tengas
- Ejecuta `cuadrar.py --datos <fichero>` y resuelve cada descuadre
- Distingue lo que cuadra de lo que no se ha podido comprobar
