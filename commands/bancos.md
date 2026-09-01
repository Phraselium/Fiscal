---
description: Convierte extractos bancarios en un documento para importar en ContaPlus (DBF) o Sage 50 (CSV)
argument-hint: <cliente> <periodo> [carpeta de extractos]
---

**$ARGUMENTS**

Carga la skill `bancos-a-contaplus` y sigue sus ocho pasos.

## Antes de nada, pide estos ficheros

| Fichero | Para qué |
|---|---|
| Extractos bancarios (xlsx, xls o csv), uno por cuenta | Los movimientos |
| Diario del ejercicio anterior del cliente (`.dbf` o `.csv`) | De aquí salen **todos** los criterios **y** el formato de salida |
| Muestra de importación, si es distinta del diario | Manda ella para el formato |

Sin los dos primeros no se empieza. El histórico no es opcional: es la única fuente de
criterio, y además es la muestra de la que sale el formato.

**El formato de salida lo decide la extensión de la muestra**: `.dbf` → `XDIARIO.DBF`
para ContaPlus; `.csv` → `XDIARIO.csv` para Sage 50. No hay ninguna especificación de
Sage escrita en la skill: todo —delimitador, codificación, columnas, formato de fecha y
separadores— sale del fichero del cliente. `generar_xdiario.py` imprime lo que ha
deducido: **enséñaselo al usuario antes de seguir**.

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
# .dbf → XDIARIO.DBF (ContaPlus) · .csv → XDIARIO.csv (Sage 50)
python3 $P/generar_xdiario.py --clasificado clasificado.json --muestra MUESTRA.DBF \
    --salida salidas/XDIARIO.DBF
python3 $P/verificar_xdiario.py salidas/XDIARIO.DBF --muestra MUESTRA.DBF \
    --diccionario dicc.json --extractos mov.json --cuentas cuentas.json --json verif.json
python3 $P/informe_revision.py --clasificado clasificado.json --cuentas cuentas.json \
    --diccionario dicc.json --extractos mov.json --verificacion verif.json \
    --salida salidas/revision.xlsx
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

Dos ficheros: el **documento para importar** (`XDIARIO.DBF` o `XDIARIO.csv`) y el
**Excel de revisión** en cuatro hojas —`Resumen` con el cuadre en fórmulas vivas,
`Notas y avisos`, `A revisar` con el texto original del extracto al lado, y
`Todos los asientos`.

## Al informar

- Di cuántos movimientos han quedado **sin identificar** y qué porcentaje del total son.
- Enumera las subcuentas que hay que **dar de alta antes de importar**.
- Señala las decisiones de criterio pendientes.
- **No digas que algo está contabilizado.** Está pendiente de revisar e importar.

Los extractos llevan IBAN, números de tarjeta y nombres de empleados: pasa
`comprobar_privacidad.py` antes de escribir nada en el repositorio.
