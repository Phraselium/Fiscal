# Reglas de imputación

Se aplican **en orden**; gana la primera que case. Cada una devuelve subcuenta de
contrapartida, concepto de 25 caracteres, nombre de la regla y una marca de «revisar».

## De dónde sale el criterio

Todo el criterio sale del **XDIARIO del ejercicio anterior del propio cliente**. Nada de
criterios genéricos. `diccionario_diario.py` extrae tres cosas:

**a) Concepto → contrapartida.** Se agrupa el diario por `ASIEN`. Dentro de cada asiento,
para cada línea cuya `SUBCTA` sea de tesorería (`57*`), se busca la línea con el **mismo
`CONCEPTO` y el importe exactamente contrario**: esa es su contrapartida.

> El emparejamiento por importe es imprescindible: los asientos agrupan varios pagos del
> día y el campo `CONTRA` viene casi siempre vacío.

Se descartan los asientos de apertura, regularización y cierre.

**b) Nombre de tercero → subcuenta.** De las líneas `400*` y `410*` (excluidas las
transitorias `4009*`) se limpia el concepto de los prefijos `P/S.FRA.`, `S/FRA.`, `REC.`,
`RECIBO` y de los números de factura, y se trocea el resto en palabras de **4 o más
letras**. Cada palabra apunta a una subcuenta. Se acepta cuando es **unánime**, o cuando
gana con al menos el **60 %** y **dos apariciones**.

Se descartan como tokens los nombres de municipio y las palabras genéricas —VALENCIA,
ALBORAYA, MADRID, CENTRO, GRUPO, DISTRIBUCIONES, MAYORISTA, BAZAR, PUNT…—: son la primera
fuente de errores.

**c) Empleados.** De los conceptos `P/NOMINAS MES <NOMBRE>` salen los nombres de pila que
aparecen en nómina, para reconocer después las transferencias a empleados.

## Extracción del tercero

Antes de buscar en el diccionario hay que sacar el nombre del tercero del texto. Patrones
que se cubren:

| Patrón | Ejemplo |
|---|---|
| `ADEUDO RECIBO X` | ADEUDO RECIBO ELECTRICA DEL SUR SL |
| `TRANSFERENCIA A X` | TRANSFERENCIA A SUMINISTROS DEL NORTE |
| `ABONO TRANSFERENCIA DE X` | ABONO TRANSFERENCIA DE CLIENTE PRINCIPAL SA |
| `TRANSFERENCIA INMEDIATA A FAVOR DE X` | |
| `RECIBO X Nº RECIBO…` | RECIBO ASEGURADORA GENERAL Nº RECIBO 4471 |
| `COMPRA TARJ. <tarjeta> X` | COMPRA TARJ. 5402 FERRETERIA CENTRAL, |
| `PAGO MOVIL EN X,` | |
| `COMPRA X,` | |
| `ELECTRICIDAD X -` | |
| `TRANSFERENCIA OTRA ENTIDAD … BENEF: X` | |
| `TRANSFERENCIAS X` | |
| `PAGO PUNTUAL RECIBO DE X` | |

**Coincidencia aproximada.** Si ninguna palabra casa exacta, se admite `difflib` con corte
**0,85** —resuelve AYVENS/AYWENS, DISCALMAQ/DIVALMARQ— y esos movimientos se marcan
**siempre** para revisar.

## La tabla

