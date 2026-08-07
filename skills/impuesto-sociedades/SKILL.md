---
name: impuesto-sociedades
description: Impuesto sobre Sociedades — ajustes extracontables del resultado contable a la base imponible, amortizaciones, deterioros, provisiones, gastos no deducibles, operaciones vinculadas, compensación de bases imponibles negativas, tipos de gravamen, deducciones y bonificaciones, reserva de capitalización y nivelación, regímenes especiales (ERD, microempresa, entidades sin fines lucrativos, consolidación fiscal), modelo 200, pagos fraccionados modelo 202 y cierre contable-fiscal. Úsala para cualquier consulta de tributación de sociedades o revisión del modelo 200.
---

# Impuesto sobre Sociedades — Ley 27/2014

## Esquema

```
Resultado contable ± ajustes = BI previa
 − reserva de capitalizacion − BIN ± reserva de nivelacion = BI
 × tipo = cuota integra − DDI − bonificaciones
 → contraste con tributacion minima (art. 30 bis)
 − deducciones por incentivos = cuota liquida
 − retenciones − pagos fraccionados = cuota diferencial
```

## Tipos: NO los uses de memoria

Las microempresas (INCN < 1 M€) y las ERD (INCN < 10 M€) estan en un **calendario
transitorio decreciente** (Ley 7/2024 y DT 44 LIS, con ajustes posteriores). El tipo
cambia cada ejercicio.

```bash
python3 scripts/parametros.py ver is.tipo.microempresa
```

Consulta el **manual practico de Sociedades del ejercicio concreto**. Un tipo equivocado
invalida toda la liquidacion.

## Ajustes que mas se olvidan

| Ajuste | Signo | Norma |
|---|---|---|
| Gasto por IS | + | 15.b |
| Multas, sanciones y **recargos** | + | 15.c |
| **Intereses de demora tributarios: SI son deducibles** | — | STS 8-2-2021, sujetos al art. 16 |
| Deterioros de inmovilizado, intangible y participaciones | + temporario | 13.2 |
| Fondo de comercio: 10 % contable vs. 5 % fiscal | + | 12.2 |
| Liberalidades por encima del 1 % del INCN | + | 15.e |
| Gastos financieros > 30 % del beneficio operativo | + | 16 |
| Retribucion de administradores sin cobertura estatutaria | + | 15.e |
| Exencion de dividendos y plusvalias (95 %) | − | 21 |

## Trampas de cierre

- **Reserva de capitalizacion**: si la reserva indisponible no esta **contabilizada** antes
  de presentar, la reduccion no procede.
- **Reserva de nivelacion**: es diferimiento, no ahorro. Revierte a los 5 anos.
- **BIN**: limite del 70 % / 1.000.000 €, y comprobables **10 anos** (art. 66 bis LGT).
- **Operaciones vinculadas**: si las hay, hay modelo **232** en noviembre. Se olvida
  sistematicamente porque va cuatro meses despues del 200.

## Modelos

`200` anual · `202` pago fraccionado · `220`/`222` consolidacion · `232` vinculadas ·
`231` country-by-country. Ver `modelo-200`, `modelo-202`, `modelo-232`.

## Detalle

`references/detalle.md` — amortizaciones, deterioros y provisiones articulo a articulo,
operaciones vinculadas y sus metodos, compensacion de BIN, reservas, tabla completa de
deducciones, y checklist de cierre fiscal.
