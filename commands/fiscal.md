---
description: Índice del plugin — todo lo que puede hacer y cómo pedírselo
argument-hint: [tema, p. ej. iva, renta, cartera, requerimiento]
---

Índice de asesoría fiscal: **$ARGUMENTS**

Si hay argumento, di en dos líneas qué comando o skill cubre ese tema y **empieza a
trabajarlo**. Si no lo hay, muestra este índice tal cual, sin añadir preámbulo:

---

## Trabajo del día a día

| Comando | Para qué |
|---|---|
| `/cartera` | Qué está pendiente, qué vence, qué hay que revisar |
| `/cierre-trimestre` | Cierre trimestral completo de un cliente |
| `/cuadrar` | Cuadrar modelos entre sí y contra la contabilidad |
| `/calendario` | Obligaciones y plazos, generales o de un cliente |
| `/documentacion` | Convertir Excel, papel y PDF escaneado en datos utilizables |

## Por impuesto

| Comando | Para qué |
|---|---|
| `/iva` | Sujeción, localización, exenciones, deducibilidad, regímenes |
| `/irpf` | Rentas, reducciones, mínimos, deducciones autonómicas |
| `/sociedades` | Ajustes extracontables, base, tipos, deducciones |
| `/retenciones` | Quién retiene, a qué tipo, en qué modelo |
| `/autonomos` | Alta, gastos deducibles, módulos, autónomo vs. sociedad |
| `/informativas` | Umbrales, facturación, SII, VeriFactu |
| `/patrimonio` | Patrimonio, herencias, donaciones, transmisiones, no residentes |

## Modelos

`/modelo <número>` sirve para **cualquiera**: `/modelo 303`, `/modelo 200`, `/modelo 720`.

Hay conocimiento específico para 036, 037, 100, 111, 115, 123, 130, 131, 180, 190, 193,
200, 202, 210, 232, 303, 347, 349, 390, 714, 718, 720 y 721. El resto se resuelve con el
catálogo completo.

| Comando | Para qué |
|---|---|
| `/modelo <n>` | Preparar, revisar o generar cualquier modelo |
| `/campana-renta` | Declaración de IRPF completa |
| `/cierre-fiscal` | Cierre del ejercicio con los ajustes del Impuesto sobre Sociedades |
| `/intrastat` | Declaración Intrastat de un periodo |
| `/generar-fichero` | Fichero en diseño de registro, listo para importar en la sede |

## Hacienda y clientes

| Comando | Para qué |
|---|---|
| `/requerimiento` | Analizar una notificación y preparar la contestación |
| `/procedimientos` | Recursos, sanciones, aplazamientos, plazos, prescripción |
| `/consulta-fiscal` | Resolver una consulta con nota para el expediente |
| `/alta-cliente` | Onboarding con diagnóstico y calendario |
| `/despacho` | Encargo, apoderamientos, blanqueo, conservación |

## Mantenimiento

| Comando | Para qué |
|---|---|
| `/verificar-normativa` | Contrastar los parámetros con el BOE y la AEAT |
| `/verificar-diseno` | Contrastar un diseño de registro con su orden oficial |
| `/sage` | Migración desde ContaPlus, importación, qué no cubre Sage |
| `/privacidad` | Comprobar que no se filtran datos de clientes |

---

**No hace falta usar comandos.** Pregunta en lenguaje normal —«¿cómo vamos este
trimestre?», «me ha llegado un requerimiento del 303 de 2024», «¿este alquiler lleva
retención?»— y se cargará solo lo que haga falta.

Tres cosas que conviene saber:

- **Nada se presenta.** El plugin prepara y cuadra; presentar es un acto humano con
  certificado, desde Sage o desde la sede.
- **Las cifras no se dan de memoria.** Se consultan, y lo que no está verificado sale
  marcado como tal.
- **El control no se lee entero.** Las preguntas sobre la cartera se responden con
  consultas filtradas, no volcando el Excel.
