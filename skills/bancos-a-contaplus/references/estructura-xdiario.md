# Formato del documento de importación

Dos formatos posibles, una sola regla:

| Programa | Fichero | Motor |
|---|---|---|
| ContaPlus | `XDIARIO.DBF`, dBase III | `lib_dbf.py` |
| Sage 50 y similares | `XDIARIO.csv` | `lib_csv.py` |

> **Nunca codifiques el formato a mano.** `generar_xdiario.py` lo lee del fichero muestra
> del cliente y lo replica. Un fichero con el formato equivocado lo rechaza el programa
> o, peor, lo lee mal.

En este repositorio **no hay ninguna especificación de Sage 50 escrita a mano**, y es
deliberado: no habría forma de verificarla. La única fuente fiable del formato es el
fichero que el cliente ya importa cada año.

Los dos motores exponen la misma interfaz, y `lib_documento.py` despacha por la extensión
del fichero muestra. El resto del flujo trabaja siempre con **registros canónicos**
—`ASIEN`, `FECHA`, `SUBCTA`, `CONTRA`, `CONCEPTO`, `EURODEBE`, `EUROHABER`— así que las
diez comprobaciones de `verificar_xdiario.py` valen igual para los dos.

## El XDIARIO.DBF de ContaPlus

Ronda los **98 campos** y su estructura cambia entre versiones de ContaPlus.

## Cabecera del fichero — 32 bytes

| Posición | Contenido |
|---|---|
| 0 | Versión: `0x03` (dBase III sin memo) |
| 1-3 | Fecha de actualización: año − 1900, mes, día |
| 4-7 | Número de registros — `uint32` little-endian |
| 8-9 | Longitud de la cabecera — `uint16` little-endian |
| 10-11 | Longitud de cada registro — `uint16` little-endian |
| 12-31 | Reservado, a cero |

## Descriptor de campo — 32 bytes por campo

| Posición | Contenido |
|---|---|
| 0-10 | Nombre, rellenado con `\x00` |
| 11 | Tipo: `C` texto · `N` numérico · `D` fecha · `L` lógico |
| 12-15 | Dirección del campo (no se usa) |
| 16 | Longitud |
| 17 | Decimales |
| 18-31 | Reservado |

Tras el último descriptor va el terminador **`0x0D`**. Al final del fichero, **`0x1A`**.

## Registros

Cada registro empieza por un byte de marca de borrado: `0x20` activo, `0x2A` borrado.
Después, los campos concatenados sin separador, cada uno con su longitud fija.

### Formato de cada tipo

| Tipo | Cómo se graba |
|---|---|
| `C` | Texto en **cp850**, alineado a la izquierda, relleno con espacios, truncado a la longitud |
| `N` | `%<longitud>.<decimales>f`, alineado a la **derecha** con espacios |
| `D` | `AAAAMMDD`, o 8 espacios si va vacía |
| `L` | `F` (o `T`) |

La codificación es **cp850**, la que usa ContaPlus en España. Los conceptos van sin
acentos y en mayúsculas.

## Campos que se rellenan

Todo lo demás va a cero, `F` o espacios, según su tipo.

| Campo | Contenido |
|---|---|
| `ASIEN` | Número de asiento, correlativo sin huecos |
| `FECHA` | Fecha del movimiento |
| `SUBCTA` | Subcuenta del apunte |
| `CONTRA` | Subcuenta del **otro** apunte del asiento |
| `CONCEPTO` | Máximo 25 caracteres, sin acentos, en mayúsculas |
| `EURODEBE` / `EUROHABER` | Importe. Uno de los dos a cero |
| `PTADEBE` / `PTAHABER` | **A cero**: los importes viajan en los campos en euros |
| `MONEDAUSO` | `'2'` (euro) |
| `NIC` | `'E'` |

## Cómo se arma cada asiento

- **Dos apuntes por asiento**, consecutivos: primero el del debe, luego el del haber.
- **Ningún importe negativo.** El signo del extracto se traduce en debe o haber:

| Movimiento | Debe | Haber |
|---|---|---|
| Cargo (importe < 0): sale dinero | Contrapartida | Banco |
| Abono (importe > 0): entra dinero | Banco | Contrapartida |

