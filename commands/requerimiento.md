---
description: Analiza una notificación de Hacienda y prepara la contestación
argument-hint: <ruta del PDF o descripción de la notificación>
---

**$ARGUMENTS**

Carga `procedimientos-y-plazos`.

1. **Identifica**: órgano, expediente, CSV, obligado, concepto, modelo, ejercicio y tipo
   de acto.
2. **Calcula el plazo** con `scripts/calcular_plazos.py`, y la fecha límite interna.
   Indica si cabe ampliación (art. 91 RGAT) y hasta cuándo pedirla.
3. **Qué pide exactamente**: lista literal. Nada más.
4. **Análisis de fondo** con el artículo, y doctrina o jurisprudencia si la hay.
5. **Riesgo cuantificado**: cuota + recargo o sanción + intereses, y el efecto de las
   reducciones del art. 188 LGT.
6. **Opciones con recomendación razonada**: aportar, alegar, conformidad, recurso, o
   regularización voluntaria antes de que avance el procedimiento.
7. **Borrador del escrito** con `/entregable`.

No aportes documentación de terceros no requerida ni reconozcas hechos no acreditados.
En sancionador, alega falta de motivación de la culpabilidad e interpretación razonable
de la norma.
