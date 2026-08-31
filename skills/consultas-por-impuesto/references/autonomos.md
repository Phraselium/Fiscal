# Autonomos y modulos

## Alta: orden correcto

```
1 AEAT 036/037  ANTES del inicio: epigrafe IAE, regimen IRPF, regimen IVA,
                obligaciones de retener, ROI si opera con la UE,
                casilla 504 si hay IVA soportado previo al inicio
2 TGSS  alta en RETA
3 Ayuntamiento, colegio profesional, RGPD, PRL
```

La **casilla 504** (deduccion de cuotas anteriores al inicio, art. 111 LIVA) se olvida
siempre en altas con inversion fuerte. Marcala.

## Gastos: los cuatro conflictivos

| Gasto | IRPF | IVA |
|---|---|---|
| **Vehiculo turismo** | Afectacion **total o nada** (art. 22 RIRPF), salvo taxi, autoescuela, agente comercial, transporte, vigilancia | Presuncion del **50 %** (art. 95.Tres) |
| **Suministros de la vivienda** | 30 % sobre el % de superficie afecta | En general **no** |
| Titularidad de la vivienda (IBI, comunidad, amortizacion) | Proporcion de superficie afecta, al 100 % de esa proporcion | — |
| **Manutencion del titular** | Limites de dietas, con **pago electronico** y factura | No, salvo prueba estricta |

Cuatro requisitos acumulativos para cualquier gasto: correlacion con los ingresos,
afectacion, **factura completa** (no ticket) y registro en los libros.

## Modulos

Los **limites de exclusion se prorrogan ano a ano**. No los des por sabidos:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py ver irpf.modulos.limites
```

Consulta la **Orden anual de modulos** del ejercicio (se publica en noviembre-diciembre).

- **Renuncia**: en diciembre por 036/037, o **tacita** presentando el 130 del 1T en plazo.
  Vincula 3 anos.
- Renunciar a modulos en IRPF arrastra la **exclusion del regimen simplificado de IVA**.
- Actividades del art. 95.6 RIRPF: retencion del **1 %** por el pagador empresario.

## Recargo de equivalencia

Comerciante minorista persona fisica o entidad en atribucion. El proveedor repercute IVA +
recargo; el minorista **no presenta 303** por esa actividad, pero **si presenta 309** por
AIB, importaciones e inversion del sujeto pasivo.

## Autonomo vs. sociedad

No hay cifra magica. Presenta siempre una **tabla numerica a tres escenarios de
beneficio**, comparando: marginal de IRPF vs. tipo del IS **mas** el coste de sacar el
dinero (dividendo o nomina), coste de estructura, y si el beneficio se reinvierte o se
consume. Y advierte del art. 18 LIS: la sociedad sin medios propios es el foco principal
de comprobacion.

---

# Autónomos y estimación objetiva

## 1. Alta de un autónomo — orden correcto

```
1. AEAT: modelo 036/037 → antes del inicio de la actividad
   · epígrafe(s) IAE  · régimen de IRPF  · régimen de IVA
   · obligaciones de retener (111/115)  · ROI si opera en la UE
2. TGSS: alta en RETA → hasta 60 días naturales antes, con efectos desde el día
   de inicio (hasta 3 altas y bajas al año con efecto desde el día concreto)
