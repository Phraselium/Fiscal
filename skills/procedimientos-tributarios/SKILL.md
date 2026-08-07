---
name: procedimientos-tributarios
description: Procedimientos frente a la AEAT — contestación a requerimientos, propuestas de liquidación, verificación de datos, comprobación limitada, inspección, procedimiento sancionador, recurso de reposición, reclamación económico-administrativa (TEAR/TEAC), suspensión de la ejecución, aplazamientos y fraccionamientos (modelo de solicitud), devolución de ingresos indebidos, rectificación de autoliquidaciones, prescripción, recargos e intereses. Úsala cuando llegue una notificación de Hacienda, haya que recurrir un acto tributario o calcular plazos y recargos.
---

# Procedimientos tributarios — LGT 58/2003

## Lo primero, siempre: el plazo

```bash
python3 scripts/calcular_plazos.py plazo --notificacion DD/MM/AAAA --meses 1
python3 scripts/calcular_plazos.py plazo --notificacion DD/MM/AAAA --dias-habiles 10
python3 scripts/calcular_plazos.py voluntaria --notificacion DD/MM/AAAA
python3 scripts/calcular_plazos.py recargo --fin-plazo ... --presentacion ... --cuota ...
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
