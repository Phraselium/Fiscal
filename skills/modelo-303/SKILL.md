---
name: modelo-303
description: Modelo 303, autoliquidación del IVA: casillas de devengado y deducible, adquisiciones intracomunitarias, inversión del sujeto pasivo, prorrata, compensación y devolución.
---

# Modelo 303 — Autoliquidación de IVA

## 1. Quién y cuándo

| Concepto | Detalle |
|---|---|
| Obligados | Todo empresario o profesional sujeto pasivo del IVA, incluso sin actividad en el periodo (se presenta **sin actividad**) |
| Periodicidad trimestral | Regla general |
| Periodicidad mensual | INCN > 6.010.121,04 € (grandes empresas), inscritos en **REDEME**, grupos de entidades y quienes lleven **SII** |
| Plazo trimestral | 1–20 de abril, julio y octubre; **4T: 1–30 de enero** |
| Plazo mensual | 1–30 del mes siguiente |
| Domiciliación | Hasta el día 15 (25 de enero para el 4T). Verificar el calendario del ejercicio |
| No obligados | Sujetos en **recargo de equivalencia** por su actividad minorista (presentan 309), y quienes solo realicen operaciones exentas sin derecho a deducción |

## 2. Estructura de casillas

### IVA devengado
| Bloque | Casillas | Contenido |
|---|---|---|
| Régimen general | 01-09 | Base y cuota por cada tipo (4 %, 10 %, 21 %) |
| Recargo de equivalencia repercutido | 16-24 | Solo si se vende a minoristas en recargo |
| Adquisiciones intracomunitarias de bienes y servicios | 10-11 | Autorrepercusión; **también** deben ir a deducible |
| Otras operaciones con inversión del sujeto pasivo | 12-13 | Ídem |
| Modificación de bases y cuotas | 14-15 | Rectificativas (signo negativo si minoran) |
| Modificación por concurso e incobrables | 25-26 | Art. 80.Tres y 80.Cuatro |
| **Total cuota devengada** | 27 | |

### IVA deducible
| Bloque | Casillas | Contenido |
|---|---|---|
| Operaciones interiores corrientes | 28-29 | |
| Operaciones interiores con bienes de inversión | 30-31 | |
| Importaciones de bienes corrientes | 32-33 | |
| Importaciones de bienes de inversión | 34-35 | |
| Adquisiciones intracomunitarias corrientes | 36-37 | |
| Adquisiciones intracomunitarias de bienes de inversión | 38-39 | |
| Rectificación de deducciones | 40-41 | |
| Compensaciones del REAGP | 42 | |
| Regularización de bienes de inversión | 43 | Solo en el último periodo |
| Regularización por aplicación del porcentaje definitivo de prorrata | 44 | Solo en el último periodo |
| **Total a deducir** | 45 | |
| **Diferencia** | 46 | 27 − 45 |

### Resultado
| Casilla | Contenido |
|---|---|
| 59 | Entregas intracomunitarias de bienes y servicios (informativa) |
| 60 | Exportaciones y operaciones asimiladas |
| 61 | Operaciones no sujetas o con inversión del sujeto pasivo que originan derecho a deducción |
| 62-63 | Operaciones en criterio de caja según devengo |
| 65 | Porcentaje de tributación a territorio común (solo si hay tributación foral) |
| 67 | Cuotas a compensar de periodos anteriores |
| 69 | Resultado |
| 70 | A deducir (declaración complementaria) |
| 71 | **Resultado de la liquidación** |
| 72 | A compensar en periodos siguientes |
| 73 | A devolver (solo 4T, o cualquier periodo si está en REDEME) |

## 3. Errores frecuentes

1. **AIB e ISP consignadas solo en devengado y no en deducible** (o al revés): salvo
   prorrata, deben ir en ambos bloques por el mismo importe. Es el error nº 1.
2. **Casilla 59 vacía** habiendo entregas intracomunitarias: descuadra con el 349 y
   genera requerimiento automático.
3. **Exportaciones en la 59** en lugar de en la 60.
4. Bienes de inversión mezclados con corrientes: impide la regularización posterior.
5. **Solicitar devolución fuera del 4T** sin estar en REDEME: se inadmite.
6. Compensación arrastrada de un periodo que ya se compensó: revisa la casilla 67 contra
   la 72 del periodo anterior, siempre.
7. Cuotas soportadas de un ejercicio anterior deducidas sin comprobar el plazo de
   **4 años** del art. 99 LIVA.
8. Facturas con IVA soportado sin factura completa en poder del destinatario: no
   deducibles aunque estén pagadas.
9. Olvidar la **regularización de prorrata y de bienes de inversión** en el último periodo.

## 4. Cuadre obligatorio antes de presentar

- [ ] Libro de facturas emitidas ↔ bases y cuotas devengadas por tipo
- [ ] Libro de facturas recibidas ↔ cuotas deducibles
- [ ] Casilla 67 ↔ casilla 72 del periodo anterior
- [ ] Casilla 59 ↔ modelo 349 del mismo periodo
- [ ] Casillas 10-11 ↔ modelo 349 (adquisiciones) ↔ facturas de proveedores UE
- [ ] Casilla 60 ↔ DUA de exportación
- [ ] Base imponible del año ↔ ingresos contables ↔ modelo 390 ↔ 200/100
- [ ] NIF-IVA de los clientes UE comprobados en **VIES a la fecha de la operación**

## 5. Régimen simplificado

Los sujetos en régimen simplificado usan el mismo 303 con el apartado específico:
- Trimestres 1 a 3: ingreso a cuenta calculado sobre los módulos a 1 de enero.
- **4T**: regularización con los módulos reales del ejercicio, la cuota mínima por
  operaciones corrientes y las cuotas soportadas por activos fijos.
- Las AIB, importaciones e ISP se liquidan **al margen** del régimen.

## 6. Presentación y pago

- Presentación electrónica obligatoria con certificado o Cl@ve.
- Resultado a ingresar: NRC de la entidad colaboradora, o domiciliación en plazo.
- Aplazamiento: posible, pero valora el coste frente al recargo. El IVA repercutido y no
  cobrado sí es aplazable (a diferencia de las retenciones del 111).
- **Sin actividad**: marca la casilla y presenta igualmente. No presentar es infracción
  del art. 198 LGT.

## 7. Complementaria vs. rectificativa

| Situación | Vía |
|---|---|
| Resultado a ingresar mayor del declarado | **Complementaria** del periodo, con recargo del art. 27 LGT |
| Resultado a ingresar menor / mayor a compensar | **Rectificación** (art. 120.3 LGT) o, si el modelo ya lo integra, autoliquidación rectificativa |
| Cuota soportada olvidada | Puede deducirse en cualquier periodo posterior dentro de los 4 años, sin complementaria |
