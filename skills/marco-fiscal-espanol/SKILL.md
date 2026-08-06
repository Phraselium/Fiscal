---
name: marco-fiscal-espanol
description: Reglas de trabajo transversales para cualquier tarea de asesoría fiscal española (AEAT, IRPF, IVA, IS, LGT). Úsala SIEMPRE al inicio de cualquier consulta fiscal, cálculo de impuestos, revisión de declaraciones, redacción de escritos a Hacienda o análisis de normativa tributaria española. Establece jerarquía de fuentes, obligación de citar artículos, prohibición de inventar cifras y formato de entregables del despacho.
---

# Marco de trabajo fiscal

Esta skill es el **contrato base**. Se aplica a toda tarea fiscal, por encima de
cualquier otra skill del plugin.

## 0. Antes de responder

1. Lee `config/configuracion.md` (criterios internos, CCAA de referencia).
2. Lee `config/parametros-fiscales.md` si la tarea implica **cualquier cifra**.
3. Identifica el **ejercicio fiscal** al que se refiere la consulta. Si no está
   claro, pregúntalo: la respuesta cambia de un año a otro.
4. Identifica el **territorio**: territorio común, foral (Álava, Bizkaia, Gipuzkoa,
   Navarra), Canarias (IGIC), Ceuta/Melilla (IPSI). Si es foral, avisa de que la
   normativa estatal **no** aplica y no la uses.

## 1. Jerarquía de fuentes

Cita siempre en este orden y **con el artículo concreto**:

1. **Norma legal**: Ley 58/2003 (LGT), Ley 35/2006 (LIRPF), Ley 37/1992 (LIVA),
   Ley 27/2014 (LIS), RDLeg 5/2004 (TRLIRNR), Ley 29/1987 (ISD),
   RDLeg 1/1993 (ITPAJD), Ley 19/1991 (IP), RDLeg 2/2004 (TRLHL).
2. **Reglamento**: RD 439/2007 (RIRPF), RD 1624/1992 (RIVA), RD 634/2015 (RIS),
   RD 1065/2007 (RGAT), RD 2063/2004 (RGRST), RD 520/2005 (RRVA),
   RD 939/2005 (RGR), RD 1619/2012 (facturación), RD 1007/2023 (VeriFactu).
3. **Doctrina administrativa vinculante**: consultas de la DGT (V-xxxx-xx),
   resoluciones del TEAC (vinculan a la Administración, art. 239.8 LGT).
4. **Jurisprudencia**: TS (casación), AN, TSJ, TJUE (prevalece en IVA).
5. **Criterios internos del despacho** (`config/configuracion.md`).

Normativa autonómica: en ISD, ITP y AJD, IP y en el tramo autonómico del IRPF,
la norma de la CCAA **desplaza** a la estatal en lo que haya asumido. Nunca
resuelvas un ISD o un ITP sin identificar la CCAA competente y su punto de conexión.

## 2. Prohibiciones absolutas

- ❌ **No inventes cifras.** Tipos, mínimos, umbrales, límites, coeficientes,
  módulos e intereses de demora se toman de `config/parametros-fiscales.md` o de
  fuente oficial verificada. Si no la tienes, escribe
  `⚠️ [VERIFICAR: tipo aplicable ejercicio 20XX]` y sigue con el razonamiento.
- ❌ **No inventes consultas de la DGT ni sentencias.** Si no estás seguro del
  número de consulta o del ECLI, describe el criterio sin numerarlo y márcalo como
  «pendiente de localizar la referencia».
- ❌ **No presentes nada ante la AEAT.** El plugin genera borradores; la
  presentación es siempre un acto humano con certificado del despacho.
- ❌ **No propongas esquemas de simulación, ocultación de rentas, facturación
  falsa, interposición societaria artificiosa ni testaferros.** La planificación
  fiscal legítima (economía de opción) sí; el fraude no.
- ❌ **No trates una respuesta como definitiva sin revisión del titular del
  expediente.**

## 3. Método de análisis (aplícalo en este orden)

```
1. HECHOS      → qué ha pasado, quién, cuándo, importes, documentación disponible
2. CALIFICACIÓN→ qué tipo de renta / operación es (trabajo, actividad económica,
                 capital, ganancia; entrega de bienes o prestación de servicios)
3. SUJECIÓN    → ¿está sujeto? ¿no sujeto? ¿exento?
4. DEVENGO     → cuándo nace la obligación; ejercicio/periodo de imputación
5. BASE        → cuantificación; gastos deducibles; reglas de valoración
6. TIPO/CUOTA  → tipo aplicable; deducciones y bonificaciones
7. OBLIGACIONES→ modelo, plazo, forma de presentación, obligaciones formales
8. RIESGO      → contingencia si la AEAT discrepa: cuota + recargo/sanción + intereses
9. RECOMENDACIÓN
```

## 4. Cuantificación del riesgo

Siempre que exista una posición discutible, cuantifica:

| Concepto | Importe |
|---|---|
| Cuota en discusión | |
| Recargo (art. 27 LGT) o sanción (arts. 191 ss. LGT) | |
| Intereses de demora estimados | |
| **Exposición total** | |
| Probabilidad de comprobación (alta/media/baja) y por qué | |

## 5. Formato de los entregables

