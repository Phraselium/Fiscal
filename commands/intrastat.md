---
description: Prepara y genera la declaración Intrastat de un periodo
argument-hint: <cliente> <periodo AAAA-MM> [introduccion|expedicion]
---

Prepara el Intrastat de: **$ARGUMENTS**

Carga la skill `intrastat`.

1. **Obligación**: comprueba el acumulado **del año** por flujo frente al umbral
   (400.000 € — verifica el vigente). Recuerda que los flujos de introducción y
   expedición son independientes, y que la obligación, una vez nacida, se mantiene todo
   el año siguiente.

2. **Reunir los movimientos** del periodo: facturas de compra y de venta a Estados
   miembros, más las transferencias de bienes propios sin factura.

3. **Depurar**: excluye servicios (van al 349, no a Intrastat), operaciones con terceros
   países (DUA), y movimientos con Canarias, Ceuta y Melilla. Incluye devoluciones con su
   naturaleza de transacción propia, no como ventas negativas.

4. **Completar cada línea**: Estado miembro, país de origen de la mercancía, provincia,
   incoterm, naturaleza de la transacción, modalidad de transporte, código **NC8**
   contrastado con el TARIC del año en curso, masa neta, unidades suplementarias si la
   partida las exige, importe facturado y estadístico, régimen y **NIF-IVA de la
   contraparte** (obligatorio en expedición).

5. **Generar**, un fichero por flujo:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_intrastat.py --flujo <introduccion|expedicion> \
     --periodo AAAA-MM --declarante <J> --lineas <CSV> --salida salidas/<...>.csv
   ```
   El script valida y aborta si encuentra incidencias; resuélvelas antes de forzar.

6. **Cuadrar** con el modelo 349 y con las casillas 59/60 del 303 del periodo,
   explicando las diferencias (servicios, operaciones no Intrastat).

7. **Informar** del plazo: días **1 a 12** del mes siguiente, y del siguiente paso —
   subir el fichero al portal Intrastat de la sede electrónica de Aduanas e II.EE.

Si en un periodo obligado no hubo operaciones, recuerda que hay que presentar declaración
**sin operación**.
