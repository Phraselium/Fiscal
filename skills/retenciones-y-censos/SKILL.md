---
name: retenciones-y-censos
description: Retenciones e ingresos a cuenta y obligaciones censales: quién retiene, a qué tipo, y altas, modificaciones y bajas en Hacienda.
---

# Retenciones y censos

## Quien retiene

Personas juridicas, y personas fisicas **en el ejercicio de su actividad economica**. Un
particular que no ejerce actividad no retiene — salvo que sea arrendatario empresario de
un local, donde retiene el, no el arrendador.

## Tipos

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar retenciones
```

Los mas usados: profesionales **15 %** (7 % en el ano de inicio y los 2 siguientes, previa
comunicacion escrita), administradores **35 %** (19 % si el INCN de la entidad < 100.000 €),
alquiler de local **19 %**, capital mobiliario **19 %**, modulos del art. 95.6 RIRPF **1 %**.
El trabajo por cuenta ajena no tiene tipo fijo: procedimiento del art. 80 ss. RIRPF.

## Las tres trampas

1. **El 111 es inaplazable** (art. 65.2.b LGT). Solicitarlo lo inadmite y la deuda entra en
   ejecutiva con recargo del 5-20 %.
2. **No retener el alquiler de local** es la regularizacion mas comun: la AEAT cruza el
   gasto contabilizado con la ausencia de 115. Las excepciones del art. 75.3.g exigen
   prueba — el certificado del grupo 861 caduca al ano.
3. **Dietas y rentas exentas** no llevan retencion pero **si van al 190 con clave L**.
   Omitirlas genera propuestas de liquidacion a los trabajadores.

## Censos: lo que provoca requerimientos

| Error | Consecuencia |
|---|---|
| Alta en la obligacion del 111 y no presentar | Requerimiento cada trimestre. Presenta negativa **o** da de baja la obligacion |
| Cese sin baja censal | Se siguen exigiendo 303, 111 y 130 indefinidamente |
| Facturar sin IVA a la UE sin ROI | La operacion no esta exenta: 21 % + sancion |
| No comunicar el cambio de domicilio fiscal | Notificaciones validas en el antiguo; se pierden plazos |
| No renunciar a modulos en diciembre | Se tributa en un regimen que no corresponde |

**Regla practica**: antes de cada trimestre, contrasta la matriz del control con el 036 de
cada cliente. Las celdas «No aplica» que deberian estar en flujo (y al reves) salen con
`python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py huecos`.

## Modelos

`111`/`190` · `115`/`180` · `123`/`193` · `216`/`296` · `036`/`037` · `840`/`848`.
Cada uno tiene su skill.

## Detalle

`references/detalle.md` — tabla completa de tipos, calculo de la retencion del trabajo,
excepciones del 115, cuadre de resumenes anuales, contenido del 036 pagina a pagina, IAE,
apoderamientos y notificaciones.
