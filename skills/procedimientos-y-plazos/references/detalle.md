# Procedimientos tributarios — LGT 58/2003

## Lo primero, siempre: el plazo

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py plazo --notificacion DD/MM/AAAA --meses 1
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py plazo --notificacion DD/MM/AAAA --dias-habiles 10
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py voluntaria --notificacion DD/MM/AAAA
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py recargo --fin-plazo ... --presentacion ... --cuota ...
```

- Fecha de notificacion = fecha de acceso, o **dia 11** desde la puesta a disposicion si no
  se accedio (art. 43.2 Ley 39/2015).
- Meses: de fecha a fecha. Dias: **habiles** salvo que diga «naturales».
- Pasa los festivos con `--festivos`: el script solo excluye sabados y domingos.

| Actuacion | Plazo |
|---|---|
| Requerimiento de informacion | El del requerimiento (habitual: 10 dias habiles) |
| Alegaciones / audiencia | 10 o 15 dias habiles |
| Sancionador: alegaciones | 15 dias habiles |
| Reposicion · REA · alzada TEAC | **1 mes** cada una |
| Contencioso-administrativo | 2 meses |

**Ampliacion de plazo** (art. 91 RGAT): automatica por la mitad del plazo si se pide
**antes** de los 3 dias previos al vencimiento. Uselo: es gratis.

## Identifica el procedimiento

| Procedimiento | Alcance | ¿Preclusivo? |
|---|---|---|
| Verificacion de datos (131-133) | Errores y discrepancias patentes | **No** |
| Comprobacion limitada (136-140) | Registros y facturas; **no** contabilidad mercantil | **Si** |
| Inspeccion (141-159) | General o parcial; si accede a contabilidad | Si |
| Sancionador (207-212) | Separado; 6 meses para iniciarlo desde la liquidacion | — |

Duracion maxima: 6 meses en gestion (el exceso **caduca**, art. 104.4), 18 meses en
inspeccion (el exceso no caduca pero deja de interrumpir la prescripcion).

## Defensa en sancionador

Dos argumentos que funcionan y hay que alegar siempre que quepan:
1. **Falta de motivacion de la culpabilidad**: las formulas genericas («al menos simple
   negligencia») estan sistematicamente anuladas por el TS.
2. **Interpretacion razonable de la norma** (art. 179.2.d LGT).

Calcula siempre el coste de recurrir frente a las reducciones del art. 188 (65 % acuerdo,
30 % conformidad, 40 % pronto pago).

## Deudas inaplazables (art. 65.2 LGT)

**Retenciones (111, 115, 123, 216) y pagos fraccionados del IS (202).** La solicitud se
inadmite y la deuda entra en ejecutiva desde el dia siguiente al vencimiento. Es el error
mas caro y mas frecuente.

## Detalle

`references/detalle.md` — metodo de contestacion a requerimientos, recursos y suspension,
recargos del art. 27 y 28, aplazamientos, devolucion de ingresos indebidos, prescripcion y
plantilla completa de escrito.




---

# Procedimientos tributarios — LGT 58/2003

## 1. Lo primero, siempre: calcular el plazo

1. **Fecha de notificación** = fecha de acceso a la notificación electrónica, o el
   **día 11** desde su puesta a disposición si no se accedió (rechazo tácito,
   art. 43.2 Ley 39/2015).
2. Los plazos por **meses** se cuentan de fecha a fecha desde el **día siguiente** a la
   notificación y vencen el día equivalente del mes correspondiente; si no existe día
   equivalente, el último del mes (art. 30.4 Ley 39/2015).
3. Los plazos por **días** son **hábiles** salvo que la norma diga «naturales». Sábados,
   domingos y festivos no son hábiles.
4. Si el vencimiento cae en inhábil, se traslada al siguiente hábil.
5. Anota el plazo **interno** del despacho: vencimiento oficial − 5 días hábiles.

| Actuación | Plazo |
|---|---|
| Contestación a requerimiento de información | El del requerimiento (normalmente 10 días hábiles) |
| Alegaciones a propuesta de liquidación / trámite de audiencia | 10 o 15 días hábiles |
| Alegaciones en procedimiento sancionador | 15 días hábiles |
| Recurso de reposición | **1 mes** |
| Reclamación económico-administrativa | **1 mes** |
| Alzada ante el TEAC | **1 mes** |
| Recurso contencioso-administrativo | **2 meses** |
| Pago en voluntaria, notificado del 1 al 15 | Hasta el **20 del mes siguiente** |
| Pago en voluntaria, notificado del 16 al fin de mes | Hasta el **5 del segundo mes siguiente** |

## 2. Identificar el procedimiento

| Procedimiento | Órgano | Alcance | Efecto preclusivo |
|---|---|---|---|
| **Verificación de datos** (arts. 131-133) | Gestión | Errores aritméticos, discrepancias con los datos declarados, aplicación indebida patente de la norma | **No** impide una comprobación posterior |
| **Comprobación limitada** (arts. 136-140) | Gestión | Examen de datos, registros y facturas. **No** puede examinar la contabilidad mercantil (salvo aportación voluntaria) ni requerir a terceros movimientos financieros | **Sí** preclusivo sobre el objeto comprobado |
| **Comprobación de valores** (arts. 134-135) | Gestión | Valoración de bienes | Tasación pericial contradictoria |
| **Inspección** (arts. 141-159) | Inspección | General o parcial; sí accede a contabilidad | Sí |
| **Sancionador** (arts. 207-212) | Separado | Debe iniciarse en **6 meses** desde la notificación de la liquidación |  |
| **Recaudación** (arts. 160-177) | Recaudación | Apremio, embargo, derivación de responsabilidad |  |

**Duración máxima**: 6 meses los de gestión (art. 104), 18 meses la inspección
(27 en los supuestos del art. 150.1). El **exceso** no produce caducidad en inspección,
pero **sí** deja de interrumpir la prescripción y elimina los intereses del exceso.
En gestión, el exceso produce **caducidad** (art. 104.4).

## 3. Contestación a un requerimiento — método

```
1. Verifica identidad del órgano, nº de expediente, CSV, y quién es el obligado.
2. Comprueba el plazo real y anótalo.
3. Determina QUÉ pide exactamente. No aportes más de lo pedido.
4. Reúne la documentación; si falta, valora solicitar AMPLIACIÓN DE PLAZO
   (art. 91 RGAT: se concede automáticamente por la mitad del plazo inicial si se
   solicita ANTES de los 3 días previos al fin del plazo y no se ha concedido antes).
