---
name: sage-despachos
description: Trabajo con Sage Despachos Connected como software del despacho — migración desde ContaPlus, contabilidad y enlace fiscal, generación y presentación telemática de modelos desde Sage, importación de asientos y facturas, plan de cuentas, y qué hacer cuando Sage no cubre un caso. Úsala para cualquier tarea que implique el software del despacho, importar datos o presentar desde Sage.
---

# Sage Despachos

El despacho migra de **ContaPlus** a **Sage Despachos Connected**. La consecuencia
operativa más importante para este plugin:

> **Los modelos se generan y se presentan desde Sage, no a mano.** El enlace fiscal de
> Sage produce el 303, 111, 115, 123, 130, 202, 347, 349, 190, 180, 193, 390 y 200 a
> partir de la contabilidad, y los presenta telemáticamente con el certificado del
> despacho.

Por eso el papel del asistente **no** es fabricar ficheros que Sage ya genera, sino:

1. Preparar los datos de entrada para que Sage los digiera (el trabajo real).
2. **Cuadrar** lo que Sage saca antes de presentarlo.
3. Resolver los casos que Sage no cubre o que salen mal.
4. Mantener el control de cartera actualizado.

## Reparto de responsabilidades

| Tarea | Quién |
|---|---|
| Contabilizar | Sage (con los datos que le preparemos) |
| Calcular el modelo a partir de la contabilidad | Sage, enlace fiscal |
| Presentar telemáticamente | Sage, con certificado |
| Decidir **si** un cliente debe presentar un modelo | El asesor, mirando el 036 |
| Calificar una operación (sujeción, exención, tipo, ISP) | El asesor |
| **Cuadrar** modelo ↔ contabilidad ↔ resúmenes anuales | `scripts/cuadrar.py` y el asesor |
| Casos fuera del enlace: Intrastat, 720, 232, 210 | Fuera de Sage, ver skills propias |

## Migración desde ContaPlus

Puntos que hay que verificar cliente a cliente al migrar; son los que rompen:

- [ ] **Plan de cuentas**: ContaPlus admite longitudes de cuenta distintas. Comprobar que
      el nivel de desglose se mantiene y que las cuentas de IVA soportado/repercutido
      quedan bien mapeadas por tipo (21/10/4) y por naturaleza (interior, AIB, ISP,
      importación). Si esto se mezcla, el 303 sale mal y no se nota hasta el 390.
- [ ] **Saldos de apertura** del ejercicio y saldos pendientes de clientes y proveedores.
- [ ] **Bienes de inversión** y su cuadro de amortización, incluida la fecha de inicio del
      periodo de regularización de IVA (4 años, 9 en inmuebles).
- [ ] **BIN y deducciones pendientes** por ejercicio de origen: es lo que la AEAT puede
      comprobar 10 años (art. 66 bis LGT). Si se pierde en la migración, se pierde el
      crédito fiscal.
- [ ] **Compensaciones de IVA** arrastradas (casilla 72 del último 303).
- [ ] **Datos censales** de cada cliente: régimen de IVA, periodicidad, obligaciones de
      retener, alta en ROI, SII. Sage los usa para decidir qué modelos ofrece.
- [ ] **Retenciones acumuladas del ejercicio** si la migración es a mitad de año: sin
      ellas el 190 de enero no cuadra.
- [ ] **Series de facturación** y su correlatividad.

Migra y **cuadra un trimestre ya presentado** antes de dar por buena la migración: si
Sage reproduce el 303 y el 111 de un trimestre cerrado, la conversión es correcta.

## Preparar datos para Sage

Sage importa asientos y facturas por fichero. El trabajo del asistente es convertir lo
que llega del cliente a un formato importable y **coherente**:

- Un asiento por documento, con fecha de **devengo**, no de pago ni de recepción.
- Cuenta de IVA correcta por tipo y naturaleza: mezclar IVA interior con AIB o con ISP es
  el error que más descuadres provoca.
- NIF validado (`scripts/lib/validaciones.py`) antes de dar de alta un tercero: un NIF mal
  dado de alta contamina el 347 y el 190 de todo el ejercicio.
- Marcar las operaciones que van a informativas: intracomunitarias (349), con retención
  (190/180/193), y las que superan el umbral del 347.

Antes de importar nada, enseña al usuario un extracto de lo que vas a cargar y el total,
para que lo valide. Nunca importes a ciegas.

## Cuando Sage saca el modelo

**No lo presentes porque Sage lo haya calculado.** El enlace fiscal es tan bueno como la
contabilidad. Cuadra siempre:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py --help
```

Y revisa a ojo, como mínimo: casillas 10-11 y 36-37 del 303 (AIB en devengado y
deducible), casilla 59 contra el 349, casilla 67 contra la 72 del periodo anterior, y
las claves del 111 contra las del 190.

## Lo que Sage no cubre

| Obligación | Dónde se hace |
|---|---|
| **Intrastat** | Portal de Aduanas. Ver skill `intrastat` y `scripts/generar_intrastat.py` |
| **Modelo 720 / 721** | Formulario de la sede; datos que no están en la contabilidad |
| **Modelo 232** | Requiere identificar vinculadas y valorar a mercado |
| **Modelo 210** | Clientes no residentes, fuera de la contabilidad del despacho |
| **ITP/AJD, ISD** | Administración autonómica |
| **Plusvalía municipal** | Ayuntamiento |
| Escritos, recursos, requerimientos | Fuera de cualquier software: ver `procedimientos-tributarios` |

## VeriFactu y facturación de los clientes

La obligación de VeriFactu recae en **el cliente que emite facturas**, no en el despacho.
Fechas vigentes tras el segundo aplazamiento:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py ver verifactu.fecha_obligatoriedad
```

Verifica la fecha antes de asesorar: se ha aplazado dos veces y cualquier documentación
que diga 2025 o 2026 está desactualizada. Lo que sí conviene hacer ya con los 85 clientes
es inventariar qué software de facturación usa cada uno y pedir al proveedor la
declaración responsable de cumplimiento del RD 1007/2023.
