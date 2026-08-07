---
name: iva
description: Impuesto sobre el Valor Añadido — sujeción, exenciones, localización del hecho imponible, devengo, base imponible, tipos, deducibilidad y prorrata, regímenes especiales (simplificado, recargo de equivalencia, REBU, RECC, agencias de viajes, REAGP, OSS/IOSS), inversión del sujeto pasivo, operaciones intracomunitarias y exportaciones, modelos 303, 390, 349, 309, 368, SII, rectificación de facturas y recuperación de IVA de impagados. Úsala para cualquier consulta de IVA o revisión de autoliquidaciones.
---

# IVA — Ley 37/1992

## Secuencia obligatoria (no la saltes)

```
1 SUJECION      arts. 4, 5, 7      5 BASE          arts. 78-81
2 CALIFICACION  arts. 8, 11, 13    6 TIPO          arts. 90-91
3 LOCALIZACION  arts. 68-70  <-- donde mas se falla
4 EXENCION      arts. 20-25        7 SUJETO PASIVO art. 84 (¿ISP?)
                                   8 DEDUCCION     arts. 92-114
```

## Los tres errores que generan el 80 % de las regularizaciones

1. **Localizacion de servicios**: regla general B2B = sede del *destinatario*; B2C = sede
   del *prestador*. Pero las reglas especiales del art. 70.Uno (inmuebles, transporte,
   restauracion, acceso a eventos, arrendamiento de medios de transporte) **desplazan** a
   la general. Comprueba siempre si aplica una especial antes de usar la general.
2. **Inversion del sujeto pasivo** (art. 84.Uno.2.º): no establecidos, ejecuciones de obra
   de construccion o rehabilitacion, inmuebles con renuncia a la exencion, oro, chatarra,
   moviles y portatiles a revendedores. Factura sin IVA con la mencion expresa, y el
   destinatario autorrepercute **y** deduce en la misma autoliquidacion.
3. **Deducibilidad**: exclusiones del art. 96 (atenciones, espectaculos, joyas, alimentos);
   vehiculos con presuncion del **50 %** en IVA — que no es la regla de todo o nada del
   IRPF; y plazo de 4 anos del art. 99.

## Cifras

No las memorices. `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar iva`

Los **tipos reducidos temporales** de alimentacion y energia han cambiado varias veces:
verifica el tipo vigente **a la fecha de devengo** de cada operacion, no el de hoy.

## Modelos

`303` autoliquidacion · `390` resumen anual · `349` intracomunitarias · `309` no periodica ·
`369` OSS/IOSS · `380` asimiladas a la importacion · `322`/`353` grupo de entidades.
Cada uno tiene su skill (`modelo-303`, `modelo-390`, `modelo-349`).

## Detalle

`references/detalle.md` — localizacion campo a campo, exenciones del art. 20 con su
casuistica, prorrata general y especial, bienes de inversion, modificacion de la base
imponible del art. 80, regimenes especiales (simplificado, recargo de equivalencia, REBU,
RECC, agencias de viaje, REAGP) y checklist de revision del 303.