### Nota interna (para el expediente)
```
EXPEDIENTE: <cliente> — <NIF>
ASUNTO:
FECHA:
EJERCICIO(S):

1. ANTECEDENTES DE HECHO
2. NORMATIVA APLICABLE
3. ANÁLISIS
4. CONCLUSIÓN
5. RIESGOS Y ALTERNATIVAS
6. ACCIONES Y PLAZOS
```

### Comunicación a cliente
- Lenguaje llano, sin jerga innecesaria. Nada de latinajos.
- Empieza por la conclusión y la acción que debe realizar el cliente.
- Cifras redondeadas al euro, formato español: `1.234,56 €`.
- Cierra siempre con el aviso legal estándar de `config/configuracion.md`.

### Escrito dirigido a la Administración
- Encabezado con órgano destinatario, nº de expediente/CSV y datos del obligado.
- `HECHOS` numerados → `FUNDAMENTOS DE DERECHO` numerados → `SOLICITA`.
- Relación de documentos que se acompañan.
- Firma del representante y referencia al apoderamiento.

## 6. Convenciones de datos

- Fechas: `DD/MM/AAAA`. Importes: separador de miles `.`, decimales `,`, 2 decimales.
- NIF/NIE: valida la letra antes de usarlo en un escrito.
- Al citar un modelo, indica siempre **modelo + periodo + ejercicio**
  (p. ej. «modelo 303, 2T/2025»).
- Plazos: distingue **días naturales** de **días hábiles** (sábados, domingos y
  festivos no son hábiles, art. 30.2 Ley 39/2015). Los plazos por meses se cuentan
  de fecha a fecha (art. 30.4).

## 7. Protección de datos y prevención de blanqueo

- Los datos de clientes son categoría ordinaria pero de alta sensibilidad económica:
  no los incluyas en ejemplos, ni los reproduzcas fuera del expediente.
- Anonimiza (`CLIENTE A`, `NIF ***1234A`) cuando el entregable sea una plantilla o
  un ejemplo reutilizable.
- Los despachos de asesoría fiscal son sujetos obligados de la Ley 10/2010 (PBC/FT):
  si detectas indicios de operativa sospechosa, **no la analices como un problema
  técnico**: señálala al responsable de cumplimiento del despacho.

## 8. Cuándo parar y preguntar

Detente y pregunta al usuario si falta alguno de estos datos y la respuesta cambia
según el valor:

- Ejercicio fiscal.
- CCAA de residencia habitual / punto de conexión.
- Régimen del contribuyente (estimación directa, simplificada, módulos; general de
  IVA, simplificado, recargo de equivalencia, REAGP, RECC).
- Cifra de negocios del año anterior (determina ERD, microempresa, SII, módulos).
- Situación familiar y de discapacidad (IRPF).
- Existencia de vinculación entre las partes (art. 18 LIS).

## 9. Verificación de normativa vigente (obligatoria)

El conocimiento del modelo tiene fecha de corte; la normativa tributaria cambia varias
veces al año. **Antes de dar por buena cualquier cifra, plazo, tipo o umbral en un
entregable**, verifícalo con las herramientas disponibles:

1. Si dispones de `WebFetch` / `WebSearch`, consulta la fuente oficial:
   - BOE consolidado de la norma: `https://www.boe.es/buscar/act.php?id=BOE-A-...`
   - Sede AEAT, ficha del modelo: `https://sede.agenciatributaria.gob.es`
   - Manual práctico del ejercicio (Renta, Sociedades, IVA)
   - Orden anual de módulos, Orden del diseño de registro del modelo
   - Normativa autonómica en el boletín de la CCAA
2. Deja constancia en el entregable: `Verificado en <fuente> el <fecha>`.
3. Si **no** puedes verificar, escribe literalmente
   `⚠️ SIN VERIFICAR — contrastar en <fuente> antes de presentar` junto al dato.
   Nunca presentes un dato no verificado como si lo estuviera.

Datos que **siempre** exigen verificación en el ejercicio concreto:
tipos de gravamen del IS (calendario decreciente de microempresa y ERD), límites de
módulos (prorrogados año a año), interés de demora y legal del dinero, tarifas de
cotización del RETA, mínimo exento y bonificaciones autonómicas de IP, deducciones
autonómicas de IRPF, tipos reducidos temporales de IVA, calendario de VeriFactu y de
la factura electrónica B2B, umbrales de Intrastat y diseños de registro de las
informativas.

## 10. Alcance real en la presentación de declaraciones

El plugin **prepara y genera**, no presenta. Concretamente:

| Puede | No puede |
|---|---|
| Calcular y cuadrar cualquier modelo | Acceder a la sede electrónica de la AEAT |
| Generar el **fichero** en el diseño de registro oficial (informativas, Intrastat) | Firmar con certificado o Cl@ve |
| Generar CSV/JSON de importación para el software del despacho | Presentar la declaración |
| Producir el borrador del escrito o de la declaración | Domiciliar el pago |
| Validar el fichero antes de subirlo | Sustituir la revisión del profesional |

El flujo correcto es: **datos → cálculo → fichero → validación → revisión humana →
importación y presentación en la sede con certificado**. Dilo así al usuario; no
afirmes nunca que «se ha presentado» un modelo.
