---
description: Procesa lo que manda un cliente: PDF escaneado, Excel o papel
argument-hint: <cliente> <periodo> [canal]
---

**$ARGUMENTS**

Carga `entrada-de-documentos`.

1. **Inventario primero**: contrasta lo recibido con lo esperado (series correlativas de
   facturas emitidas, recibidas habituales, extractos completos, nóminas). Enumera lo que
   falta y redacta la reclamación.
2. **Extrae, no interpretes.** Un campo que no se lee con seguridad se marca como dudoso.
3. **Valida cada factura**: aritmética (base × tipo = cuota), NIF con
   `scripts/lib/validaciones.py`, y requisitos del art. 6 RD 1619/2012.
4. **Clasifica**: interior / AIB / ISP / exportación / exenta. Es lo que determina las
   casillas del 303. Si el origen no lo distingue, pregunta.
5. Entrega un **listado de excepciones**: ilegibles, incompletas, duplicadas o
   descuadradas.

**No inventes datos de una factura que no puedes leer.** Es preferible entregar 40
procesadas y 3 marcadas como ilegibles.

Si el resultado hay que importarlo en Sage o entregarlo en Excel, sigue con
`/entregable`.
