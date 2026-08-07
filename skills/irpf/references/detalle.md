# IRPF — Ley 35/2006 y RD 439/2007

## 1. Determinar primero

1. **Residencia fiscal** (art. 9 LIRPF): >183 días en España, o núcleo principal de
   intereses económicos, o presunción por cónyuge e hijos menores residentes.
   Si no es residente → **IRNR**, no IRPF (modelos 210/216, skill `no-residentes`).
2. **CCAA de residencia habitual** (art. 72 LIRPF): donde haya permanecido más días
   en el periodo impositivo. Determina escala autonómica, mínimos autonómicos y
   deducciones autonómicas.
3. **Unidad familiar y modalidad**: individual vs. conjunta. Calcula ambas y compara.
4. **Regímenes especiales**: art. 93 LIRPF (impatriados, «ley Beckham»), régimen de
   atribución de rentas, transparencia fiscal internacional.

## 2. Componentes de la renta y su base

| Componente | Base | Norma |
|---|---|---|
| Rendimientos del trabajo | General | arts. 17-20 |
| Rendimientos del capital inmobiliario | General | arts. 21-24 |
| Rendimientos del capital mobiliario (dividendos, intereses, seguros) | **Ahorro** | art. 25.1-3 |
| Capital mobiliario art. 25.4 (propiedad intelectual, arrendamiento de negocio, cesión de imagen) | General | art. 25.4 |
| Capital mobiliario de entidades vinculadas (exceso 3× fondos propios) | General | art. 46 b) |
| Rendimientos de actividades económicas | General | arts. 27-32 |
| Imputaciones de renta inmobiliaria | General | art. 85 |
| Ganancias y pérdidas por transmisión de elementos patrimoniales | **Ahorro** | arts. 33-39 |
| Ganancias sin transmisión (premios, subvenciones, ayudas) | General | art. 45 |

## 3. Rendimientos del trabajo

**Gastos deducibles (art. 19)**: Seguridad Social y mutualidades alternativas, cuotas
sindicales, cuotas colegiales obligatorias (máx. 500 €), gastos de defensa jurídica
frente al empleador (máx. 300 €), y «otros gastos» 2.000 € (incrementado en movilidad
geográfica y en trabajadores activos con discapacidad).

**Reducciones (art. 20)**: reducción por obtención de rendimientos del trabajo, con
tramos decrecientes — verifica los umbrales del ejercicio en
`config/parametros-fiscales.md`.

**Reducción del 30 % (art. 18.2)**: rendimientos con periodo de generación > 2 años o
notoriamente irregulares (RD 439/2007 art. 11), sobre un máximo de 300.000 €. Ojo con
la regla de no aplicación si en los 5 años anteriores se aplicó a otro rendimiento
plurianual (salvo indemnizaciones por despido).

**Exenciones frecuentes (art. 7)**:
- Indemnización por despido, con el límite del ET y máximo 180.000 € (art. 7.e).
  Requiere que sea **obligatoria** por el ET; el despido pactado tributa.
- Prestaciones por incapacidad permanente absoluta y gran invalidez (art. 7.f).
- Trabajos efectivamente realizados en el extranjero, máx. **60.100 €** (art. 7.p) —
  incompatible en el mismo ejercicio con el régimen de excesos del art. 9.A.3.b RIRPF,
  a elección del contribuyente.
- Prestaciones por maternidad/paternidad públicas (art. 7.h).
- Rendimientos del trabajo en especie exentos (art. 42.3): comedor 11 €/día, seguro
  médico 500 €/persona (1.500 € con discapacidad), transporte colectivo 1.500 €/año,
  formación, entrega de acciones hasta 12.000 € (o 50.000 € en emergentes, Ley 28/2022).

## 4. Capital inmobiliario

- Ingresos íntegros − gastos deducibles (art. 23.1): intereses y financiación y gastos
  de reparación y conservación **limitados conjuntamente al importe de los ingresos**
  del inmueble (el exceso se deduce en los 4 años siguientes con el mismo límite);
  tributos y tasas, comunidad, seguros, suministros no repercutidos, servicios
  personales, saldos de dudoso cobro (6 meses), amortización 3 % sobre el mayor de
  coste de adquisición o valor catastral, excluido suelo.
