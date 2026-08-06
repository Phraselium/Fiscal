---
description: Muestra las obligaciones y plazos pendientes, o construye el calendario de un cliente
argument-hint: [cliente o NIF] [mes o trimestre]
---

Calendario fiscal: **$ARGUMENTS**

Carga la skill `calendario-fiscal`.

Si se indica un **cliente**, construye su calendario personalizado:
1. Lee sus obligaciones censales (036/037 o su ficha).
2. Determina la periodicidad (trimestral, o mensual por INCN, REDEME o SII).
3. Añade las anuales según sus circunstancias: 349 e Intrastat si opera con la UE, 232 si
   tiene vinculadas, 720/721 si tiene bienes fuera, 714/718 por patrimonio, 200 y
   obligaciones registrales si es sociedad, resúmenes anuales si retiene.
4. Para cada obligación: modelo, periodo, plazo de presentación, plazo de **domiciliación**
   y **fecha límite interna** (vencimiento − 5 días hábiles).

Si no se indica cliente, muestra el calendario general del periodo solicitado, agrupado
por fecha, incluyendo las obligaciones que no son de la AEAT: Intrastat (días 1-12),
tributos autonómicos y locales, y las obligaciones mercantiles y registrales del ejercicio.

Usa `scripts/calcular_plazos.py` para las fechas concretas y advierte de que el calendario
del contribuyente de la AEAT del ejercicio es la referencia definitiva, porque hay
adaptaciones anuales por festivos.
