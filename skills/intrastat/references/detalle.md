# Intrastat

## 1. Qué es y qué no es

Intrastat es una **declaración estadística** (Reglamento (UE) 2019/2152 y Reglamento de
Ejecución (UE) 2020/1197), no tributaria, gestionada por el Departamento de Aduanas e
Impuestos Especiales de la AEAT. Recoge los movimientos **físicos de bienes** entre
España y otros Estados miembros.

| Intrastat | Modelo 349 |
|---|---|
| Solo **bienes** | Bienes **y servicios** |
| Estadística de movimiento físico | Declaración fiscal de operaciones |
| Solo si se superan los umbrales | Cualquier importe |
| Días 1-12 del mes siguiente | Días 1-20 del periodo siguiente |
| Departamento de Aduanas | Gestión Tributaria |

**No son intercambiables.** Un cliente puede tener que presentar los dos, solo el 349,
o —muy raramente— solo Intrastat. Un traslado de mercancía propia a un almacén en otro
Estado miembro va en Intrastat aunque no haya venta.

## 2. Obligación y umbrales

- Dos flujos **independientes**: **INTRODUCCIÓN** (llegadas, flujo A) y **EXPEDICIÓN**
  (salidas, flujo D). Se supera el umbral en uno y no en el otro con frecuencia.
- Umbral de exención en España: **400.000 €** anuales por flujo.
  ⚠️ **Verifícalo cada año**: lo fija la orden anual del Ministerio de Hacienda y ha
  cambiado en el pasado.
- Una vez superado el umbral en un año, la obligación **nace el mes en que se supera** y
  se mantiene durante todo el año siguiente completo.
- Existe además un **umbral estadístico** superior a partir del cual hay que informar
  del valor estadístico además del facturado. Verifica el vigente.
- Si en un mes obligado no hay operaciones, se presenta declaración **sin operación**.
  No presentar nada es una falta.

## 3. Qué se incluye y qué no

**Sí**: compraventas de bienes entre Estados miembros; transferencias de bienes propios
(stock a almacén, consignación); trabajos por encargo (perfeccionamiento) declarando el
movimiento físico en ambos sentidos; devoluciones (con la naturaleza de transacción de
devolución); entregas de bienes con instalación cuando hay movimiento físico; leasing
financiero superior a 24 meses.

**No**: prestaciones de servicios; mercancías en tránsito; muestras sin valor comercial;
material publicitario; medios de pago de curso legal y oro monetario; bienes en régimen
aduanero de tránsito; reparaciones (desde la revisión de la metodología); operaciones con
terceros países (van por **DUA**, no por Intrastat).

⚠️ **Canarias, Ceuta y Melilla están fuera del territorio aduanero a efectos de IVA**:
sus movimientos con la Península **no** son Intrastat.

## 4. Datos de cada línea

| Dato | Descripción | Obligatorio |
|---|---|---|
| `estado_miembro` | País de destino (expedición) o de procedencia (introducción), ISO-2. Nunca `ES` | Sí |
| `pais_origen` | País de origen de la mercancía, ISO-2 | Sí en expedición (desde 2022) |
| `provincia` | Provincia de destino o de origen en España, 2 dígitos | Sí |
| `condiciones_entrega` | Incoterm: EXW, FCA, CPT, CIP, DAP, DPU, DDP, FAS, FOB, CFR, CIF | Según umbral |
| `naturaleza_transaccion` | Código de 1-2 dígitos: 11 compraventa firme, 12 venta a prueba, 21/22 devoluciones y sustituciones, 31/32 operaciones sin contrapartida, 41/42 perfeccionamiento… | Sí |
| `modalidad_transporte` | 1 marítimo, 2 ferrocarril, 3 carretera, 4 aéreo, 5 correo, 7 instalaciones fijas, 8 navegación interior, 9 propulsión propia | Sí |
| `codigo_nc8` | Partida arancelaria de la Nomenclatura Combinada, **8 dígitos** | Sí |
| `masa_neta` | Kilogramos sin embalaje, 3 decimales | Sí, salvo si la partida exige unidad suplementaria |
| `unidades_suplementarias` | La que exija el arancel para esa partida (unidades, litros, m²…) | Cuando el arancel la exija |
| `importe_facturado` | Base de la factura en euros, sin IVA | Sí |
| `importe_estadistico` | Valor en frontera española (ajusta portes y seguros según el incoterm) | Sobre el umbral estadístico |
| `regimen_estadistico` | Código de régimen | Sí |
| `nif_iva_contraparte` | NIF-IVA del cliente comunitario, con prefijo de país | **Sí en expedición** (desde 2022) |
| `puerto_aeropuerto` | Puerto o aeropuerto de carga/descarga | Según flujo y umbral |