- **Reducción por arrendamiento de vivienda (art. 23.2)**: régimen reformado por la
  Ley 12/2023 — porcentajes 50 / 60 / 70 / 90 % según supuesto y con régimen
  transitorio para contratos anteriores al 26-05-2023. **Verifica el porcentaje
  aplicable al contrato concreto**; es uno de los puntos de mayor litigiosidad.
- La reducción **solo** se aplica sobre rendimientos **declarados** (art. 23.2 in fine):
  no cabe en regularización de rentas no declaradas.
- Alquiler turístico con servicios propios de la hostelería → **actividad económica**,
  no capital inmobiliario.
- **Imputación de rentas inmobiliarias (art. 85)**: 2 % del valor catastral, o 1,1 % si
  el valor catastral fue revisado en el propio ejercicio o en los 10 anteriores.

## 5. Actividades económicas

**Regímenes**:
- Estimación directa normal: INCN > 600.000 €.
- Estimación directa simplificada: INCN ≤ 600.000 €. Gastos de difícil justificación
  5 %, máximo 2.000 €.
- Estimación objetiva (módulos): solo actividades de la Orden anual, con límites de
  ingresos (actividades / agrícolas), de compras y por facturación a empresarios
  sujeta a retención. Ver skill `autonomos-y-modulos`.

**Elemento clave — afectación (art. 29 LIRPF, art. 22 RIRPF)**:
- Vehículos de turismo: **afectación total o nada** salvo las excepciones tasadas
  (taxis, autoescuelas, agentes comerciales, transporte, vigilancia). No cabe
  afectación parcial. Esto vale para IRPF; en IVA sí hay presunción del 50 % (art. 95
  LIVA) — no confundas los dos regímenes.
- Inmuebles y elementos divisibles: sí cabe afectación parcial.
- Suministros de vivienda parcialmente afecta: 30 % sobre el % de superficie afecta.

**Reducción por inicio de actividad (art. 32.3)**: 20 % del rendimiento neto positivo
en el primer periodo con rendimiento positivo y el siguiente, con límite de base
de 100.000 €.

## 6. Ganancias y pérdidas patrimoniales

Fórmula: `Valor de transmisión − Valor de adquisición`.

- Valor de transmisión: importe real − gastos y tributos inherentes a cargo del
  transmitente.
- Valor de adquisición: importe real + inversiones y mejoras + gastos y tributos
  inherentes − amortizaciones (obligatoriamente las mínimas en inmuebles arrendados).
- **Coeficientes de abatimiento** (DT 9.ª): solo para elementos adquiridos antes del
  31-12-1994, sobre la parte generada hasta el 20-01-2006, con límite acumulado de
  400.000 € de valor de transmisión por contribuyente.

**Exenciones y diferimientos**:
- Reinversión en vivienda habitual (art. 38.1): 2 años antes o después.
- Mayores de 65 años: transmisión de vivienda habitual exenta (art. 33.4.b), o
  constitución de renta vitalicia hasta 240.000 € (art. 38.3).
- Dación en pago de la vivienda habitual (art. 33.4.d).

**Reglas de no cómputo de pérdidas (art. 33.5)**: transmisiones lucrativas inter vivos,
consumo, juego (salvo compensación con ganancias del juego), recompra de valores
homogéneos en **2 meses** (cotizados) o **1 año** (no cotizados), recompra del mismo
elemento en 1 año.

**Compensación (arts. 48-49)**:
- Base general: pérdidas patrimoniales sin transmisión ↔ ganancias del mismo tipo;
  saldo negativo compensa hasta el **25 %** del saldo positivo de rendimientos.
- Base del ahorro: rendimientos de capital mobiliario ↔ entre sí; ganancias/pérdidas
  ↔ entre sí; los saldos negativos se compensan entre bloques hasta el **25 %**.
- Saldos negativos no compensados: **4 años** siguientes.

## 7. Reducciones de la base y mínimos

- Aportaciones a sistemas de previsión social (art. 51-52): límite general **1.500 €**,
  ampliable hasta 8.500 € por contribuciones empresariales (y aportaciones del
  trabajador con los coeficientes de la DA 16.ª), 5.000 € en seguros colectivos de
  dependencia, 4.250 € adicionales para autónomos en planes de empleo simplificados.
  Límite porcentual: 30 % de la suma de rendimientos netos del trabajo y actividades.
