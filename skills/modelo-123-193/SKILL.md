---
name: modelo-123-193
description: Modelos 123 y 193, retenciones sobre rendimientos del capital mobiliario y su resumen anual — dividendos, intereses de préstamos de socios, propiedad intelectual e industrial, arrendamiento de bienes muebles y negocios, tipo del 19 %, momento del devengo, distribución de dividendos y reparto de reservas, y generación del fichero. Úsala para retenciones de dividendos e intereses.
---

# Modelos 123 y 193 — Retenciones del capital mobiliario

## 1. Qué se retiene

| Concepto | Tipo |
|---|---|
| **Dividendos** y participaciones en fondos propios | 19 % |
| Intereses de préstamos, incluidos los de socios a la sociedad | 19 % |
| Rendimientos de la propiedad intelectual e industrial (cuando no sean de actividad económica) | 19 % |
| Arrendamiento de **bienes muebles**, negocios o minas | 19 % |
| Cesión del derecho de explotación de la imagen | 24 % |
| Rentas de operaciones de capitalización y seguros | 19 % (modelo 128/188) |

| Modelo | Objeto | Plazo |
|---|---|---|
| **123** | Autoliquidación periódica | 1–20 de abril, julio, octubre y enero (mensual si gran empresa) |
| **193** | Resumen anual | 1–31 de enero |

## 2. Momento del devengo — el punto crítico

La retención se devenga cuando los rendimientos son **exigibles**, o en el momento del
cobro si es anterior (art. 94 RIRPF).

- **Dividendos**: la retención se devenga en la fecha acordada por la junta general para
  el pago. Si la junta acuerda repartir sin fijar fecha, se entiende exigible el día
  siguiente al acuerdo. **No** cuando materialmente se transfiere el dinero.
- **Intereses de préstamos de socios**: se devengan conforme a lo pactado. Si el contrato
  no fija fecha, la DGT considera exigibles los intereses al cierre de cada anualidad. Un
  préstamo de socio **sin intereses** exige el ajuste por operación vinculada (art. 18
  LIS) y puede generar retención sobre el interés imputado.

Presentar el 123 tarde por confundir el devengo con el pago es un error habitual y caro:
la deuda es **inaplazable**.

## 3. Reparto de dividendos — secuencia completa

```
1. Verificar que hay reservas disponibles y que se ha dotado la reserva legal
2. Acuerdo de la junta general, con fecha de pago expresa
3. Retención del 19 % en la fecha de exigibilidad
4. Modelo 123 en el trimestre del devengo
5. Certificado de retención al socio
6. Modelo 193 en enero
7. El socio persona física: base del ahorro en su IRPF
   El socio sociedad: exención del art. 21 LIS al 95 % si participa ≥ 5 % y 1 año
```

⚠️ Si el socio es una sociedad con derecho a la exención del art. 21 LIS y participación
≥ 5 % mantenida 1 año, **no procede practicar retención** (art. 61 RIS). Verifícalo antes
de retener: retener de más obliga al socio a pedir la devolución.

## 4. Errores frecuentes

1. Repartir dividendos sin practicar retención.
2. Retener en la fecha de la transferencia y no en la de exigibilidad acordada.
3. Préstamos de socios sin contrato ni interés de mercado: ajuste por vinculación,
   retención omitida y posible calificación como retribución de fondos propios.
4. Distribuir prima de emisión o reducir capital con devolución de aportaciones y tratarlo
   como dividendo: el régimen fiscal es distinto (minora el valor de adquisición hasta el
   límite del valor de los fondos propios).
5. No presentar el 123 negativo estando de alta en la obligación censal.
6. Olvidar la exención del art. 61 RIS y retener a una matriz con participación
   cualificada.

## 5. Generar el fichero del 193

```bash
python3 scripts/generar_informativa.py \
  --modelo 193 --ejercicio 2025 \
  --declarante clientes/<NIF>/declarante.json \
  --detalle    clientes/<NIF>/perceptores-capital.csv \
  --salida     salidas/193-2025.txt \
  --acepto-diseno-no-verificado
```

Columnas: `nif_perceptor`, `apellidos_nombre_perceptor`, `codigo_provincia`,
`clave_percepcion` (A dividendos, B otros rendimientos, C propiedad intelectual e
industrial, D arrendamiento de muebles y negocios), `percepcion_integra`,
`retenciones_practicadas`.

## 6. Cuadre

- [ ] Σ bases de los 123 = Σ percepciones del 193
- [ ] Σ retenciones de los 123 = Σ retenciones del 193
- [ ] Dividendos declarados ↔ acta de la junta general ↔ cuenta 526/545 de la contabilidad
- [ ] Intereses declarados ↔ gasto financiero contabilizado (cuenta 662/663)
- [ ] Certificados de retención emitidos a todos los perceptores
- [ ] Socios personas jurídicas con exención verificada antes de retener
