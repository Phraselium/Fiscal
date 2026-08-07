# Modelo 200 — Impuesto sobre Sociedades

## 1. Quién y cuándo

- Obligados: **todas** las entidades sujetas al IS, incluidas las inactivas, las que no
  tengan ingresos y las que estén en pérdidas. También el IRNR con establecimiento
  permanente.
- **Plazo**: 25 días naturales siguientes a los 6 meses posteriores a la conclusión del
  periodo impositivo → **1 a 25 de julio** para ejercicios coincidentes con el año natural.
- Si el plazo de presentación se inicia antes de la aprobación de las cuentas, se declara
  con las cuentas formuladas y, en su caso, se presenta declaración complementaria.
- Domiciliación del pago: hasta el **20 de julio** (verificar el calendario del ejercicio).

**Exoneración parcial** (art. 124.3 LIS) para entidades parcialmente exentas del art. 9.3:
solo si concurren los tres requisitos — ingresos totales ≤ 75.000 €, ingresos de rentas no
exentas ≤ 2.000 € y todas las rentas no exentas sometidas a retención.

## 2. Bloques del modelo

| Bloque | Contenido |
|---|---|
| Caracteres de la declaración | Régimen aplicable, tipo de entidad, ERD, microempresa, consolidación, incentivos |
| Identificación y administradores | NIF, denominación, domicilio, relación de administradores y su NIF |
| **Balance** | Activo, patrimonio neto y pasivo, según el PGC o el PGC de pymes |
| **Cuenta de pérdidas y ganancias** | Resultado del ejercicio, que es el punto de partida |
| Estado de cambios en el patrimonio neto | Aplicación del resultado |
| **Liquidación (páginas 12 y ss.)** | Del resultado contable a la cuota diferencial |
| Detalle de correcciones | Cada ajuste, con su naturaleza (permanente/temporario) y su casilla |
| Compensación de BIN | Saldos pendientes por ejercicio de origen, límite aplicado y remanente |
| Deducciones | Por ejercicio de generación, límite, aplicado y pendiente |
| Información adicional | Operaciones vinculadas, régimen de entidades patrimoniales, reserva de capitalización y nivelación, ajustes de primera aplicación |

## 3. Cadena de liquidación

```
Resultado contable antes de impuestos (casilla 500)
 ± Correcciones al resultado (casillas 301-414)
 = Base imponible previa (casilla 550)
 − Reserva de capitalización (art. 25 LIS)
 − Compensación de BIN (art. 26 LIS)
 ± Reserva de nivelación (art. 105 LIS, solo ERD)
 = Base imponible (casilla 552)
 × Tipo de gravamen (casilla 558)
 = Cuota íntegra (casilla 562)
 − Deducciones por doble imposición y bonificaciones
 = Cuota íntegra ajustada positiva  → contraste con la tributación mínima (art. 30 bis)
 − Deducciones por incentivos (I+D+i, producciones, empleo con discapacidad)
 = Cuota líquida positiva (casilla 592)
 − Retenciones e ingresos a cuenta soportados
 − Pagos fraccionados (modelo 202) del ejercicio
 = Cuota diferencial (casilla 621) → a ingresar o a devolver
```

## 4. Los ajustes que más se olvidan

| Ajuste | Signo | Norma |
|---|---|---|
| Gasto por Impuesto sobre Sociedades | + | art. 15.b LIS |
| Multas, sanciones y recargos | + | art. 15.c |
| Deterioros de inmovilizado, intangible y participaciones | + (temporario) | art. 13.2 |
| Provisiones no deducibles | + (temporario) | art. 14 |
| Exceso de amortización contable sobre la fiscal | + (temporario) | art. 12 |
| Amortización acelerada y libertad de amortización | − (temporario) | arts. 102, 103 |
| Fondo de comercio: contable 10 % vs. fiscal 5 % | + | art. 12.2 |
| Liberalidades y atenciones que exceden del 1 % del INCN | + | art. 15.e |
| Gastos financieros por encima del 30 % del beneficio operativo | + | art. 16 |
| Operaciones vinculadas valoradas fuera de mercado | ± | art. 18 |
| Exención de dividendos y plusvalías (95 %) | − | art. 21 |
| Reversión de ajustes de ejercicios anteriores | − | según origen |
| Diferencias por el criterio de imputación temporal | ± | art. 11 |

**Los intereses de demora tributarios SÍ son deducibles** (STS 8-2-2021), sujetos al
límite del art. 16. No los ajustes junto con las sanciones: es un error frecuente.

## 5. Antes de presentar

- [ ] Cuentas anuales formuladas y balance de sumas y saldos cuadrado
- [ ] Impuesto contabilizado (cuentas 630, 6301, 4740, 4745, 473, 4752)
- [ ] Activos y pasivos por impuesto diferido coherentes con los ajustes temporarios
- [ ] Ajustes del ejercicio anterior que revierten, incorporados
- [ ] BIN pendientes verificadas contra las declaraciones de origen (la AEAT puede
      comprobarlas **10 años**, art. 66 bis LGT)
- [ ] Deducciones pendientes con su año de generación y plazo de caducidad (15 años,
      18 en I+D+i)
- [ ] Reserva de capitalización **contabilizada** como indisponible antes de presentar:
      si no está dotada, la reducción no procede
- [ ] Retenciones soportadas cuadradas con los certificados recibidos
- [ ] Pagos fraccionados del 202 deducidos por su importe real
- [ ] Operaciones vinculadas identificadas: ¿procede el modelo **232** en noviembre?
- [ ] Coherencia 200 ↔ 190/180/193 ↔ 347 ↔ 390 ↔ cuentas depositadas en el Registro
- [ ] Relación de administradores con NIF correctos

## 6. Después de presentar

