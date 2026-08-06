---
description: Analiza una notificación de Hacienda y prepara la contestación
argument-hint: <ruta del PDF o descripción de la notificación>
---

Analiza la notificación: **$ARGUMENTS**

Carga la skill `procedimientos-tributarios` y sigue este orden:

1. **Identificación**
   - Órgano emisor, delegación, número de expediente y CSV
   - Obligado tributario y su NIF
   - Concepto, modelo, ejercicio y periodo afectados
   - Tipo de acto: requerimiento de información, propuesta de liquidación, trámite de
     audiencia, acuerdo de liquidación, inicio de sancionador, providencia de apremio,
     diligencia de embargo

2. **Procedimiento**: verificación de datos, comprobación limitada, comprobación de
   valores, inspección, sancionador o recaudación. Indica su **alcance**, su **duración
   máxima** y si tiene **efecto preclusivo**.

3. **Plazo**: calcula la fecha de notificación (fecha de acceso, o día 11 desde la puesta
   a disposición si no se accedió), el vencimiento y la fecha límite interna. Usa
   `scripts/calcular_plazos.py`. Indica si cabe **ampliación de plazo** (art. 91 RGAT) y
   hasta cuándo puede solicitarse.

4. **Qué pide exactamente**: lista literal de lo requerido. Nada más.

5. **Análisis de fondo**: ¿tiene razón la Administración? Normativa aplicable con
   artículos, doctrina de la DGT o del TEAC que apoye cada posición, y jurisprudencia si
   la hay.

6. **Cuantificación del riesgo**: cuota, recargo o sanción, intereses de demora,
   exposición total, y efecto de las reducciones del art. 188 LGT si se diera conformidad.

7. **Opciones**, con recomendación razonada:
   - Aportar lo requerido y allanarse
   - Aportar y alegar
   - Conformidad con reducción
   - Recurso de reposición o reclamación económico-administrativa
   - En su caso, regularización voluntaria antes de que avance el procedimiento

8. **Borrador del escrito**: HECHOS → FUNDAMENTOS DE DERECHO → SOLICITA → documentos que
   se acompañan, con la plantilla de la skill.

9. **Acciones y responsables**, con fechas.

No aportes documentación de terceros no requerida ni reconozcas hechos no acreditados.