- `CONTRA` de cada apunte es la subcuenta del otro.
- Numeración **correlativa sin huecos** desde el número inicial pactado, en orden
  cronológico.
- La **longitud de las subcuentas la manda el plan del cliente** (7, 8, 9 o 12 dígitos):
  se lee del histórico, no del fichero muestra.
- Los movimientos de **importe cero no generan asiento**; se listan aparte.

## Ejemplo de un asiento

Pago de 1.234,56 € a un proveedor desde el banco 5720001, contrapartida 4000012:

```
ASIEN  FECHA     SUBCTA   CONTRA   CONCEPTO              EURODEBE  EUROHABER
   47  20260315  4000012  5720001  P/S.FRA.PROVEEDOR      1234.56       0.00
   47  20260315  5720001  4000012  P/S.FRA.PROVEEDOR         0.00    1234.56
```

## Comprobación antes de entregar

`verificar_xdiario.py` relee el fichero y compara los descriptores de campo con los del
fichero muestra: si difiere uno solo, el fichero no se entrega. Es la única forma de
saber que ContaPlus podrá leerlo sin tener ContaPlus delante.

## El CSV de Sage 50

No tiene una estructura fija que replicar byte a byte, sino un conjunto de convenciones
que hay que deducir de la muestra. `lib_csv.py` detecta:

| Qué | Cómo |
|---|---|
| Codificación | Se prueban utf-8, cp1252, cp850 y latin-1. `utf-8-sig` **solo** si el fichero trae BOM de verdad: añadirlo al escribir rompe la primera cabecera |
| Delimitador | El más frecuente de `;` `,` tabulador `\|` en la primera línea |
| Fin de línea | `\r\n` si la muestra lo trae; si no, `\n` |
| Cabecera | Se exige. Sin nombres de columna no se puede saber qué es cada cosa, y se para |
| Formato de fecha | Se prueban `%d/%m/%Y`, `%d-%m-%Y`, `%Y-%m-%d`, `%d.%m.%Y`, `%Y%m%d`… contra los valores reales de la columna |
| Separadores | Decimal por mayoría; el de miles basta con que **un solo** importe venga agrupado |

### Cómo se reconoce cada columna

Por el nombre de la cabecera, normalizado (minúsculas, sin acentos ni puntuación) y
comparado **de forma exacta** contra una lista de sinónimos:

| Campo | Nombres que se reconocen |
|---|---|
| `ASIEN` | asiento, asien, nº asiento, número asiento, diario, apunte |
| `FECHA` | fecha, fecha asiento, fecha operación, fecha registro |
| `SUBCTA` | subcuenta, cuenta, cta, código cuenta, cuenta contable |
| `CONTRA` | contrapartida, contra, cuenta contrapartida |
| `CONCEPTO` | concepto, descripción, comentario, detalle, glosa |
| `EURODEBE` | debe, importe debe, cargo |
| `EUROHABER` | haber, importe haber, abono |

> La comparación es **exacta, no por subcadena**. Si fuese por subcadena, «Contrapartida»
> se llevaría por delante a «Cuenta» y todos los apuntes saldrían contra la cuenta
> equivocada. Es el error que más caro sale de todos los de este fichero.

### La variante de un solo importe

Algunas instalaciones exportan una columna `Importe` y otra `D/H` en lugar de `Debe` y
`Haber`. Se detecta sola, y las marcas de debe y haber se toman de los valores que use la
propia muestra. Internamente el registro sigue siendo canónico: el reparto se hace al
escribir.

### Columnas que no son ninguno de nuestros campos

- Si en la muestra **valen siempre lo mismo** (el diario, la empresa, la moneda), son
  constantes del formato y se copian tal cual.
- Si vienen siempre vacías, se dejan vacías.

### Un importe que no se puede leer no vale cero

Si un importe no encaja con los separadores detectados, `lib_csv.py` **para y dice cuál
es**. Devolver `0,00` en silencio es la forma más fácil de entregar un fichero que cuadra
sobre el papel y está mal.
