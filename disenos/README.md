# Diseños de registro

Cada `NNN.json` describe el fichero de una declaración informativa: qué registros
tiene, qué campos ocupa cada posición y de qué tipo son. El motor
`scripts/lib/registro.py` los interpreta; **no hay lógica de ningún modelo dentro
del código**. Cuando la AEAT publica una orden que modifica un diseño, se actualiza
el JSON y no hace falta tocar los scripts.

## Estado de los diseños incluidos

Los ficheros que se distribuyen con el plugin son **borradores de trabajo**
(`"verificado": false`). Reproducen la estructura general de las informativas —el
bloque común del registro de tipo 1 (posiciones 1 a 135) es estable entre modelos—
pero **las posiciones del bloque de totales y del registro de detalle deben
contrastarse con el anexo de la orden ministerial vigente antes del primer uso en
producción**.

Los generadores se niegan a escribir un fichero con un diseño no verificado salvo
que se pase `--acepto-diseno-no-verificado`, y en todo caso imprimen el aviso.

## Cómo verificar y marcar un diseño

1. Localiza la orden vigente del modelo en el BOE (campo `fuente` del JSON) y abre
   su **anexo de diseños de registro**.
2. Contrasta campo a campo: posición inicial, posición final, tipo y, en los campos
   codificados, la tabla de claves admitidas.
3. Corrige el JSON. `Diseno.comprobar()` verifica automáticamente que los campos
   cubren 1..250 sin huecos ni solapamientos, así que un error de posición se
   detecta al cargar.
4. Genera un fichero de prueba y pásalo por el **servicio de validación de la sede
   electrónica de la AEAT** (formulario del modelo → «Importar fichero»). Ese
   validador es la comprobación definitiva, no este plugin.
5. Cuando cuadre, pon `"verificado": true` y anota `"verificado_el"` y
   `"verificado_contra"` con la referencia de la orden y la fecha.

## Tipos de campo

| Tipo | Significado | Alineación |
|---|---|---|
| `A` | Alfanumérico | Izquierda, relleno con espacios |
| `N` | Numérico entero | Derecha, relleno con ceros |
| `I` | Importe (se graba en céntimos, sin coma) | Derecha, relleno con ceros |
| `S` | Signo (`" "` positivo, `"N"` negativo) | — |
| `C` | Constante declarada en el diseño | Izquierda |
| `X` | Relleno a blancos | — |

Un campo `S` declara `campo_importe` con el nombre del campo cuyo signo representa.

## Convenciones del fichero generado

- Codificación **ISO-8859-1**, mayúsculas y sin acentos (`Ñ` y `Ç` se conservan).
- Registros de **250 posiciones**, separador **CRLF**.
- Primer registro de tipo `1` (declarante); resto de tipo `2` (detalle).
- Extensión habitual del fichero: la que indique el formulario del modelo (`.txt`).
