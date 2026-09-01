---
description: Convierte extractos bancarios en un XDIARIO.DBF para importar en ContaPlus
argument-hint: <cliente> <periodo> [carpeta de extractos]
---

**$ARGUMENTS**

Carga la skill `bancos-a-contaplus` y sigue sus ocho pasos.

## Antes de nada, pide estos tres ficheros

| Fichero | Para qué |
|---|---|
| Extractos bancarios (xlsx, xls o csv), uno por cuenta | Los movimientos |
| XDIARIO del ejercicio anterior del cliente (`.dbf`) | De aquí salen **todos** los criterios |
| Fichero muestra de importación (`.dbf`) | De aquí sale la estructura del fichero a generar |

Sin los tres no se empieza. El histórico no es opcional: es la única fuente de criterio.

Después, con `AskUserQuestion` y recomendación por defecto: nivel de mapeo (por histórico
y lo dudoso a puente), estructura de asientos (uno por movimiento con dos apuntes),
subcuenta de cada banco nuevo, cuenta puente (`5550000`), periodo y asiento inicial (1).
Si nadie contesta, aplica los valores por defecto y **dilo al principio del entregable**.

## El flujo

```bash
P="${CLAUDE_PLUGIN_ROOT:-.}"/scripts/bancos
python3 $P/leer_extractos.py extractos/ --json mov.json
python3 $P/diccionario_diario.py XDIARIO_ANT.dbf --json dicc.json
python3 $P/clasificar_movimientos.py --movimientos mov.json --diccionario dicc.json \
    --cuentas cuentas.json --salida clasificado.json
python3 $P/generar_xdiario.py --clasificado clasificado.json --muestra MUESTRA.DBF \
    --salida salidas/XDIARIO.DBF
python3 $P/verificar_xdiario.py salidas/XDIARIO.DBF --muestra MUESTRA.DBF \
    --diccionario dicc.json --extractos mov.json --cuentas cuentas.json --json verif.json
python3 $P/informe_revision.py --clasificado clasificado.json --cuentas cuentas.json \
    --diccionario dicc.json --extractos mov.json --verificacion verif.json \
    --salida salidas/README.md
```

Entre el paso 1 y el 3, **enseña la tabla de identificación de cuentas** (banco, cuenta
del extracto, saldo inicial, subcuenta, saldo de cierre del histórico) y espera
confirmación. Si algún saldo no cuadra, párate: el histórico no está cerrado o faltan
movimientos.

## Antes de entregar

La verificación es **obligatoria** y tiene diez comprobaciones. Si falla una sola, no se
entrega. Después, lanza el agente `revisor-fiscal` con el informe y los movimientos de
mayor importe.

## Qué se entrega

Dos ficheros y nada más: **`XDIARIO.DBF`** y un **`README.md`** al lado. Sin Excel y sin
borrador de correo: el README ya lleva los pasos previos a importar, el cuadre por banco,
la verificación, la cuenta puente desglosada y los movimientos a revisar con el texto
original del extracto.

## Al informar

- Di cuántos movimientos han quedado **sin identificar** y qué porcentaje del total son.
- Enumera las subcuentas que hay que **dar de alta antes de importar**.
- Señala las decisiones de criterio pendientes.
- **No digas que algo está contabilizado.** Está pendiente de revisar e importar.

Los extractos llevan IBAN, números de tarjeta y nombres de empleados: pasa
`comprobar_privacidad.py` antes de escribir nada en el repositorio.