5. Redacta: HECHOS → FUNDAMENTOS → SOLICITA → DOCUMENTOS QUE SE ACOMPAÑAN.
6. Presenta por la sede (trámite de aportación de documentación complementaria o
   contestación al requerimiento) y guarda el justificante con CSV en el expediente.
```

Reglas del despacho al contestar:
- Nunca reconozcas hechos que no consten acreditados.
- Nunca aportes documentación de terceros no requerida.
- Si la posición es discutible, contesta con los hechos y reserva la argumentación
  jurídica completa para las alegaciones o el recurso.
- Cita la doctrina que te favorece (DGT/TEAC vincula a la Administración: art. 239.8 y
  art. 89 LGT).

## 4. Recursos

**Recurso de reposición (arts. 222-225)**: potestativo, previo a la vía
económico-administrativa, ante el **mismo órgano** que dictó el acto. 1 mes. Resolución
en 1 mes; el silencio es **desestimatorio** y abre el plazo de la reclamación.

**Reclamación económico-administrativa (arts. 226-249)**:
- TEAR/TEAL en primera instancia; TEAC en alzada o en única instancia si la cuantía
  supera los umbrales reglamentarios.
- **Procedimiento abreviado** para cuantías inferiores al umbral del art. 245 RRVA:
  alegaciones necesariamente **con** el escrito de interposición.
- Silencio: desestimatorio a **1 año** desde la interposición.
- Es **gratuita** y no requiere abogado ni procurador.

**Suspensión de la ejecución (art. 233)**:
- **Automática** con garantía de depósito, aval solidario de entidad de crédito o fianza
  personal y solidaria de dos contribuyentes.
- **Discrecional** con otras garantías, o **sin garantía** si se acredita perjuicio de
  difícil o imposible reparación, o si el acto incurre en **error aritmético, material o
  de hecho** (art. 233.4).
- Las **sanciones** quedan automáticamente suspendidas sin garantía por el mero hecho de
  recurrirlas en vía administrativa (art. 212.3), hasta que sean firmes en vía
  administrativa. Ojo: la suspensión decae al agotar la vía administrativa.

## 5. Sancionador

- **Principio de culpabilidad** (art. 179): no hay sanción si se actuó con la diligencia
  necesaria, hubo interpretación razonable de la norma, o se siguió el criterio de la
  Administración. Es la línea de defensa principal.
- La motivación de la culpabilidad debe ser **específica**: las fórmulas genéricas
  («se aprecia al menos simple negligencia») están sistemáticamente anuladas por el TS.
  Alega siempre falta de motivación si el acuerdo es estereotipado.
- Reducciones (art. 188): **65 %** actas con acuerdo, **30 %** conformidad, y **40 %**
  adicional por pronto pago sin recurrir. Calcula siempre el coste de recurrir frente a
  la reducción que se pierde.
- Plazo para iniciar: 6 meses desde la notificación de la liquidación. Duración máxima
  del expediente sancionador: 6 meses.

## 6. Regularización voluntaria y recargos (art. 27)

| Retraso desde el fin del plazo voluntario | Recargo |
|---|---|
| Mes 1 | 1 % |
| Meses 2 a 12 | 1 % + 1 % por cada mes completo adicional |
| > 12 meses | 15 % + intereses de demora desde el día siguiente a los 12 meses |

- Reducción del **25 %** del recargo si se ingresa en el plazo del art. 62.2 abierto con
  la notificación del recargo y no se recurre la liquidación ni el recargo.
- **No** procede recargo (art. 27.2, párrafo añadido por la Ley 11/2021) si el obligado
  regulariza otros periodos del mismo concepto en los 6 meses siguientes a la
  notificación de una liquidación previa por hechos idénticos, sin sanción ni recurso.
- Presentar fuera de plazo **antes** de un requerimiento evita la sanción del art. 191 y
  deja solo el recargo: es casi siempre la mejor opción.

## 7. Aplazamientos y fraccionamientos (arts. 65 LGT y 44 ss. RGR)

- **Deudas inaplazables**: retenciones e ingresos a cuenta (art. 65.2.b) salvo los
  supuestos excepcionales, pagos fraccionados del IS, deudas del concursado posteriores
  al concurso, y las derivadas de resoluciones firmes suspendidas.
  ⚠️ Es un error frecuente solicitar aplazamiento del **111**: se inadmite y la deuda
  entra en ejecutiva desde el día siguiente al fin del plazo voluntario.
- **Exención de garantías** hasta el umbral vigente (actualmente 50.000 € —
  **verificar** la orden en vigor), con solicitud en sede y plan de pagos automático.
- Solicitar **en periodo voluntario** impide el inicio del periodo ejecutivo; solicitarlo
  en ejecutiva no evita el recargo ya devengado.
- Intereses de demora durante el aplazamiento; interés legal si hay aval.

## 8. Devolución de ingresos indebidos y rectificación

- **Rectificación de autoliquidación** (art. 120.3 LGT, arts. 126-129 RGAT): cuando el
  error perjudica al contribuyente. En IRPF e IS existe ya la **autoliquidación
  rectificativa** integrada en el propio modelo: úsala con preferencia al escrito.
- **Devolución de ingresos indebidos** (art. 221): duplicidad, exceso sobre lo liquidado,
  ingreso de deudas prescritas, o cuando lo establezca la norma. Plazo: 4 años.
- Intereses de demora a favor del contribuyente desde la fecha del ingreso indebido
  (art. 32.2).

## 9. Prescripción (arts. 66-70)

- **4 años** para: liquidar, exigir el pago, solicitar devoluciones y obtenerlas.
- Se interrumpe por cualquier acción administrativa con conocimiento formal del obligado,
  por la interposición de reclamaciones y por cualquier actuación fehaciente del obligado
  conducente a la liquidación o pago.
- **BIN, deducciones y créditos fiscales**: derecho de comprobación durante **10 años**
  (art. 66 bis); después basta con exhibir la liquidación y el depósito de cuentas.
- Sanciones: 4 años desde la comisión de la infracción.
- Conserva la documentación al menos **6 años** por el Código de Comercio y hasta
  **10-15 años** cuando haya BIN o deducciones pendientes.

## 10. Plantilla de escrito

```
AL <ÓRGANO> — <DELEGACIÓN / ADMINISTRACIÓN>
Expediente / Referencia: <...>          CSV: <...>

D./D.ª <representante>, con NIF <...>, en nombre y representación de
<obligado tributario>, con NIF <...> y domicilio a efectos de notificaciones en
<...>, según acredita el apoderamiento que consta en el Registro de Apoderamientos
de la AEAT, ante ese órgano comparece y, como mejor proceda, DICE:

HECHOS
PRIMERO.- ...
SEGUNDO.- ...

FUNDAMENTOS DE DERECHO
PRIMERO.- Competencia y plazo. ...
SEGUNDO.- <fondo>. Artículo <...> de la Ley <...>. Doctrina: consulta DGT <...>;
resolución TEAC de <fecha>; STS de <fecha> (rec. <...>).

Por lo expuesto,
SOLICITA que, teniendo por presentado este escrito, se sirva admitirlo y, en su
virtud, <pretensión concreta>.

DOCUMENTOS QUE SE ACOMPAÑAN
1. ...

En <lugar>, a <fecha>.
```
