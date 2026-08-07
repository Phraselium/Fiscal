---
name: intrastat
description: Declaración Intrastat de intercambios de bienes intracomunitarios — obligación y umbrales, flujos de introducción y expedición, datos de cada línea (código NC8, naturaleza de la transacción, condiciones de entrega, modalidad de transporte, país de origen, NIF-IVA de la contraparte, masa neta, unidades suplementarias, valor facturado y estadístico), plazos, rectificaciones, relación con el modelo 349 y generación del fichero CSV listo para subir al portal de Aduanas. Úsala para preparar, revisar o generar cualquier declaración Intrastat.
---

# Intrastat

Declaracion **estadistica** de movimientos fisicos de **bienes** entre Estados miembros.
Gestion: Departamento de Aduanas e II.EE.

| Intrastat | Modelo 349 |
|---|---|
| Solo **bienes** | Bienes **y servicios** |
| Solo si se superan umbrales | Cualquier importe |
| Dias 1-12 del mes siguiente | Dias 1-20 |

## Obligacion

Dos flujos **independientes**: INTRODUCCION (llegadas) y EXPEDICION (salidas).

```bash
python3 scripts/parametros.py ver intrastat.umbral_exencion
```

Umbral de **400.000 €** anuales por flujo. La obligacion nace **el mes en que se supera** y
se mantiene el resto del ano y **todo el ano siguiente**. Verifica el umbral cada ejercicio.

En un mes obligado sin operaciones se presenta declaracion **sin operacion**. No presentar
nada es una falta.

## Datos criticos de cada linea

- **Codigo NC8**: 8 digitos. Contrastalo con el **TARIC del ano en curso**: cambia cada
  1 de enero. No lo copies del ejercicio anterior.
- **NIF-IVA de la contraparte** y **pais de origen de la mercancia**: obligatorios en
  expedicion desde 2022.
- Naturaleza de la transaccion, modalidad de transporte, incoterm, provincia, masa neta
  (o unidades suplementarias si la partida las exige), importe facturado y estadistico.

## Que NO entra

Servicios (van al 349), transito, muestras sin valor, terceros paises (DUA), y movimientos
con **Canarias, Ceuta y Melilla**. Si entran: transferencias de bienes propios sin factura,
perfeccionamiento en ambos sentidos y devoluciones con su naturaleza propia.

## Generar

```bash
python3 scripts/generar_intrastat.py --flujo expedicion --periodo AAAA-MM \
  --declarante <json> --lineas <csv> --salida salidas/intrastat-D-AAAA-MM.csv
```

Un fichero por flujo. El script valida y aborta si hay incidencias (NC8 mal, Estado miembro
inexistente o `ES`, importe cero, falta el NIF-IVA en expedicion). Contrasta las columnas
del fichero de carga con la **guia Intrastat del ejercicio** antes del primer envio del ano.

Despues: subir al portal Intrastat de la sede de Aduanas, que valida linea a linea.

## Cuadre

Entregas de bienes del 349 ↔ Intrastat de expedicion. La diferencia debe explicarse por
servicios y por operaciones no sujetas a Intrastat. Si no se explica, hay un error en uno
de los dos.

## Detalle

`references/detalle.md` — tabla completa de datos por linea, casuistica de que se incluye y
que no, rectificaciones, regimen sancionador y checklist mensual.
