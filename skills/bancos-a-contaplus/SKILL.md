---
name: bancos-a-contaplus
description: Convierte los extractos bancarios de un cliente en un documento listo para importar -XDIARIO.DBF de ContaPlus o CSV de Sage 50-, deduciendo la contrapartida de cada movimiento del diario del ejercicio anterior del propio cliente. Úsala para contabilizar bancos, pasar extractos a contabilidad o preparar un fichero de importación para ContaPlus o Sage.
---

# Bancos a ContaPlus

Subordinada a `asesoria-fiscal`: no se inventan cuentas, no se inventan importes, y
nada se da por contabilizado sin revisión humana.

## Qué hace y qué no hace

**Hace**: leer los extractos, deducir la contrapartida de cada movimiento a partir del
histórico del cliente, generar el documento de importación, verificarlo y entregar un
Excel de revisión.

**No hace**: importar en ContaPlus ni en Sage, ni dar por contabilizado nada.

```
extractos + diario del ejercicio anterior (que hace de muestra)
  → identificación de cuentas → diccionario de contrapartidas → clasificación
  → documento de importación + Excel de revisión
  → REVISIÓN HUMANA → importación
```

Di siempre en qué paso estás. El fichero entregado está **pendiente de revisar e
importar**, nunca «contabilizado».

## Dos formatos de salida, un solo criterio

| Programa | Documento que se genera | De dónde sale el formato |
|---|---|---|
| ContaPlus | `XDIARIO.DBF` | Del fichero muestra `.dbf` |
| Sage 50 | `XDIARIO.csv` | Del fichero muestra `.csv` |

**El formato lo manda siempre la muestra del cliente**, nunca una especificación escrita
en esta skill. No hay ninguna «especificación de Sage 50» en el código, porque no habría
forma de verificarla: la única fuente fiable es el fichero que el cliente ya importa cada
año. `generar_xdiario.py` decide por la extensión de `--muestra` y replica delimitador,
codificación, orden y nombre de columnas, formato de fecha y separadores decimales.

Del CSV muestra se deduce además:

- **Qué columna es cada campo**, por el nombre de la cabecera (`Cuenta` → SUBCTA,
  `Contrapartida` → CONTRA…). La comparación es exacta sobre el nombre normalizado: si
  fuese por subcadena, «Contrapartida» se llevaría por delante a «Cuenta».
- La variante de **una sola columna de importe** más un indicador `D/H`, además de la de
  columnas `Debe` y `Haber` separadas.
- Las **columnas constantes** de la muestra (el diario, la empresa, la moneda), que se
  copian tal cual. Las que vienen siempre vacías se dejan vacías.

Enseña siempre al usuario el mapeo detectado antes de generar: lo imprime el propio
script. Si a la muestra le falta algún campo, **no se genera nada** y se dice cuál falta.

## Qué pedir antes de empezar

| Fichero | Para qué | ¿Obligatorio? |
|---|---|---|
| Extractos bancarios (xlsx, xls o csv), uno por cuenta | Los movimientos a contabilizar | Sí |
| Diario del ejercicio anterior del cliente (`.dbf` o `.csv`) | De aquí salen **todos** los criterios **y** el formato de salida | Sí |
| Fichero muestra de importación, si es distinto del diario | El formato exacto a generar | Solo si difiere |
| Plan de subcuentas | Nombres de cuenta para el informe | No |

Lo normal es que el fichero del año pasado sirva para las dos cosas: de él salen el mapeo
y el formato. Pídelo una vez y úsalo como `--muestra` y como histórico. Si el cliente
manda además una muestra de importación distinta, esa manda para el formato.

Y estas decisiones, con `AskUserQuestion`, todas con recomendación:

| Decisión | Opciones | Por defecto |
|---|---|---|
| Nivel de mapeo | (a) por histórico y lo dudoso a puente · (b) todo a puente · (c) solo lo repetitivo | **(a)** |
| Estructura de asientos | (a) un asiento por movimiento con dos apuntes · (b) uno por día y banco | **(a)** |
| Subcuenta de cada banco nuevo | — | Se pregunta |
| Cuenta puente | — | `5550000`, avisando de darla de alta si no existe |
| Periodo y asiento inicial | — | Todo el extracto, asiento 1 |

Si la sesión es desatendida, aplica los valores por defecto, **dilo al principio del
entregable** y sigue.

## Los ocho pasos

### 1 · Leer los extractos
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/leer_extractos.py extractos/ --json mov.json
```
Localiza la fila de cabecera buscando fecha, concepto e importe juntos; no asume una fila
fija. Cubre Ibercaja, BBVA, Santander y Sabadell, y se amplía añadiendo sinónimos a
`PISTAS`. Extrae también IBAN y titular de las primeras filas.

### 2 · Identificar qué subcuenta es cada banco
**No preguntes por el número de cuenta: dedúcelo y enséñalo cuadrado.** Para cada 572* del
histórico, saldo de cierre = Σ(EURODEBE − EUROHABER) excluyendo apertura, regularización y
cierre. Para cada extracto, saldo inicial = saldo de la primera fila − su importe. Empareja
por coincidencia **exacta** de importe:

```
Banco   Cuenta del extracto   Saldo inicial   Subcuenta   Saldo cierre histórico
```

Saldo inicial 0 y primer movimiento de apertura = **cuenta nueva**: pide la subcuenta y
avisa de darla de alta. Si algún saldo no cuadra, **párate**: el histórico no está cerrado
o faltan movimientos.

### 3 · Construir el diccionario
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/diccionario_diario.py XDIARIO_ANT.dbf --json dicc.json
```
Todo el criterio sale del histórico del cliente. Detalle en
`references/reglas-de-imputacion.md`.

