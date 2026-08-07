---
name: modelo-347
description: Modelo 347, declaración anual de operaciones con terceras personas — umbral de 3.005,06 €, claves de operación, desglose trimestral, operaciones excluidas, arrendamientos de local de negocio, cobros en efectivo, criterio de caja, exonerados por SII, discrepancias con la contraparte y generación del fichero. Úsala en febrero para preparar, cuadrar o generar el 347.
---

# Modelo 347 — Operaciones con terceras personas

## 1. Quién y cuándo

- Obligados: empresarios y profesionales que hayan realizado operaciones con un mismo
  tercero por importe **superior a 3.005,06 €** en el año natural, computando por
  separado entregas y adquisiciones.
- **Plazo: febrero.** ⚠️ Verifica la convocatoria del ejercicio: la fecha exacta ha
  variado (todo febrero, o solo hasta el día 28/29).
- **Exonerados**: quienes lleven los libros registro por el **SII**, quienes no realicen
  operaciones que superen el umbral, y las personas físicas y entidades en atribución de
  rentas en régimen de estimación objetiva y simplificado de IVA por sus operaciones
  fuera de la actividad empresarial.

## 2. Qué se declara

| Se incluye | No se incluye |
|---|---|
| Entregas y adquisiciones de bienes y servicios, **IVA incluido** | Operaciones ya declaradas en el **349** |
| Subvenciones recibidas de las Administraciones Públicas | Operaciones sometidas a retención declaradas en 190, 180, 193 |
| Arrendamientos de **local de negocio** (con referencia catastral) | Importaciones y exportaciones (van por DUA) |
| Anticipos recibidos y satisfechos | Operaciones realizadas al margen de la actividad |
| Operaciones de seguro | Entregas de energía eléctrica y agua a domicilio |
| Cobros por cuenta de terceros > 300,51 € | Operaciones de quienes llevan SII |
| Operaciones con inversión del sujeto pasivo | Arrendamientos de **vivienda** exentos |
| Operaciones exentas de IVA | |

## 3. Claves de operación

| Clave | Significado |
|---|---|
| **A** | Adquisiciones de bienes y servicios |
| **B** | Entregas de bienes y prestaciones de servicios |
| **C** | Cobros por cuenta de terceros |
| **D** | Adquisiciones efectuadas por entidades públicas |
| **E** | Subvenciones, auxilios y ayudas satisfechas por entidades públicas |
| **F** | Ventas de agencias de viaje |
| **G** | Compras de agencias de viaje |

## 4. El desglose trimestral

Los importes se declaran **por trimestres naturales de devengo**, aunque el umbral de
3.005,06 € se compruebe sobre el total anual. Un cliente al que se le facturó
1.500 € cada trimestre entra en el 347 aunque ningún trimestre supere el umbral.

Excepción: las operaciones en **régimen especial del criterio de caja** se declaran
además por el importe efectivamente cobrado o pagado, en el apartado específico y con el
desglose que corresponda.

## 5. La causa nº 1 de requerimiento: la discrepancia

La AEAT cruza automáticamente el 347 de cada declarante con el de su contraparte.
Cualquier diferencia genera un requerimiento. Causas habituales:

| Causa | Cómo evitarla |
|---|---|
| Criterio de imputación distinto (fecha de factura vs. fecha de contabilización) | Ambas partes deben usar la fecha de **devengo**, no la de pago ni la de registro |
| Facturas de diciembre contabilizadas en enero | Periodifica correctamente en el cierre |
| Una parte incluye el IVA y la otra no | El 347 va **siempre con IVA** |
| Rappels y descuentos aplicados por una sola parte | Confirma el neto anual con el cliente/proveedor |
| Una parte lleva SII y la otra no | El del SII está exonerado; la diferencia es esperada y se explica |
| Operaciones con inversión del sujeto pasivo | Se declaran por la base, sin IVA repercutido |

**Práctica del despacho**: cuando un tercero se acerque o supere el umbral, envía
confirmación del importe anual antes de presentar. Un correo con el desglose trimestral
resuelve el 347 y sirve de prueba si luego llega el requerimiento.

## 6. Arrendamientos de local de negocio

El arrendador que perciba rentas de local de negocio sujetas a retención las declara en
el **180**, no en el 347. Pero si no están sujetas a retención (por alguna de las
excepciones del art. 75.3.g RIRPF), sí van al 347, consignando la **referencia catastral**
y la situación del inmueble.

## 7. Generar el fichero

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_informativa.py \
  --modelo 347 --ejercicio 2025 \
  --declarante clientes/<NIF>/declarante.json \
  --detalle    clientes/<NIF>/terceros.csv \
  --salida     salidas/347-2025.txt \
  --acepto-diseno-no-verificado
```

Columnas: `nif_declarado`, `apellidos_nombre_declarado`, `codigo_provincia`,
`clave_operacion`, `importe_anual` y, si procede, `codigo_pais`. El diseño incluido es
**borrador** en el bloque de importes trimestrales: contrástalo con el anexo de la orden
vigente antes de usarlo.

## 8. Checklist

- [ ] Extracto de mayor de clientes y proveedores del ejercicio, ordenado por importe
- [ ] Filtro > 3.005,06 € aplicado por tercero y por sentido (A y B por separado)
- [ ] Importes **con IVA**
- [ ] Operaciones intracomunitarias **excluidas** (van al 349)
- [ ] Retenciones declaradas en 190/180/193 **excluidas**
- [ ] Cobros en efectivo > 6.000 € del mismo tercero identificados y declarados
- [ ] Subvenciones públicas recibidas incluidas
- [ ] Desglose por trimestre de devengo, no de cobro
- [ ] NIF validados
- [ ] Confirmación enviada a los terceros cercanos al umbral