- Pensiones compensatorias al cónyuge y anualidades por alimentos **por decisión
  judicial** (art. 55). Las anualidades a los hijos no reducen la base: aplican la
  regla especial del art. 64.
- Tributación conjunta: 3.400 € (biparental) / 2.150 € (monoparental).
- Mínimos personal y familiar: ver `config/parametros-fiscales.md`. Reglas: convivencia
  o dependencia económica, rentas del descendiente/ascendiente ≤ 8.000 €, y el
  descendiente no debe presentar declaración con rentas > 1.800 €.

## 8. Deducciones de la cuota

**Estatales**: inversión en empresas de nueva o reciente creación (art. 68.1, hasta
50 % sobre 100.000 € — verificar), actividades económicas (remisión a la LIS), donativos
(Ley 49/2002: 80 % sobre los primeros 250 € y 40 % del resto, 45 % con recurrencia),
rentas obtenidas en Ceuta y Melilla, patrimonio histórico, alquiler de vivienda habitual
(régimen transitorio para contratos anteriores a 2015), maternidad y familia numerosa /
personas con discapacidad a cargo (arts. 81 y 81 bis), obras de mejora de eficiencia
energética (DA 50.ª), adquisición de vehículos eléctricos (DA 58.ª) — **verifica la
vigencia y prórroga de las deducciones temporales cada ejercicio**.

**Deducción por inversión en vivienda habitual**: suprimida desde 2013, pero subsiste
el **régimen transitorio** (DT 18.ª) para adquisiciones anteriores al 01-01-2013 con
deducción practicada en 2012 o anteriores.

**Autonómicas**: consulta obligatoria de la normativa de la CCAA. Nunca las omitas en
una revisión: son la fuente más habitual de devoluciones perdidas.

## 9. Modelos y plazos

| Modelo | Objeto | Plazo |
|---|---|---|
| 100 | Declaración anual IRPF | Campaña de Renta (habitualmente abril–junio del año siguiente) |
| 102 | Segundo plazo (40 %) | Habitualmente 5 de noviembre |
| 130 | Pago fraccionado, estimación directa | 1–20 de abril, julio, octubre; 1–30 de enero |
| 131 | Pago fraccionado, módulos | Ídem |
| 140 | Deducción por maternidad, abono anticipado | Cualquier momento |
| 143 | Familia numerosa / discapacidad, abono anticipado | Cualquier momento |
| 145 | Comunicación de datos al pagador | Antes del primer pago |
| 149/151 | Régimen de impatriados (art. 93) | Alta: 6 meses desde el alta en SS |

## 10. Errores y rectificaciones

| Situación | Vía |
|---|---|
| Resultado a ingresar mayor / devolución menor de lo declarado | **Declaración complementaria** del ejercicio (recargo art. 27 LGT) |
| Resultado a ingresar menor / devolución mayor (error en perjuicio del contribuyente) | **Autoliquidación rectificativa** (art. 120.3 LGT). Desde el ejercicio 2023 el modelo 100 incorpora la casilla de rectificativa: úsala en lugar del escrito |
| Datos personales o de domicilio | Modificación censal / renta web |

Plazo: dentro de los **4 años** de prescripción.

## 11. Checklist de revisión de una declaración

- [ ] Datos fiscales AEAT descargados y contrastados con los aportados por el cliente
- [ ] Todos los pagadores incluidos; retenciones cuadran con certificados
- [ ] Situación familiar actualizada (nacimientos, defunciones, divorcios, discapacidad)
- [ ] Titularidad y % de propiedad de inmuebles verificados en el Catastro
- [ ] Inmuebles no arrendados → imputación de renta; verificado el % (1,1 vs 2)
- [ ] Alquileres: reducción del art. 23.2 con el porcentaje correcto y justificada
- [ ] Amortización de inmuebles arrendados calculada sobre construcción, no sobre suelo
- [ ] Transmisiones del ejercicio: valores, gastos, abatimiento, exenciones
- [ ] Saldos negativos de ejercicios anteriores pendientes de compensar aplicados
- [ ] Aportaciones a planes de pensiones dentro de límites; exceso trasladado
- [ ] Deducciones **autonómicas** revisadas una a una
- [ ] Comparativa individual vs. conjunta realizada
- [ ] Cuenta bancaria correcta y titularidad del declarante
- [ ] Si sale a devolver > importe habitual: revisar antes de presentar
