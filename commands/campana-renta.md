---
description: Prepara o revisa una declaración de IRPF de campaña de Renta
argument-hint: <contribuyente> <ejercicio>
---

Declaración de Renta de: **$ARGUMENTS**

Carga las skills `irpf` y `modelo-100`.

1. **Datos de partida**: datos fiscales de la AEAT, borrador y documentación aportada por
   el contribuyente. Recuerda que **los datos fiscales no son la declaración**.

2. **Situación personal y familiar a 31 de diciembre**: estado civil, descendientes con su
   fecha de nacimiento, ascendientes convivientes, grados de discapacidad, cambios del
   ejercicio (nacimientos, divorcios, defunciones). CCAA de residencia habitual.

3. **Rentas, por componente**:
   - Trabajo: todos los pagadores, gastos del art. 19, reducciones, rentas exentas
   - Capital inmobiliario: por inmueble, con gastos, amortización sobre construcción y la
     reducción del art. 23.2 con el porcentaje justificado
   - Imputación de rentas de inmuebles vacíos: 1,1 % o 2 % según revisión catastral
   - Capital mobiliario: base del ahorro, salvo el art. 25.4
   - Actividades económicas: régimen aplicable, rendimiento neto, reducciones
   - Ganancias y pérdidas: valor de adquisición con gastos, abatimiento si el elemento es
     anterior a 1995, exenciones por reinversión o por mayores de 65 años

4. **Integración y compensación**: aplica los saldos negativos pendientes de los **4
   ejercicios anteriores** y los límites del 25 % entre bloques.

5. **Reducciones y mínimos**: previsión social dentro de límites, pensiones compensatorias
   y anualidades por decisión judicial, mínimo personal y familiar (estatal y autonómico).

6. **Deducciones**: estatales y, una a una, las **autonómicas** de su comunidad. Es donde
   más devoluciones se pierden.

7. **Comparativa individual vs. conjunta**, con el resultado de ambas.

8. **Coherencia**: modelo 720/721 si hay bienes en el extranjero, con sus rentas
   declaradas; modelo 714 si el patrimonio lo exige; retenciones cuadradas con los
   certificados.

9. **Salida**: resumen del cálculo por apartados, resultado, checklist de revisión de la
   skill `modelo-100` marcado, y lista de documentación pendiente.

Si el resultado a devolver es anormalmente alto, revisa antes de dar la declaración por
buena y explica de dónde viene.
