---
description: Estado de la cartera — qué está pendiente, qué vence, qué hay que revisar
argument-hint: [resumen|revisar|vencimientos|cliente <nombre>|modelo <n>|alquileres|huecos]
---

Consulta del control de cartera: **$ARGUMENTS**

Carga la skill `control-de-cartera` y ejecuta el subcomando que corresponda de
`scripts/control.py`. **No leas el Excel entero**: cuesta ~15.000 tokens y el script ya
devuelve la información filtrada.

| Lo que pide el usuario | Subcomando |
|---|---|
| Sin argumentos, «cómo vamos» | `resumen` |
| «qué hay que revisar» | `cola --estado Revisar` |
| «a quién le falta el 303» | `cola --estado Pendiente --modelo 303` |
| Un nombre de cliente | `cliente "<nombre>"` |
| Un número de modelo | `modelo <n>` |
| «qué vence» | `vencimientos --dias 30` |
| «alquileres» | `alquileres` |
| «revisa el control», «incoherencias» | `huecos` |

Si el fichero no está en el directorio actual, pregunta su ruta y pásala con `--fichero`.

Al presentar el resultado:
- Saca primero la cola de **Revisar**: es trabajo terminado sin presentar, y es donde se
  pierden los plazos.
- Señala los ejercicios anteriores pendientes (columnas `(2)` y `(3)`): son sanciones del
  art. 198 LGT acumulándose.
- Para marcar un estado, ejecuta siempre antes con `--simular` y enseña el cambio.
- No interpretes las marcas `T`, `V` y `O`: su significado está sin confirmar.