3. Ayuntamiento: licencia de apertura / declaración responsable si hay local
4. Seguridad Social: si contrata, inscripción de empresa y alta de trabajadores
5. Otros: colegio profesional, mutualidad alternativa, RGPD, PRL
```

**Tarifa plana**: cuota reducida los 12 primeros meses, prorrogable 12 más si el
rendimiento neto no supera el SMI anual. Requiere no haber estado de alta en los 2 años
anteriores (3 si ya se disfrutó). **Verifica el importe vigente**.

**Cotización por ingresos reales** (RD-ley 13/2022): el autónomo elige base dentro del
tramo correspondiente a su previsión de rendimiento neto; puede cambiarla 6 veces al año.
La TGSS regulariza al año siguiente cruzando con el rendimiento neto declarado en IRPF.
El rendimiento neto se calcula como rendimiento de la actividad + cuotas de RETA
deducidas − 7 % de deducción por gastos genéricos (3 % para autónomos societarios).

## 2. Gastos deducibles del autónomo — los conflictivos

| Gasto | Regla IRPF | Regla IVA |
|---|---|---|
| **Vehículo turismo** | Afectación **total o nada** (art. 22 RIRPF). Solo afecto si se usa exclusivamente en la actividad, salvo excepciones tasadas (taxi, autoescuela, agentes comerciales, transporte, vigilancia) | Presunción del **50 %** (art. 95.Tres LIVA), 100 % en los mismos supuestos tasados |
| **Suministros de la vivienda** (luz, agua, gas, internet) | 30 % sobre el porcentaje de superficie afecta declarado en el 036 (art. 30.2.5.ª b LIRPF) | En general **no deducible** por falta de afectación exclusiva |
| **Gastos de titularidad de la vivienda** (IBI, comunidad, seguro, amortización) | Deducibles en proporción a la superficie afecta (100 % de esa proporción, no el 30 %) | — |
| **Manutención del titular** | Deducible con límites de dietas: **26,67 €/día** en España y 48,08 € en el extranjero (el doble con pernocta), exigiendo pago **electrónico**, factura y realización en establecimiento de restauración en día laborable fuera del municipio | No deducible salvo prueba estricta |
| **Ropa** | Solo si es uniforme o ropa de protección con anagrama | Ídem |
| **Teléfono móvil** | Recomendable línea exclusiva; si es compartida, la AEAT rechaza la deducción total | 50 % discutible |
| **Cuota de autónomos (RETA)** | Deducible al 100 % | — |
| **Seguro de salud** | Deducible hasta **500 €** por el titular, cónyuge e hijos < 25 años que convivan (1.500 € con discapacidad) | — |
| **Formación y colegios profesionales** | Deducible si guarda correlación con los ingresos | Sí |

**Regla general**: correlación con los ingresos + afectación + justificación documental
(factura completa, no ticket) + registro contable en los libros. Los cuatro requisitos
son acumulativos.

## 3. Estimación objetiva (módulos) — IRPF

### Requisitos de permanencia
| Magnitud | Límite |
|---|---|
| Ingresos íntegros del conjunto de actividades (año anterior) | 250.000 € (verificar prórroga; límite ordinario de la Ley 150.000 €) |
| Ingresos por operaciones con obligación de expedir factura a empresarios | 125.000 € (ordinario 75.000 €) |
| Ingresos de actividades agrícolas, ganaderas y forestales | 250.000 € |
| Volumen de compras de bienes y servicios (sin inmovilizado) | 250.000 € |
| Actividad desarrollada fuera del ámbito de aplicación del IRPF | Exclusión |

> ⚠️ Los límites han sido objeto de **prórroga anual sucesiva** en las Leyes de
> Presupuestos y en reales decretos-leyes. **Verifica siempre el límite del ejercicio.**

### Renuncia y exclusión
- **Renuncia**: en diciembre del año anterior mediante 036/037, o de forma **tácita** al
  presentar el modelo 130 del 1T en plazo. Vincula **3 años**, prorrogables tácitamente.
- **Exclusión**: automática por superar límites; produce efectos el año siguiente.
- La renuncia a módulos en IRPF arrastra la **exclusión del régimen simplificado de IVA**
  (y viceversa): son regímenes vinculados.
- Actividades del art. 95.6 RIRPF sujetas a retención del **1 %** por el pagador
  empresario.

### Cálculo
```
Σ (unidades de módulo × rendimiento anual por unidad)
 − minoraciones por incentivos al empleo y a la inversión (amortizaciones)
 × índices correctores (población, temporada, empresas de pequeña dimensión, inicio…)
 = Rendimiento neto de módulos
 − reducción general del ejercicio (verificar en la Orden anual)
 − gastos extraordinarios por circunstancias excepcionales (comunicados a la AEAT)
 + otras percepciones empresariales (subvenciones)
 = Rendimiento neto reducido
```
La **Orden anual del Ministerio de Hacienda** (habitualmente publicada en noviembre-
diciembre) fija módulos, índices y reducciones. Búscala siempre para el ejercicio.

## 4. Régimen simplificado de IVA

- Aplicable solo si se aplica estimación objetiva en IRPF y la actividad está en la Orden.
- Cuota devengada por operaciones corrientes = Σ (módulos × cuota devengada anual por
  unidad) × índices.
- Menos IVA soportado en operaciones corrientes + 1 % de cuota devengada como difícil
  justificación, con el suelo de la **cuota mínima** de la actividad.
- Los tres primeros trimestres se ingresa un porcentaje a cuenta; el **4T** regulariza.
- Las adquisiciones intracomunitarias, importaciones, ISP y activos fijos se liquidan al
  margen del régimen.

## 5. Recargo de equivalencia

- Obligatorio para **comerciantes minoristas** personas físicas o entidades en atribución
  de rentas, cuando más del 80 % de sus ventas sean a consumidores finales y no
  transformen los productos.
- El proveedor repercute IVA + recargo (5,2 / 1,4 / 0,5 %). El minorista **no** repercute
  ni deduce, y **no presenta modelo 303** por su actividad.
- Sí debe presentar **modelo 309** por adquisiciones intracomunitarias, importaciones y
  supuestos de inversión del sujeto pasivo.
- No está obligado a llevar libros de IVA por esa actividad, pero sí a conservar facturas.

## 6. Autónomo vs. sociedad — marco de decisión

No hay una cifra mágica. Analiza en este orden:

1. **Tipo efectivo**: compara el marginal de IRPF del beneficio adicional con el 25 %
   (o el tipo de microempresa/ERD/nueva creación) **más** el coste de sacar el dinero
   (dividendo al 19-30 %, o nómina/factura del socio con su propio marginal).
2. **Vinculación (art. 18 LIS)**: el socio profesional debe facturar a valor de mercado.
   La «sociedad interpuesta» sin medios propios es el principal foco de comprobación.
3. **Coste de estructura**: contabilidad, depósito de cuentas, auditoría eventual,
   Impuesto de Sociedades, notaría, Registro Mercantil.
4. **Responsabilidad patrimonial** y percepción comercial.
5. **Necesidad de reinvertir** el beneficio: si el beneficio se reinvierte, la sociedad
   gana; si se consume íntegramente, la ventaja se reduce mucho.
6. **Cotización**: el administrador con control efectivo cotiza en RETA (autónomo
   societario, con base mínima superior).

Presenta siempre la comparativa como **tabla numérica a 3 escenarios de beneficio**, no
como afirmación genérica.
