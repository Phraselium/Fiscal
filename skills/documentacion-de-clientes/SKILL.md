---
name: documentacion-de-clientes
description: Entrada y tratamiento de la documentación que envían los clientes por sus distintos canales — contabilidad llevada en Sage, Excel del cliente, papel y PDF escaneado de facturas. Normalización a un formato importable, extracción de datos de facturas, control de lo que falta, reclamación al cliente y trazabilidad. Úsala al recibir documentación, al preparar un trimestre o cuando falte documentación para cerrar.
---

# Entrada de documentación

Los 85 clientes no entregan igual. El canal determina el trabajo, el coste y el riesgo.

| Canal | Trabajo del despacho | Riesgo principal |
|---|---|---|
| **A. Contabilidad en Sage** | Ninguno de captura: los datos ya están | Errores de imputación heredados |
| **B. Excel del cliente** | Normalizar columnas e importar | Formato distinto cada trimestre; importes como texto |
| **C. PDF escaneado** | Extraer datos factura a factura | Errores de lectura; facturas ilegibles |
| **D. Papel** | Digitalizar y luego como C | Pérdida de documentos; llega tarde |

## Regla común a todos los canales

Antes de contabilizar nada, monta el **inventario de lo recibido** y contrástalo con lo
esperado. Es más barato reclamar el día 5 del mes que descubrir el hueco el día 18.

```
Esperado = facturas emitidas por serie correlativa
         + facturas recibidas habituales (alquiler, suministros, cuotas, seguros)
         + extractos bancarios del periodo completo
         + nóminas y seguros sociales si tiene personal
Recibido = lo que ha llegado
Falta    = la diferencia  → reclamar POR ESCRITO
```

La **correlatividad de las series** de facturas emitidas es la comprobación más rentable:
un salto en la numeración es una factura no entregada, y su IVA repercutido aparecerá en
el cruce de la AEAT.

## Canal B — Excel del cliente

Antes de importar, normaliza y valida:

- [ ] Fecha de **devengo** en una columna, en formato fecha, no texto
- [ ] Importes numéricos: convierte `1.234,56` y detecta los guardados como texto
- [ ] `base × tipo = cuota` y `base + cuota = total` en cada línea
- [ ] Tipo de IVA coherente con la actividad; señala los que no encajen
- [ ] NIF de cada tercero validado (`scripts/lib/validaciones.py`)
- [ ] Naturaleza de la operación: interior / AIB / ISP / exportación / exenta. Si el Excel
      no lo distingue, **pregunta**: es lo que determina las casillas del 303
- [ ] Sin duplicados (mismo NIF, número y fecha)
- [ ] Totales contra los extractos bancarios del periodo

Guarda el Excel original tal como llegó, junto al normalizado. Si luego hay discrepancia,
la prueba de qué envió el cliente es ese fichero.

## Canales C y D — PDF escaneado y papel

De cada factura hay que extraer: fecha de expedición y de operación si difieren, número y
serie, NIF y nombre de emisor y destinatario, base por tipo, tipo, cuota, total, y las
menciones especiales (inversión del sujeto pasivo, criterio de caja, exención con su
artículo, régimen especial).

Al leer facturas escaneadas:

1. **Extrae, no interpretes.** Si un campo no se lee con seguridad, márcalo como dudoso.
   Nunca deduzcas un NIF ni un importe que no se ve.
2. **Valida aritméticamente** cada factura. La que no cuadra está mal leída o mal
   emitida; en ambos casos hay que mirarla.
3. **Valida el NIF** con su letra de control. Si no valida, es error de lectura o factura
   defectuosa.
4. Comprueba los requisitos del **art. 6 RD 1619/2012**. Sin ellos no se deduce el IVA
   (art. 97 LIVA), por mucho que la factura esté pagada.
5. Entrega siempre un **listado de excepciones**: ilegibles, incompletas, duplicadas o
   descuadradas.

**No inventes datos de una factura que no puedes leer.** Es preferible devolver 40
facturas procesadas y 3 marcadas como ilegibles que 43 con tres importes inventados: esos
tres van a la contabilidad, al 303 y al 347, y salen en el cruce de la AEAT.

## Facturas que hay que apartar siempre

| Caso | Por qué |
|---|---|
| Ticket sin NIF del destinatario | No permite deducir IVA (art. 97 LIVA) |
| Factura simplificada por encima del límite | `parametros.py ver facturacion.simplificada.limite_general` |
| A nombre del socio o de un tercero | No es gasto de la actividad |
| Combustible, restaurantes, viajes | Deducibilidad restringida (art. 96 LIVA, art. 15 LIS) |
| Vehículos | IRPF: afectación total o nada. IVA: presunción del 50 % |
| Sin fecha o sin número | No es factura |
| Proveedor de la UE sin NIF-IVA | Verificar en VIES antes de tratarla como AIB |
| Efectivo por encima del límite | Art. 7 Ley 7/2012 |
| De un ejercicio anterior | Comprobar el plazo de 4 años del art. 99 LIVA |

## Reclamación y trazabilidad

Deja rastro escrito, siempre:

```
Semana −3   Solicitud con la lista concreta de lo que falta
Semana −2   Recordatorio
Semana −1   SEGUNDO recordatorio, con la consecuencia expresa: recargo del art. 27 LGT,
            o presentación con los datos disponibles y las reservas que correspondan
Vencimiento Comunicación de qué se ha presentado, con qué datos y con qué reservas
```

Refleja el estado en el control para que la cola de trabajo sea real:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py marcar --cliente "X" --modelo 303 --estado Documentación --simular
```

## Priorizar 85 clientes

Ordena el trimestre por coste y riesgo, no alfabéticamente:

1. Canales C y D primero: son los que más tardan y los que pueden bloquearse.
2. Los que arrastran ejercicios anteriores (columnas `(2)` y `(3)` del control).
3. Los de mayor volumen, con operaciones intracomunitarias, SII o vinculadas.
4. Canal A al final: si la contabilidad está en Sage, el modelo sale solo y solo hay que
   cuadrarlo.
