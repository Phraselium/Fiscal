---
name: catalogo-modelos-aeat
description: Qué modelo hay que presentar. Catálogo de todos los modelos de la AEAT, autonómicos y locales, con quién los presenta y en qué plazo. Úsala para «¿qué modelo me toca?» o para listar las obligaciones de un cliente.
---

# Catalogo de modelos

Mapa para identificar **que modelo corresponde**. Los plazos son los ordinarios; verifica
el calendario del contribuyente del ejercicio, que tiene adaptaciones anuales.

## Arbol de decision

```
PERSONA FISICA residente
  sin actividad        → 100  (+714 si patrimonio)
  con actividad        → 100 + 130/131 + 303/390 + 111/115 + 347/349
PERSONA JURIDICA       → 200 + 202 + 303/390 + 111/115/123 + 347/349 + 232
NO RESIDENTE  sin EP   → 210   |  con EP → 200 + 206
ENTIDAD EN ATRIBUCION  → 184 + IVA y retenciones

OPERACION
  compra inmueble a particular → 600 (TPO)
  compra a promotor            → IVA + 600 (AJD)
  herencia                     → 650 + plusvalia municipal
  donacion                     → 651 + IRPF DEL DONANTE
  bienes a la UE               → 303 + 349 + Intrastat (si umbral)
  servicios a empresa UE       → 303 + 349, SIN Intrastat
  exportacion fuera UE         → 303 + DUA, sin 349 ni Intrastat
```

> **Intrastat cubre bienes; el 349 cubre bienes y servicios.** No son equivalentes.

## Los que se usan a diario

| Grupo | Modelos |
|---|---|
| Censales | 036, 037, 030, 034, 840, 848 |
| IRPF | 100, 102, 130, 131, 145, 149/151 |
| Retenciones | 111, 115, 123, 216 → resumenes 190, 180, 193, 296 |
| IVA | 303, 309, 322/353, 349, 369, 380, 390 |
| Sociedades | 200, 202, 220/222, 231, 232 |
| No residentes | 210, 211, 213, 216/296 |
| Informativas | 347, 720, 721, 184, 182, 233, 238, 289 |
| Patrimonio | 714, 718 |
| Aduanas | Intrastat, DUA |
| Autonomicos / locales | 600, 620, 650, 651, 655, IIVTNU, IBI, IVTM |

## Plazos de referencia

| Cuando | Que |
|---|---|
| 1-20 abril, julio, octubre; 1-30 enero | 111, 115, 123, 130/131, 303, 349 |
| 1-20 abril, octubre, diciembre | 202 |
| Enero | 190, 180, 193, 184 y demas resumenes; 390 hasta el 30 |
| Febrero | 347; 848 hasta el 14 |
| 1 enero - 31 marzo | 720, 721 |
| Abril-junio | Campana de Renta (100, 714) |
| 1-25 julio | 200 |
| Julio | 718 |
| Noviembre | 232; 102 el dia 5 |
| Dias 1-12 de cada mes | Intrastat |

**Domiciliacion**: cierra el dia 15 (25 de enero para el 4T; 20 de julio para el 200). Es
la causa numero uno de presentaciones fuera de plazo evitables.

## Detalle

`references/detalle.md` — catalogo completo con todos los modelos estatales, autonomicos,
locales, de impuestos especiales y medioambientales, mas las obligaciones mercantiles y
registrales con sus plazos.
