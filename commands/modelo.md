---
description: Prepara, revisa o cuadra cualquier modelo tributario
argument-hint: <número de modelo> [periodo/ejercicio] [cliente]
---

**$ARGUMENTS**

Carga `modelos-aeat` y el fichero de referencia del modelo. Si no tiene uno propio, usa
`references/catalogo.md`.

1. Confirma ejercicio, periodo, régimen del contribuyente y CCAA si aplica.
2. Localiza la documentación de partida. Si no está, pídela antes de calcular.
3. Calcula casilla a casilla, mostrando el detalle.
4. **Cuadra** contra los modelos relacionados con
   `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py`. Si algo no cuadra, para y
   explica la diferencia antes de seguir.
5. Indica plazo de presentación, plazo de **domiciliación** y fecha límite interna
   (vencimiento − 5 días hábiles).

Si hay que producir el fichero o un Excel, sigue con `/entregable`. Recuerda que el
resultado es un borrador: presentar es un acto humano.
