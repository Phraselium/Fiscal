---
name: autonomos-y-modulos
description: Fiscalidad del autónomo: alta en Hacienda y RETA, gastos deducibles (vehículo, suministros, dietas), estimación objetiva o módulos, recargo de equivalencia y comparativa autónomo vs. sociedad.
---

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

## Detalle

`references/detalle.md` — cotizacion por ingresos reales y tarifa plana, calculo completo
de modulos con indices y minoraciones, regimen simplificado de IVA, y el marco de decision
autonomo/sociedad desarrollado.
