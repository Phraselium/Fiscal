---
description: Comprueba que no se filtran datos de clientes al repositorio
argument-hint: [--staged | --historial]
---

**$ARGUMENTS**

Antes de responder:

- Ejecuta `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py`
- Detecta NIF con letra válida, IBAN, correos, teléfonos y ficheros prohibidos
- Con `--historial` busca también en los commits ya hechos
- Instala el hook con `--instalar-hook` para que se compruebe en cada commit
