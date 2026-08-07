---
name: modelo-115-180
description: Modelos 115 y 180, retenciones por arrendamiento de inmuebles urbanos y su resumen anual — quién retiene, tipo del 19 %, supuestos excluidos de retención, certificado del grupo 861 del IAE, referencia catastral, plazos, cuadre y generación del fichero del 180. Úsala para preparar o revisar retenciones de alquileres de local.
---

# Modelos 115 y 180 — Retenciones por arrendamiento de inmuebles urbanos

## 1. Quién retiene

Retiene el **arrendatario** cuando es empresario o profesional y paga rentas por el
arrendamiento o subarrendamiento de **inmuebles urbanos**. Un particular que alquila una
vivienda para vivir **no** retiene.

| Concepto | Detalle |
|---|---|
| Tipo | **19 %** sobre todos los conceptos que se satisfagan al arrendador, IVA excluido |
| Modelo periódico | **115**, 1–20 de abril, julio, octubre y enero (mensual si gran empresa) |
| Resumen anual | **180**, 1–31 de enero |

La base de retención incluye la renta, los gastos repercutidos (IBI, comunidad,
suministros) y cualquier otro concepto, **excluido el IVA**.

## 2. Supuestos en que NO se retiene (art. 75.3.g RIRPF)

1. Arrendamiento de **vivienda** por empresas a sus empleados.
2. Rentas satisfechas al mismo arrendador que **no superen 900 € al año**.
   ⚠️ Si a mitad de año se prevé superarlos, hay que retener desde el principio y
   regularizar; el umbral es anual, no mensual.
3. El arrendador acredita, mediante **certificación de la AEAT**, estar obligado a
   tributar por alguno de los epígrafes del **grupo 861** del IAE («alquiler de bienes
   inmuebles») con cuota no nula, o por el epígrafe 833.3. El certificado tiene validez
   de un año: pídelo cada ejercicio y consérvalo.
4. Arrendamientos financieros (**leasing**).
5. Rentas derivadas de contratos de arrendamiento de inmuebles rústicos (no urbanos).

## 3. Errores frecuentes

1. **No retener** en el alquiler de local de negocio. Es una de las regularizaciones más
   habituales en comprobación: la AEAT lo detecta cruzando el gasto de arrendamiento
   contabilizado con la ausencia de 115.
2. Retener sobre la base **con IVA**.
3. No retener sobre los gastos repercutidos (IBI, comunidad): también forman base.
4. Aceptar la exclusión por el grupo 861 sin el certificado en el expediente.
5. Confundir el umbral de 900 € (anual, por arrendador) con un umbral mensual.
6. Alquiler de plaza de garaje o trastero anexo a la vivienda: sigue el régimen de la
   vivienda; si es independiente y el arrendatario es empresario, hay retención.
7. Olvidar la **referencia catastral** en el 180: la AEAT la exige y su ausencia genera
   requerimiento.

## 4. Modelo 180 — resumen anual

Recoge, por cada arrendador: NIF, nombre, provincia, importe íntegro satisfecho,
retenciones practicadas, y los datos del inmueble arrendado, incluida la **referencia
catastral** (obtenible en la sede del Catastro) y la situación del inmueble.

### Generar el fichero

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_informativa.py \
  --modelo 180 --ejercicio 2025 \
  --declarante clientes/<NIF>/declarante.json \
  --detalle    clientes/<NIF>/arrendadores.csv \
  --salida     salidas/180-2025.txt \
  --acepto-diseno-no-verificado
```

Columnas: `nif_perceptor`, `apellidos_nombre_perceptor`, `codigo_provincia`,
`percepcion_integra`, `retenciones_practicadas`. El bloque de datos del inmueble del
diseño incluido está pendiente de verificación: contrástalo con el anexo de la orden
antes de usarlo en producción.

## 5. Cuadre

- [ ] Σ bases de los cuatro 115 = Σ percepciones íntegras del 180
- [ ] Σ retenciones de los 115 = Σ retenciones del 180
- [ ] Gasto de arrendamiento contabilizado (cuenta 621) ↔ bases declaradas
- [ ] Referencias catastrales completas y correctas para todos los inmuebles
- [ ] Certificados de exclusión del grupo 861 archivados y vigentes
- [ ] Certificados de retenciones entregados a los arrendadores
- [ ] Arrendamientos sin retención por alguna excepción → verificar si deben ir al **347**

## 6. Del lado del arrendador

El arrendador persona física declara estas rentas como **rendimientos del capital
inmobiliario** (o de actividad económica si hay ordenación de medios) y deduce la
retención soportada en su modelo 100. Si es sociedad, como ingreso de explotación con la
retención deducible en el 200.

Si el arrendatario no retuvo debiendo hacerlo, el arrendador **puede deducir igualmente
la retención procedente** (art. 99.5 LIRPF): la responsabilidad del ingreso es del
retenedor. Consérvalo como argumento de defensa.
