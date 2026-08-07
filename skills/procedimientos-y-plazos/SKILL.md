---
name: procedimientos-y-plazos
description: Actuaciones con Hacienda y cómputo de plazos: requerimientos, comprobaciones, inspección, procedimiento sancionador, recursos, aplazamientos, recargos, intereses y prescripción. Úsala cuando llegue una notificación de la AEAT o haya que calcular un plazo o un recargo.
---

# Procedimientos y plazos

## Lo primero, siempre: el plazo

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py plazo --notificacion DD/MM/AAAA --meses 1
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py plazo --notificacion DD/MM/AAAA --dias-habiles 10
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py voluntaria --notificacion DD/MM/AAAA
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py recargo --fin-plazo ... --presentacion ... --cuota ...
```

- Fecha de notificación = fecha de acceso, o el **día 11** desde la puesta a disposición
  si no se accedió (art. 43.2 Ley 39/2015).
- Meses: de fecha a fecha. Días: **hábiles** salvo que la norma diga «naturales».
- Pasa los festivos con `--festivos`: el script solo excluye sábados y domingos.

| Actuación | Plazo |
|---|---|
| Requerimiento de información | El del requerimiento (habitual: 10 días hábiles) |
| Alegaciones / audiencia | 10 o 15 días hábiles |
| Sancionador: alegaciones | 15 días hábiles |
| Reposición · reclamación económico-administrativa · alzada | **1 mes** cada una |
| Contencioso-administrativo | 2 meses |

**Ampliación de plazo** (art. 91 RGAT): automática por la mitad si se pide **antes** de
los 3 días previos al vencimiento. Úsala, es gratis.

## Identifica el procedimiento

| Procedimiento | Alcance | ¿Preclusivo? |
|---|---|---|
| Verificación de datos | Errores y discrepancias patentes | **No** |
| Comprobación limitada | Registros y facturas; **no** contabilidad mercantil | **Sí** |
| Inspección | General o parcial; sí accede a contabilidad | Sí |
| Sancionador | Separado; 6 meses para iniciarlo tras la liquidación | — |

Gestión: 6 meses, y el exceso **caduca** (art. 104.4). Inspección: 18 meses, y el exceso
no caduca pero deja de interrumpir la prescripción.

## Defensa en sancionador

Alega siempre que quepa: **falta de motivación de la culpabilidad** (las fórmulas
genéricas están sistemáticamente anuladas por el TS) e **interpretación razonable de la
norma** (art. 179.2.d LGT). Y calcula el coste de recurrir frente a las reducciones del
art. 188: 65 % actas con acuerdo, 30 % conformidad, 40 % pronto pago.

## Deudas inaplazables

**Retenciones (111, 115, 123, 216) y pagos fraccionados del IS (202)** (art. 65.2 LGT).
La solicitud se inadmite y la deuda entra en ejecutiva desde el día siguiente al
vencimiento. Es el error más caro y más frecuente.

## Cómo contestar

Verifica órgano, expediente y CSV → calcula el plazo → determina qué se pide exactamente
→ reúne la documentación → redacta con `generacion-de-entregables` → presenta y archiva
el justificante con CSV.

Detalle completo, recursos, suspensión, aplazamientos y prescripción en
`references/detalle.md`.
