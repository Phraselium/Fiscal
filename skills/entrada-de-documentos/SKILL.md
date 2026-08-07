---
name: entrada-de-documentos
description: Procesar lo que mandan los clientes: PDF escaneado, Excel, papel y contabilidad en Sage. Extracción de facturas con validación, inventario de lo que falta, normalización para importar y reclamación al cliente. Úsala al recibir documentación o al preparar un periodo.
---

# Entrada de documentos

Cuatro canales, cuatro costes distintos.

| Canal | Trabajo | Riesgo principal |
|---|---|---|
| Contabilidad en **Sage** | Ninguno de captura | Errores de imputación heredados |
| **Excel** del cliente | Normalizar e importar | Formato distinto cada vez; importes como texto |
| **PDF escaneado** | Extraer factura a factura | Lectura errónea; facturas ilegibles |
| **Papel** | Digitalizar y luego como PDF | Se pierde; llega tarde |

Detalle en `references/canales-y-validacion.md`. Para Sage, `references/sage-despachos.md`.

## Lo primero, siempre: el inventario

```
Esperado = facturas emitidas por serie correlativa
         + recibidas habituales (alquiler, suministros, cuotas, seguros)
         + extractos bancarios del periodo completo
         + nóminas y seguros sociales si tiene personal
Recibido = lo que ha llegado
Falta    = la diferencia → reclamar POR ESCRITO
```

La **correlatividad de las series** es la comprobación más rentable: un salto es una
factura no entregada, y su IVA repercutido aparecerá en el cruce de la AEAT.

## Al leer facturas

1. **Extrae, no interpretes.** Si un campo no se lee con seguridad, márcalo como dudoso.
2. **Valida la aritmética**: base × tipo = cuota; suma de bases + cuotas = total.
3. **Valida el NIF** con su letra de control:
   `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/lib/validaciones.py <NIF>`
4. Comprueba los requisitos del **art. 6 RD 1619/2012**: sin ellos no se deduce el IVA.
5. Entrega siempre un **listado de excepciones**: ilegibles, incompletas, duplicadas o
   descuadradas.

**No inventes datos de una factura que no puedes leer.** Mejor 40 procesadas y 3 marcadas
como ilegibles que 43 con tres importes inventados: esos tres van a la contabilidad, al
303 y al 347, y salen en el cruce.

## Qué apartar siempre

Ticket sin NIF del destinatario · factura simplificada por encima del límite · a nombre
del socio · combustible, restaurantes y viajes · vehículos · sin fecha o sin número ·
proveedor de la UE sin NIF-IVA validado en VIES · efectivo por encima del límite ·
facturas de un ejercicio anterior fuera del plazo de 4 años.

## Priorizar 85 clientes

PDF y papel primero (son los que se bloquean), luego los que arrastran ejercicios
anteriores, luego los de más volumen o con operaciones intracomunitarias, y al final los
de Sage: ahí el modelo sale solo y solo hay que cuadrarlo.
