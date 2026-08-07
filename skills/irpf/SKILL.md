---
name: irpf
description: Impuesto sobre la Renta de las Personas Físicas — cálculo, revisión de borradores y declaraciones (modelo 100), calificación de rentas, rendimientos del trabajo, capital inmobiliario y mobiliario, actividades económicas, ganancias y pérdidas patrimoniales, reducciones, mínimos, deducciones estatales y autonómicas, tributación individual o conjunta, retenciones y pagos fraccionados (modelos 130/131), declaraciones complementarias y rectificativas. Úsala para cualquier consulta de renta de una persona física residente.
---

# IRPF — Ley 35/2006

## Determina primero (sin esto no hay respuesta correcta)

1. **Residencia** (art. 9): >183 dias, nucleo de intereses economicos, o presuncion
   familiar. Si no es residente -> **IRNR**, skill `modelo-210`.
2. **CCAA de residencia habitual** (art. 72): determina escala autonomica, minimos y
   **deducciones autonomicas**. Sin la CCAA no se puede calcular una Renta.
3. **Individual vs. conjunta**: calcula las dos y compara. Siempre.
4. **Regimen especial**: art. 93 (impatriados), atribucion de rentas, TFI.

## Que base

| Componente | Base |
|---|---|
| Trabajo, capital inmobiliario, actividades economicas, imputaciones | General |
| Capital mobiliario (arts. 25.1-3) y ganancias por **transmision** | Ahorro |
| Capital mobiliario del art. 25.4 y ganancias **sin transmision** | General |

## Los cuatro puntos que mas cuestan dinero al cliente

1. **Reduccion por arrendamiento de vivienda (art. 23.2)**: regimen reformado por la Ley
   12/2023 con porcentajes 50/60/70/90 % y transitoria para contratos anteriores al
   26-05-2023. Depende del **contrato concreto**. Y solo cabe sobre rendimientos
   *declarados*: nunca en una regularizacion.
2. **Deducciones autonomicas**: es donde mas devoluciones se pierden. Reviselas una a una.
3. **Saldos negativos** de los 4 ejercicios anteriores pendientes de compensar.
4. **Amortizacion de inmuebles arrendados** sobre construccion, nunca sobre suelo.

## Vehiculos y afectacion

IRPF: afectacion **total o nada** (art. 22 RIRPF), salvo taxis, autoescuelas, agentes
comerciales, transporte y vigilancia. **No lo confundas con el 50 % del IVA.**

## Cifras

`python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar irpf` — escalas, minimos y limites. Las marcadas
`sin_verificar` hay que contrastarlas en el manual de Renta del ejercicio antes de usarlas.

## Modelos

`100` anual · `102` segundo plazo · `130`/`131` pagos fraccionados · `145` comunicacion al
pagador · `140`/`143` abonos anticipados · `149`/`151` impatriados.

## Detalle

`references/detalle.md` — rendimientos del trabajo con sus exenciones del art. 7, capital
inmobiliario, actividades economicas, ganancias y perdidas con coeficientes de abatimiento
y reglas de no computo, integracion y compensacion, reducciones y minimos, deducciones
estatales, y checklist completo de revision de una declaracion.
