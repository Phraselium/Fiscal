---
description: Estado de la cartera: pendientes, vencimientos y revisiones
argument-hint: [resumen | revisar | cliente <nombre> | modelo <n> | vencimientos | huecos]
---

**$ARGUMENTS**

Carga `control-de-cartera`. **No leas el Excel entero**: cuesta ~15.000 tokens y el
script devuelve la información filtrada.

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py --fichero Control.xlsx <subcomando>
```

| Lo que piden | Subcomando |
|---|---|
| «cómo vamos» | `resumen` |
| «qué hay que revisar» | `cola --estado Revisar` |
| «a quién le falta el 303» | `cola --estado Pendiente --modelo 303` |
| Un nombre de cliente | `cliente "<nombre>"` |
| Un número de modelo | `modelo <n>` |
| «qué vence» | `vencimientos --dias 30` |
| «revisa el control» | `huecos` |

Saca primero la cola de **Revisar**: es trabajo terminado sin presentar, y es donde se
pierden los plazos. Señala los ejercicios anteriores pendientes (columnas `(2)` y `(3)`).

Para marcar un estado, ejecuta antes con `--simular` y enseña el cambio. No interpretes
las marcas `T`, `V` y `O`: su significado está sin confirmar.

Si piden el estado en Excel, pásalo con `exportar --formato csv` a `/entregable`.
