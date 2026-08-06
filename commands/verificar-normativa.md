---
description: Verifica en fuente oficial los parámetros fiscales y actualiza el fichero de referencia
argument-hint: [ejercicio] [ámbito, p. ej. IRPF, IVA, IS, módulos, CCAA]
---

Verificación de normativa: **$ARGUMENTS**

`config/parametros-fiscales.md` es una referencia de trabajo, no una fuente oficial. Este
comando la contrasta y la actualiza.

1. Lee `config/parametros-fiscales.md` e identifica los datos del ámbito solicitado,
   priorizando los marcados como `PENDIENTE_COMPLETAR` o con aviso de verificación.

2. **Verifica en fuente oficial** (usa WebFetch o WebSearch si están disponibles):
   - BOE consolidado de la norma
   - Sede electrónica de la AEAT y manuales prácticos del ejercicio
   - Orden anual de módulos y órdenes de aprobación de cada modelo
   - Ley de Presupuestos del ejercicio (interés de demora e interés legal)
   - Boletín de la CCAA para escalas, mínimos y deducciones autonómicas
   - Seguridad Social para los tramos de cotización del RETA

3. Presta atención especial a lo que cambia todos los años:
   - Tipos del IS de microempresa y de entidad de reducida dimensión (calendario
     decreciente de la Ley 7/2024)
   - Límites de módulos (prorrogados año a año)
   - Interés de demora y legal del dinero
   - Escalas, mínimos y deducciones autonómicas del IRPF
   - Mínimo exento y bonificaciones autonómicas del IP; vigencia del ITSGF
   - Tipos reducidos temporales del IVA
   - Calendario de VeriFactu y de la factura electrónica B2B
   - Umbrales de Intrastat y diseños de registro de las informativas

4. **Actualiza el fichero**: corrige los valores, anota la fuente y la fecha de
   verificación en cada bloque, y actualiza «Última revisión manual» y «Ejercicio de
   referencia» de la cabecera.

5. **Informe final**: tabla con los datos revisados, valor anterior, valor verificado,
   fuente y fecha. Señala expresamente los que **no** has podido verificar, para que se
   comprueben a mano.

No cambies un valor que no hayas podido verificar: márcalo como pendiente.
