---
name: modelo-349
description: Modelo 349, operaciones intracomunitarias: claves de operación, periodicidad, alta en el ROI, comprobación del NIF-IVA en VIES y requisitos de la exención del artículo 25 LIVA.
---

# Modelo 349 — Operaciones intracomunitarias

## 1. Quién y cuándo

- Obligados: empresarios y profesionales que realicen entregas o adquisiciones
  intracomunitarias de **bienes o servicios**, cualquiera que sea su importe.
- Requisito previo: estar inscrito en el **ROI** (Registro de Operadores
  Intracomunitarios) mediante el modelo 036, casillas 582/584. La AEAT dispone de
  **3 meses** para resolver; hasta entonces no se puede facturar sin IVA.
- **Periodicidad**:

| Situación | Periodicidad |
|---|---|
| Regla general | **Mensual**, 1–20 del mes siguiente |
| Si el importe de entregas de bienes y prestaciones de servicios no supera **50.000 €** en el trimestre ni en ninguno de los **4 trimestres anteriores** | **Trimestral**, 1–20 siguiente al trimestre |
| Si se supera el umbral a mitad de trimestre | Se pasa a mensual: hay que presentar el periodo corrido |

## 2. Claves de operación

| Clave | Operación |
|---|---|
| **A** | Adquisiciones intracomunitarias de bienes |
| **E** | Entregas intracomunitarias de bienes |
| **T** | Entregas en otro Estado miembro subsiguientes a una adquisición intracomunitaria exenta (operaciones triangulares) |
| **S** | Prestaciones de servicios localizadas en otro Estado miembro |
| **I** | Adquisiciones de servicios localizadas en el TAI |
| **M** | Entregas de bienes sin impuesto tras una importación exenta |
| **H** | Entregas de bienes efectuadas por el representante fiscal |
| **R** | Transferencias de bienes en acuerdos de **venta en consigna** |
| **D** | Devoluciones de bienes desde acuerdos de venta en consigna |
| **C** | Sustituciones del destinatario en acuerdos de venta en consigna |

## 3. Los cuatro requisitos de la exención del art. 25 LIVA

Para facturar una entrega intracomunitaria de bienes **sin IVA** hacen falta los cuatro:

1. **Transmisión del poder de disposición** sobre bienes corporales.
2. **Transporte efectivo** desde España a otro Estado miembro, acreditado. Prueba: CMR
   firmado en destino, carta de porte, factura del transportista, albarán de recepción.
   El Reglamento (UE) 282/2011 (art. 45 bis) establece presunciones con dos medios de
   prueba no contradictorios de partes independientes.
3. **Destinatario identificado a efectos de IVA en otro Estado miembro**, con NIF-IVA
   **válido en VIES a la fecha de la operación**. Desde la Directiva 2018/1910 este es un
   requisito **material**, no formal: sin él, no hay exención.
4. **Declaración correcta en el modelo 349**. También requisito material desde 2020.

**Práctica del despacho**: consulta el NIF-IVA en VIES en cada operación y **guarda el
justificante con fecha**. Sin ese justificante, en una comprobación la exención decae y
la AEAT liquida el 21 % sobre la base, con sanción.

## 4. Errores frecuentes

1. Facturar sin IVA a un cliente de la UE **antes de estar de alta en el ROI**.
2. No comprobar el NIF-IVA en VIES, o comprobarlo una sola vez al dar de alta al cliente.
3. Declarar servicios en Intrastat (no van) o bienes solo en Intrastat y no en el 349.
4. Confundir clave **S** (servicios prestados) con **E** (entrega de bienes).
5. No presentar el 349 en un periodo sin operaciones cuando ya se ha superado el umbral:
   hay que presentarlo, aunque sea sin contenido, mientras subsista la obligación censal.
6. Olvidar el paso a periodicidad mensual al superar los 50.000 €.
7. Declarar la operación triangular como entrega ordinaria en lugar de con clave **T**.
8. No declarar las **transferencias de bienes propios** a un almacén en otro Estado
   miembro (clave E por el valor de la mercancía, aunque no haya venta).

## 5. Rectificaciones

Los errores de periodos anteriores **no** se corrigen con una declaración complementaria
del periodo antiguo: se consignan en el **bloque de rectificaciones** del 349 del periodo
corriente, indicando el ejercicio y el periodo rectificados y el importe correcto.

## 6. Generar el fichero

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_informativa.py \
  --modelo 349 --ejercicio 2026 \
  --declarante clientes/<NIF>/declarante.json \
  --detalle    clientes/<NIF>/operadores-2026-07.csv \
  --salida     salidas/349-2026-07.txt \
  --periodo 3T \
  --sin-validar-nif \
  --acepto-diseno-no-verificado
```

Columnas: `codigo_pais_operador`, `nif_operador_intracomunitario` (sin prefijo),
`nombre_operador`, `clave_operacion`, `base_imponible`. Usa `--sin-validar-nif` porque
los identificadores son extranjeros; valida los NIF-IVA con
`scripts/lib/validaciones.py` y, sobre todo, en **VIES**.

El modelo exige el **periodo**: pásalo con `--periodo` (`01`-`12` mensual, `1T`-`4T`
trimestral, `0A` anual). Sin él, el generador aborta indicando el campo que falta.

## 7. Cuadre

- [ ] Σ bases con clave **E** ↔ casilla 59 del modelo 303 del periodo
- [ ] Σ bases con clave **A** ↔ casillas 10-11 del 303 (y las mismas en deducible, 36-37)
- [ ] Σ clave **S** ↔ facturas de servicios a empresas de la UE, sin IVA
- [ ] Σ clave **I** ↔ facturas de proveedores UE con inversión del sujeto pasivo
- [ ] Entregas de bienes del 349 ↔ Intrastat de expedición (la diferencia debe explicarse
      por servicios y por operaciones no sujetas a Intrastat)
- [ ] Anual: Σ 349 ↔ apartado 9 del modelo 390