**El código NC8 es el dato crítico**: determina el arancel, la unidad suplementaria y los
cruces que hace Aduanas. Consúltalo en el **TARIC** para el año en curso; cambia cada
1 de enero. No lo copies de un ejercicio anterior sin comprobar que sigue vigente.

## 5. Generar el fichero

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_intrastat.py \
  --flujo expedicion \
  --periodo 2026-07 \
  --declarante clientes/B12345674/declarante_intrastat.json \
  --lineas    clientes/B12345674/movimientos-2026-07.csv \
  --salida    salidas/intrastat-D-2026-07.csv
```

`--flujo` acepta `introduccion` o `expedicion`. Genera un flujo por fichero: son
declaraciones independientes.

El script **valida antes de escribir** y aborta si encuentra incidencias (código 1):
- Estado miembro inexistente o igual a `ES`.
- Código NC8 que no tiene 8 dígitos.
- Importe facturado nulo o negativo.
- Masa neta a cero sin unidades suplementarias.
- Falta del NIF-IVA de la contraparte o del país de origen en expedición.
- NIF-IVA con prefijo que no es de un Estado miembro, o NIF español mal formado.

Con `--forzar` genera igualmente e imprime las incidencias: úsalo solo cuando sepas por
qué una línea es una excepción legítima.

## 6. Después de generar

1. Sube el fichero en el **portal Intrastat de la sede electrónica de la AEAT**
   (Aduanas e II.EE.). El validador del portal devuelve los errores línea a línea.
2. Verifica el orden y los nombres de las columnas contra la **guía Intrastat del
   ejercicio** antes del primer envío de cada año: la estructura del fichero de carga la
   fija el Departamento de Aduanas y ha cambiado con la revisión de la metodología.
3. Guarda el acuse en `clientes/<NIF>/06-intrastat/<ejercicio>/`.

## 7. Plazo y rectificaciones

- **Días 1 a 12** del mes siguiente al periodo de referencia. Verifica el calendario
  anual de Aduanas: hay adaptaciones por festivos.
- Rectificaciones: se presenta una declaración rectificativa del periodo afectado. Las
  correcciones por debajo del umbral de rectificación fijado por Aduanas pueden no ser
  exigibles; verifícalo antes de rehacer un periodo entero.
- Sanciones: régimen de la **Ley 12/1989 de la Función Estadística Pública** (no la LGT).

## 8. Cuadre mensual — checklist

- [ ] Facturas de venta a clientes de la UE del mes ↔ líneas de expedición
- [ ] Facturas de compra a proveedores de la UE del mes ↔ líneas de introducción
- [ ] Servicios excluidos (no van a Intrastat pero **sí** al 349)
- [ ] Transferencias de bienes propios incluidas aunque no haya factura
- [ ] Devoluciones con la naturaleza de transacción correcta, no como ventas negativas
- [ ] Códigos NC8 contrastados con el TARIC del año en curso
- [ ] NIF-IVA de los clientes comprobados en **VIES** (guarda el justificante)
- [ ] Suma de importes facturados ↔ casillas 59/60 del modelo 303 y ↔ modelo 349
      (la diferencia debe explicarse por servicios y por operaciones no Intrastat)
- [ ] Acumulado del año revisado contra el umbral, por cada flujo