### 4 · Clasificar
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/clasificar_movimientos.py \
    --movimientos mov.json --diccionario dicc.json --cuentas cuentas.json \
    --salida clasificado.json
```
17 reglas en orden; gana la primera que case. La tabla completa, con el criterio del que
sale cada una y ejemplos de los cuatro bancos, en `references/reglas-de-imputacion.md`.

### 5 · Traspasos entre cuentas propias
Se resuelven en una **pasada global** sobre todos los movimientos ya clasificados, nunca
uno a uno durante la clasificación: si no, se duplican o se pierden apuntes y los bancos
dejan de cuadrar. Ya lo hace `clasificar_movimientos.py`.

### 6 · Generar el documento de importación
```bash
# ContaPlus
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/generar_xdiario.py \
    --clasificado clasificado.json --muestra MUESTRA.DBF --salida salidas/XDIARIO.DBF

# Sage 50
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/generar_xdiario.py \
    --clasificado clasificado.json --muestra MUESTRA_SAGE.csv --salida salidas/XDIARIO.csv
```
**No se codifica el formato**: se lee del fichero muestra y se replica —byte a byte en el
DBF, columna a columna en el CSV. El script imprime lo que ha deducido de la muestra:
**enséñaselo al usuario antes de seguir**. Detalle en `references/estructura-xdiario.md`.

### 7 · Verificar — obligatorio
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/verificar_xdiario.py salidas/XDIARIO.DBF \
    --muestra MUESTRA.DBF --diccionario dicc.json --extractos mov.json --cuentas cuentas.json
```
Las mismas diez comprobaciones valen para el DBF y para el CSV: los dos se releen como
registros canónicos. **Si falla una sola, no se entrega.** La novena, el cuadre por banco
al céntimo, es la que de verdad importa.

Después, lanza el agente **`revisor-fiscal`** con el informe y una muestra de los
movimientos de mayor importe.

### 8 · Entregables — dos ficheros
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/informe_revision.py \
    --clasificado clasificado.json --cuentas cuentas.json --diccionario dicc.json \
    --extractos mov.json --verificacion verif.json --salida salidas/revision.xlsx
```

| Fichero | Qué es |
|---|---|
| `XDIARIO.DBF` o `XDIARIO.csv` | El documento listo para importar |
| `revision.xlsx` | El Excel de revisión, en cuatro hojas |

Las cuatro hojas del Excel:

| Hoja | Qué lleva |
|---|---|
| `Resumen` | Cuadre por banco **con fórmulas vivas**, no con números calculados en Python, y recuento por regla aplicada |
| `Notas y avisos` | Qué contiene el fichero, cuentas a dar de alta, comercios de tarjeta identificados, decisiones de criterio pendientes, desglose de la cuenta puente por motivo y partidas sueltas |
| `A revisar` | Lo que va a la puente y lo marcado, con el texto original del extracto al lado para poder localizarlo |
| `Todos los asientos` | La traza completa movimiento → asiento, con filtros y panel fijo |

Tipografía Arial e importes con formato `#,##0.00;(#,##0.00);-`. Si la sesión tiene
disponible una skill de hojas de cálculo, recalcula las fórmulas antes de entregar: el
cuadre del Resumen son fórmulas vivas y hay que verlas resueltas.

Todas las cifras salen del propio mapeo. Ninguna se escribe a mano.

## Reglas de prudencia

- **Ninguna cuenta ni ningún importe se inventa.** Lo que no tenga respaldo en el
  histórico va a la cuenta puente. Es mejor entregar 300 movimientos en la 555 que 300
  mal imputados.
- **Marca para revisar, como mínimo**: coincidencias aproximadas, cobros contra cuentas de
  proveedor, transferencias reconocidas solo por nombre de pila, seguros sociales cuyo
  periodo se haya deducido, impuestos sin modelo identificado, movimientos con socios y
  traspasos sin pareja.
- **Compras con tarjeta**: solo se imputan a un proveedor si el comercio está en la lista
  blanca validada por el usuario. Advierte de que cargarlas contra la cuenta del proveedor
  descuadra su saldo si no hay factura detrás, y pregunta si van a compras (600) o a gastos.
- **Di siempre** cuántos movimientos han quedado sin identificar y qué porcentaje son.
- **No afirmes que algo está contabilizado.** Está pendiente de revisar e importar.
- **Privacidad**: los extractos llevan IBAN, números de tarjeta y nombres de empleados.
  Antes de escribir nada en el repositorio:
  `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py`
