---
name: informativas-y-facturacion
description: Declaraciones informativas (modelos 347, 349, 720, 721, 232, 190, 180, 193, 184, 172/173) y obligaciones de facturación y registro — contenido obligatorio de la factura, facturas simplificadas y rectificativas, plazos de expedición, libros registro, SII, VeriFactu y sistemas informáticos de facturación, factura electrónica B2B, y limitación de pagos en efectivo. Úsala para preparar o cuadrar informativas anuales, resolver dudas de facturación o implantar VeriFactu/SII en un cliente.
---

# Informativas y facturacion

## Informativas: umbrales

```bash
python3 scripts/parametros.py buscar informativas
```

| Modelo | Umbral | Plazo |
|---|---|---|
| 347 | 3.005,06 € por tercero (6.000 € en efectivo) | Febrero |
| 349 | Cualquier importe | 1-20 siguiente al periodo |
| 720/721 | 50.000 € **por bloque** | 1 enero - 31 marzo |
| 232 | 250.000 € / 100.000 € operaciones especificas | Noviembre |
| 190/180/193 | — | Enero |

**Exonerados del 347**: quienes llevan **SII**, y las operaciones ya declaradas en 349 o
en 190/180/193. Es la causa habitual de descuadres «inexplicables» con la contraparte.

## Modelo 720: no cites el regimen antiguo

La **STJUE de 27-01-2022 (C-788/19)** anulo la sancion del 150 % y la imprescriptibilidad;
la **Ley 5/2022** las suprimio. Ahora se sanciona por el regimen general del **art. 198
LGT**. Cualquier documentacion que hable del 150 % esta obsoleta.

Reiteracion: solo se vuelve a presentar si un bloque sube **más de 20.000 €** o si se
extingue la titularidad de un elemento declarado.

## Facturacion

Contenido obligatorio: art. 6 RD 1619/2012. Sin el, **no se deduce el IVA** (art. 97 LIVA).
Simplificada: limites en `parametros.py buscar facturacion`. Plazo de expedicion: en el
momento, o antes del dia 16 del mes siguiente si el destinatario es empresario.

Rectificativas: **serie propia y separada**, identificando la factura rectificada. No se
«anula y rehace» una factura: eso es infraccion del art. 201 LGT.

## VeriFactu: fechas aplazadas DOS veces

```bash
python3 scripts/parametros.py ver verifactu.fecha_obligatoriedad
```

El RD-ley 15/2025 (BOE 03-12-2025) llevo la obligacion a **1-1-2027** (contribuyentes del
IS) y **1-7-2027** (el resto). Cualquier fuente que diga 2025 o 2026 esta desactualizada.
Verifica antes de asesorar: es la pregunta que mas hacen los clientes.

La obligacion es **del cliente que emite facturas**, no del despacho. Lo util ahora es
inventariar que software usa cada cliente y pedirle al proveedor la declaracion responsable
de cumplimiento del RD 1007/2023.

## Detalle

`references/detalle.md` — mapa completo de informativas, reglas del 347 y sus
discrepancias, libros registro, SII, guion de implantacion de VeriFactu, factura
electronica B2B y limite de pagos en efectivo.
