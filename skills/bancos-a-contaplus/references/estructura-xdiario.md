# Estructura del XDIARIO.DBF

El XDIARIO es un fichero **dBase III** (`.dbf`). Ronda los **98 campos** y su estructura
cambia entre versiones de ContaPlus.

> **Nunca la codifiques a mano.** `generar_xdiario.py` la lee del fichero muestra de
> importación del cliente y la replica byte a byte. Un fichero con la estructura
> equivocada lo rechaza ContaPlus o, peor, lo lee mal.

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
