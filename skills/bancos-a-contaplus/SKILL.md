---
name: bancos-a-contaplus
description: Convierte los extractos bancarios de un cliente en un fichero XDIARIO.DBF listo para importar en ContaPlus, deduciendo la contrapartida de cada movimiento del diario contable del ejercicio anterior del propio cliente. Úsala cuando haya que contabilizar bancos, pasar extractos a contabilidad o preparar un fichero de importación para ContaPlus.
---

# Bancos a ContaPlus

Subordinada a `asesoria-fiscal`: no se inventan cuentas, no se inventan importes, y
nada se da por contabilizado sin revisión humana.

## Qué hace y qué no hace

**Hace**: leer los extractos, deducir la contrapartida de cada movimiento a partir del
histórico del cliente, generar el DBF, verificarlo y entregar un informe de revisión.

**No hace**: importar en ContaPlus, ni dar por contabilizado nada.

```
extractos + XDIARIO del ejercicio anterior + fichero muestra de importación
  → identificación de cuentas → diccionario de contrapartidas → clasificación
  → XDIARIO.DBF + informe de revisión → REVISIÓN HUMANA → importación en ContaPlus
```

Di siempre en qué paso estás. El fichero entregado está **pendiente de revisar e
importar**, nunca «contabilizado».

## Qué pedir antes de empezar

| Fichero | Para qué | ¿Obligatorio? |
|---|---|---|
| Extractos bancarios (xlsx, xls o csv), uno por cuenta | Los movimientos a contabilizar | Sí |
| XDIARIO del ejercicio anterior del cliente (`.dbf`) | De aquí salen **todos** los criterios | Sí |
| Fichero muestra de importación (`.dbf`) | De aquí sale la estructura exacta a generar | Sí |
| Plan de subcuentas | Nombres de cuenta para el informe | No |

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

### 6 · Generar el fichero
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/generar_xdiario.py \
    --clasificado clasificado.json --muestra MUESTRA.DBF --salida salidas/XDIARIO.DBF
```
**No se codifica la estructura**: se lee del fichero muestra y se replica byte a byte.
Detalle del formato en `references/estructura-xdiario.md`.

### 7 · Verificar — obligatorio
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/verificar_xdiario.py salidas/XDIARIO.DBF \
    --muestra MUESTRA.DBF --diccionario dicc.json --extractos mov.json --cuentas cuentas.json
```
Diez comprobaciones. **Si falla una sola, no se entrega.** La novena, el cuadre por banco
al céntimo, es la que de verdad importa.

Después, lanza el agente **`revisor-fiscal`** con el informe y una muestra de los
movimientos de mayor importe.

### 8 · Entregables
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos/informe_revision.py \
    --clasificado clasificado.json --cuentas cuentas.json --diccionario dicc.json \
    --extractos mov.json --verificacion verif.json \
    --salida salidas/revision.xlsx --correo salidas/correo.md
```
XDIARIO.DBF · Excel de cuatro hojas (Resumen con fórmulas vivas, Notas y avisos,
A revisar, Todos los asientos) · borrador de correo para quien va a importar.

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
