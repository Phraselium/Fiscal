---
description: Contrasta el diseño de registro de un modelo con la orden oficial y lo marca como verificado
argument-hint: <número de modelo>
---

Verificación del diseño de registro del modelo: **$ARGUMENTS**

Los diseños de `disenos/` se distribuyen como **borradores** (`"verificado": false`) y el
generador se niega a usarlos sin `--acepto-diseno-no-verificado`. Este comando los
contrasta con la fuente oficial.

1. Lee `disenos/<modelo>.json`: campo `fuente`, `aviso` y la lista
   `pendiente_verificacion`.

2. **Localiza el anexo oficial de diseños de registro**: la orden ministerial que aprueba
   el modelo y sus modificaciones posteriores, en el BOE y en la ficha del modelo en la
   sede electrónica de la AEAT. Usa WebFetch o WebSearch si están disponibles; si no,
   pide al usuario el PDF del anexo.

3. **Contrasta campo a campo**: posición inicial, posición final, tipo (alfanumérico,
   numérico, importe, signo, constante), y las tablas de claves admitidas.

4. **Corrige el JSON**. Recuerda:
   - Los campos deben cubrir **exactamente** 1..250 en cada registro; `Diseno.comprobar()`
     falla al cargar si hay hueco o solapamiento
   - Los tramos sin uso van como `{"tipo": "X"}`
   - Los importes van como `"I"` (en céntimos) con su `"S"` de signo apuntando al campo
     mediante `campo_importe`

5. **Prueba**: genera un fichero con 2-3 registros de ejemplo, valídalo con
   `scripts/validar_fichero.py --modelo <M> --detallar 3` y revisa visualmente que ningún
   campo está desplazado.

6. **Marca como verificado** solo si has contrastado todos los bloques: pon
   `"verificado": true` y añade `"verificado_el"` con la fecha y `"verificado_contra"` con
   la referencia exacta de la orden. Vacía `pendiente_verificacion`.

7. Advierte al usuario de que la comprobación definitiva la hace el validador del
   formulario del modelo en la sede electrónica al importar el fichero, y de que conviene
   hacer una prueba real antes de la primera presentación de cada campaña.

Si no has podido contrastar algún bloque, **no** marques el diseño como verificado:
actualiza `pendiente_verificacion` con lo que queda.
