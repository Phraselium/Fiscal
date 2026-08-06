---
description: Genera el fichero de una declaración listo para importar en la sede de la AEAT
argument-hint: <modelo> <ejercicio/periodo> <cliente>
---

Genera el fichero de: **$ARGUMENTS**

Carga la skill `generacion-de-ficheros` (o `intrastat` si el modelo es Intrastat).

1. **Comprobar el diseño**: ¿existe `disenos/<modelo>.json`? ¿Está marcado como
   `verificado`? Si no lo está, avisa al usuario de qué bloques faltan por contrastar y
   ofrece verificarlos contra el anexo de la orden vigente antes de generar.

2. **Reunir los datos**:
   - Fichero del declarante (NIF, denominación, teléfono, persona de contacto, número
     identificativo de 13 dígitos)
   - Detalle en CSV o JSON, con las columnas que exige el diseño
   - Si los datos vienen de otro formato (nóminas, contabilidad, Excel), conviértelos
     primero y muestra la conversión al usuario para que la revise

3. **Cuadrar antes de generar** contra las autoliquidaciones periódicas del ejercicio.
   Si no cuadra, para y explica la diferencia. No generes un fichero descuadrado.

4. **Generar**:
   ```bash
   python3 scripts/generar_informativa.py --modelo <M> --ejercicio <E> \
     --declarante <J> --detalle <D> --salida salidas/<M>-<E>-<NIF>.txt
   ```

5. **Validar**:
   ```bash
   python3 scripts/validar_fichero.py salidas/<fichero> --modelo <M> --detallar 3
   ```
   Revisa visualmente el primer registro de detalle buscando desplazamientos de campo.

6. **Informar** al usuario de: ruta del fichero, número de registros, totales, incidencias
   detectadas y el siguiente paso — importarlo en el formulario del modelo en la sede
   electrónica de la AEAT, donde el validador oficial hará la comprobación definitiva.

Nunca digas que la declaración se ha presentado: lo que existe es un fichero pendiente de
importar y presentar con certificado.
