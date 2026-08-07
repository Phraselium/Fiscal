---
name: modelos-aeat
description: Modelos de la AEAT: qué modelo corresponde, casillas, plazos, errores frecuentes y cuadres. Cubre 036, 100, 111, 115, 123, 130, 180, 190, 193, 200, 202, 210, 232, 303, 347, 349, 390, 714, 720, 721 e Intrastat. Úsala para preparar, revisar o cuadrar cualquier declaración.
---

# Modelos de la AEAT

## ¿Qué modelo toca?

```
PERSONA FÍSICA  sin actividad → 100 (+714 si patrimonio)
                con actividad → 100 + 130/131 + 303/390 + 111/115 + 347/349
PERSONA JURÍDICA              → 200 + 202 + 303/390 + 111/115/123 + 347/349 + 232
NO RESIDENTE    sin EP → 210        con EP → 200 + 206
ENTIDAD EN ATRIBUCIÓN         → 184 + IVA y retenciones

Bienes a la UE      → 303 + 349 + Intrastat (si supera umbral)
Servicios a la UE   → 303 + 349, SIN Intrastat
Exportación         → 303 + DUA, sin 349 ni Intrastat
Herencia → 650   Donación → 651 + IRPF del donante   Compraventa → 600
```

> Intrastat cubre **bienes**; el 349 cubre bienes **y servicios**. No son equivalentes.

## Dónde está cada modelo

| Modelo | Fichero |
|---|---|
| Cualquier otro, y el catálogo completo | `references/catalogo.md` |
| 036 y 037 — censal | `references/036-037-censal.md` |
| 100 — Renta | `references/100-renta.md` |
| 111 y 190 — retenciones de trabajo y actividades | `references/111-190-retenciones-trabajo.md` |
| 115 y 180 — alquiler de local | `references/115-180-alquileres.md` |
| 123 y 193 — dividendos e intereses | `references/123-193-capital-mobiliario.md` |
| 130 y 131 — pagos fraccionados del IRPF | `references/130-131-pagos-fraccionados.md` |
| 200 y 202 — Impuesto sobre Sociedades | `references/200-202-sociedades.md` |
| 210 — no residentes | `references/210-no-residentes.md` |
| 232 — operaciones vinculadas | `references/232-vinculadas.md` |
| 303 y 390 — IVA | `references/303-390-iva.md` |
| 347 — operaciones con terceros | `references/347-terceros.md` |
| 349 — intracomunitarias | `references/349-intracomunitarias.md` |
| 714 y 718 — Patrimonio y Grandes Fortunas | `references/714-718-patrimonio.md` |
| 720 y 721 — bienes en el extranjero | `references/720-721-extranjero.md` |
| Intrastat | `references/intrastat.md` |

## Plazos de referencia

| Cuándo | Qué |
|---|---|
| 1-20 abril, julio, octubre; 1-30 enero | 111, 115, 123, 130/131, 303, 349 |
| 1-20 abril, octubre, diciembre | 202 |
| Enero | 190, 180, 193, 184; 390 hasta el 30 |
| Febrero | 347 |
| 1 enero – 31 marzo | 720, 721 |
| Abril–junio | Campaña de Renta (100, 714) |
| 1-25 julio | 200 |
| Noviembre | 232 |
| Días 1-12 de cada mes | Intrastat |

**La domiciliación cierra el día 15** (25 de enero en el 4T; 20 de julio en el 200). Es la
causa número uno de presentaciones fuera de plazo evitables.

## Antes de dar un modelo por bueno

Cuádralo. Es lo que evita la mayoría de los requerimientos:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py --plantilla > cuadre.json
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py --datos cuadre.json
```

Comprueba: 190 ↔ Σ111 · 180 ↔ Σ115 · 193 ↔ Σ123 · 390 ↔ Σ303 · casilla 59 del 303 ↔ 349
clave E · casillas 10-11 ↔ 36-37 (AIB devengado y deducible) · casilla 67 ↔ 72 del
periodo anterior.

Para producir el fichero, ver `generacion-de-entregables`.