| # | Detecta | Contrapartida | Concepto |
|---|---|---|---|
| 1 | Abono de remesa de TPV (`ABONO TPV`, `LIQUIDACION REMESA DE COMERCIOS`, `FACT.TPV`) | Caja `570*` | `ABONO REMESA TPV` |
| 2 | Comisión de TPV (`COMISIONES <nº comercio>`, `COMI.TPV`) | Servicios bancarios `626*` | `COMIS VAR REMESAS` |
| 3 | Comisiones y gastos bancarios, liquidación de contrato, gestión de devoluciones | `626*` | `COMIS VARIAS` |
| 4 | Retrocesión de apunte | `626*` | `RETROC COMISIONES` |
| 5 | Liquidación de intereses | Ingreso financiero si es a favor, gasto si es en contra | `ABONO INTERESES` |
| 6 | TGSS, seguros sociales, Tesorería de la Seguridad Social | Régimen general `476*` / autónomos `4760001` | `P/SEG.SOC.<MES/AA>` |
| 7 | Nómina, finiquito, adelanto, o pago de nóminas por cuenta del banco | Remuneraciones pendientes `465*` | `P/NOMINAS MES <NOMBRE>` |
| 8 | Ingreso o retirada de efectivo, cajero, depósito auditado | Caja `570*` | `TRASP DE CJA` / `TRASP A CJA` |
| 9 | Nombre de un socio | Cuenta con socios `551*` | `P/S.CTA.SOCIO <NOMBRE>` |
| 10 | Traspaso entre cuentas propias | Se resuelve en la pasada global | `TRASPASO BANCOS` |
| 11 | Impuestos con modelo identificable | Cuenta `475*` del modelo | `P/MOD <nnn>` |
| 12 | Ayuntamiento, tasas municipales | Tributos `631*` | `P/REC.AYUNTAMIENTO` |
| 13 | Estación de servicio | Combustible según histórico | `P/S.FRA.COMBUSTIBLE` |
| 14 | Valores e inversiones (bróker, custodia, cupones) | Según histórico | — |
| 15 | Proveedor identificado en el diccionario | Su subcuenta | `P/S.FRA.<NOMBRE>` |
| 16 | Transferencia a nombre de un empleado conocido | `465*` | `P/NOMINAS MES <NOMBRE>` · **revisar** |
| 17 | Todo lo demás | **Cuenta puente** | Texto del extracto recortado |

Modelos de la regla 11: retenciones de trabajo → **111**, arrendamientos → **115**,
capital mobiliario → **123**, IVA → **303**, Impuesto sobre Sociedades → **200/202**.
Si se reconoce la AEAT pero no el modelo, va a la cuenta de Hacienda acreedora y se marca
para revisar.

## Reglas especiales

### Compras con tarjeta
Solo se imputan a la cuenta de un proveedor cuando el comercio está identificado **sin
ninguna duda** en el histórico. Se mantiene una **lista blanca** de comercios validados
por el usuario; todo lo demás va a la cuenta puente.

> Cargar una compra con tarjeta contra la cuenta del proveedor **descuadra su saldo** si
> no hay factura detrás. Pregunta si esas compras deben ir a compras (600) o a gastos.

### Cobros contra cuentas de proveedor
Un abono cuyo tercero está en el diccionario de proveedores es **sospechoso**: puede ser
un rappel, una devolución o un cliente distinto. Se imputa, pero se marca para revisar.

### Traspasos entre cuentas propias
Un traspaso aparece **dos veces**, una en cada extracto. Se empareja el cargo con el abono
por importe contrario, cuentas distintas y fecha dentro de **±5 días**, y se genera **un
solo asiento**, el del lado del pago, con la otra cuenta bancaria como contrapartida. El
otro movimiento se marca como ya contabilizado, queda fuera del fichero y se recoge en el
informe.

Un traspaso sin pareja —típico a fin de periodo, cuando la contrapartida cae en el mes
siguiente— va a la cuenta puente y se marca para revisar.

> Esta pasada es **global**, sobre todos los movimientos ya clasificados. Hacerla
> movimiento a movimiento durante la clasificación duplica o pierde apuntes, y los bancos
> dejan de cuadrar.

## Ejemplos de texto por banco

| Banco | Texto tal como llega |
|---|---|
| Ibercaja | `RECIBO ASEGURADORA GENERAL SA Nº RECIBO 000447112` |
| Ibercaja | `LIQUIDACION REMESA DE COMERCIOS 0012345` |
| BBVA | `TRANSFERENCIA OTRA ENTIDAD  BENEF: SUMINISTROS DEL NORTE SL` |
| BBVA | `COMPRA TARJ. 5402 FERRETERIA CENTRAL, VALENCIA` |
| Santander | `ADEUDO RECIBO ELECTRICA DEL SUR SL` |
| Santander | `PAGO MOVIL EN PANADERIA LA ESPIGA, ALBORAYA` |
| Sabadell | `TRANSFERENCIA A NOMINA MES JUNIO GARCIA` |
| Sabadell | `LIQUIDACION DE INTERESES Y COMISIONES` |

En el último ejemplo, `VALENCIA` y `ALBORAYA` son palabras de parada: no identifican al
comercio, y por eso esos dos movimientos acaban en la cuenta puente salvo que el comercio
esté en la lista blanca.