- **Depósito de cuentas** en el Registro Mercantil: 1 mes desde la aprobación.
- **Legalización de libros**: 4 meses desde el cierre.
- Conservar la documentación **10 años** si hay BIN o deducciones pendientes, y al menos
  6 por el Código de Comercio.
- Si el resultado es a devolver, la AEAT tiene 6 meses desde el fin del plazo de
  presentación; a partir de ahí devenga intereses de demora a favor de la entidad.

## 7. Errores caros

1. Presentar sin haber dotado la reserva de capitalización.
2. Aplicar el tipo de microempresa o de ERD sin comprobar el INCN del ejercicio anterior
   (y sin verificar el tipo del calendario transitorio vigente).
3. Compensar BIN por encima del límite del 70 % / 1.000.000 €.
4. Deducir la retribución del administrador sin cobertura estatutaria.
5. Olvidar la reversión de la reserva de nivelación a los 5 años.
6. No presentar el modelo por estar la sociedad inactiva.


# Modelo 202 — Pago fraccionado del Impuesto sobre Sociedades

## 1. Plazos

**1 a 20 de abril, octubre y diciembre.** Domiciliación hasta el día 15.

Para ejercicios no coincidentes con el año natural, los plazos son los mismos: los
pagos fraccionados se refieren siempre a esos tres periodos.

## 2. Quién está obligado

- Todas las entidades sujetas al IS con **cuota positiva** en el último periodo declarado
  (modalidad del art. 40.2), o con base imponible positiva en el periodo corrido
  (modalidad del art. 40.3).
- **No hay obligación de presentar** en la modalidad del art. 40.2 si la casilla 599 del
  último modelo 200 presentado es cero o negativa. En la del art. 40.3, si el resultado
  del cálculo es cero, **sí** hay que presentar (declaración negativa).
- Entidades con INCN ≥ 6.000.000 € en los 12 meses anteriores: obligadas a la modalidad
  del art. 40.3.

## 3. Modalidad del artículo 40.2 (por defecto)

```
Base = cuota íntegra del último periodo impositivo cuyo plazo de declaración
       estuviera vencido, minorada en deducciones, bonificaciones, retenciones
       e ingresos a cuenta  (casilla 599 del modelo 200)
Pago = 18 % de esa base
```

| Pago | Última declaración a tomar (ejercicio natural) |
|---|---|
| Abril | Modelo 200 del ejercicio N−2 |
| Octubre | Modelo 200 del ejercicio N−1 |
| Diciembre | Modelo 200 del ejercicio N−1 |

⚠️ El pago de **abril** se calcula con la declaración de **hace dos años**, porque el 200
del año anterior aún no se ha presentado. Es un error habitual usar el más reciente.

## 4. Modalidad del artículo 40.3 (opcional u obligatoria)

```
Base = base imponible de los 3, 9 u 11 primeros meses del periodo impositivo,
       aplicando las normas de la LIS
Pago = base × (5/7 × tipo de gravamen), redondeado por defecto
     − retenciones e ingresos a cuenta del periodo
     − pagos fraccionados anteriores del mismo ejercicio
```

Con tipo del 25 %: 5/7 × 25 = 17,857 → **17 %**.

**Opción**: se ejerce con el modelo **036** en **febrero** del ejercicio en que deba
surtir efectos (o, si el ejercicio no es natural, en los 2 meses desde su inicio). Es
**vinculante** para ese ejercicio y para los siguientes mientras no se renuncie por el
mismo procedimiento y en el mismo plazo.

### Pago mínimo (DA 14.ª LIS)
Entidades con INCN ≥ 10.000.000 € en los 12 meses anteriores: el pago no puede ser
inferior al **23 %** del resultado contable positivo del periodo (25 % para entidades que
tributen al 30 %), minorado solo en pagos fraccionados anteriores. **Verifica los
porcentajes vigentes**: esta disposición ha sido objeto de reformas y de
pronunciamientos del Tribunal Constitucional.

## 5. Cuándo interesa cada modalidad

| Situación | Modalidad recomendada |
|---|---|
| Beneficio estable año a año | 40.2 — más simple, sin cálculo intermedio |
| Beneficio en fuerte caída respecto al año anterior | **40.3** — evita anticipar sobre un beneficio que ya no existe |
| Beneficio en fuerte crecimiento | 40.2 — difiere el pago |
| Ejercicio con pérdidas tras años de beneficio | 40.3 — el pago sería cero |
| Entidad de nueva creación sin 200 anterior | No hay obligación en 40.2 el primer año |
| INCN ≥ 6.000.000 € | 40.3, obligatoria |

La decisión se toma **en febrero** y vincula todo el año: revisa la previsión de
resultados de la cartera cada enero, antes de que se cierre el plazo de opción.

## 6. Errores frecuentes

1. Usar el 200 equivocado en el pago de abril.
2. Presentar en la modalidad 40.2 con casilla 599 negativa (no procede presentar).
3. **No** presentar en la modalidad 40.3 con resultado cero (sí procede, negativa).
4. Cambiar de modalidad sin comunicarlo en el 036 en febrero.
5. Olvidar deducir los pagos fraccionados anteriores del mismo ejercicio en la 40.3.
6. No aplicar el pago mínimo estando obligado.
7. Solicitar aplazamiento: los pagos fraccionados del IS son **inaplazables**
   (art. 65.2 LGT). Se inadmite y la deuda entra en ejecutiva.

## 7. Cierre

Los tres pagos fraccionados del ejercicio se deducen en la cuota diferencial del modelo
**200**. Verifica que el importe deducido coincide con lo efectivamente ingresado, no con
lo calculado: si un pago quedó impagado o se ingresó parcialmente, el 200 debe reflejar
la realidad.
