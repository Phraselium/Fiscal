# Generación de ficheros para la AEAT

## 1. Qué hace y qué no hace

El plugin **genera y valida** el fichero. **No presenta**. El flujo completo es:

```
datos del cliente → normalización → generación del fichero → validación estructural
   → REVISIÓN HUMANA → importación en el formulario de la sede → presentación con certificado
```

Di siempre al usuario en qué paso está. Nunca afirmes que una declaración «se ha
presentado»: lo que existe es un fichero pendiente de importar.

## 2. Herramientas

| Script | Para qué |
|---|---|
| `scripts/generar_informativa.py` | Cualquier informativa con diseño en `disenos/` |
| `scripts/generar_intrastat.py` | Declaración Intrastat (ver skill `intrastat`) |
| `scripts/validar_fichero.py` | Validar y descomponer campo a campo un fichero ya generado |
| `scripts/calcular_plazos.py` | Vencimientos, periodo voluntario, recargos del art. 27 y 28 LGT |
| `scripts/lib/validaciones.py` | NIF, NIE, CIF, NIF-IVA, IBAN, NC8, referencia catastral |

## 3. Generar una informativa

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_informativa.py \
  --modelo 190 \
  --ejercicio 2025 \
  --declarante clientes/B12345674/declarante.json \
  --detalle   clientes/B12345674/perceptores.csv \
  --salida    salidas/190-2025-B12345674.txt
```

**Fichero del declarante** (JSON):
```json
{
  "nif_declarante": "B12345674",
  "denominacion_declarante": "RAZON SOCIAL SL",
  "telefono_contacto": "911234567",
  "persona_contacto": "APELLIDO APELLIDO NOMBRE",
  "numero_identificativo": "1900000000001"
}
```
El **número identificativo** son 13 dígitos que empiezan por el código del modelo y
los asigna el declarante; debe ser único por declaración y ejercicio.

**Fichero de detalle** (CSV con `;` o JSON): la cabecera debe usar los nombres de campo
del diseño. Ver `ejemplos/perceptores_190.csv`. Los importes admiten `1234.56` y
`1.234,56`; los negativos se graban con el campo de signo correspondiente.

**Opciones útiles**:

| Opción | Efecto |
|---|---|
| `--complementaria` / `--sustitutiva` | Marca la declaración y exige `--identificativo-anterior` |
| `--campo-importe-total` / `--campo-retencion-total` | Fuerza qué columna suma en la cabecera |
| `--periodo 3T` | Periodo, en los modelos que lo exigen (349) |
| `--diseno ruta.json` | Usa un diseño alternativo |
| `--sin-validar-nif` | Necesario si hay perceptores con identificador extranjero |
| `--acepto-diseno-no-verificado` | Obligatoria mientras el diseño esté marcado como borrador |

## 4. El bloqueo de diseño no verificado

Los diseños que se distribuyen llevan `"verificado": false`. El generador **aborta**
(código 3) e imprime qué bloques faltan por contrastar. Es intencionado: un diseño con
las posiciones mal produce un fichero que la AEAT rechaza, y peor, uno que acepta con
datos desplazados.

Antes de usar un modelo en producción, sigue `disenos/README.md`: localiza el anexo de
la orden vigente en el BOE, contrasta campo a campo, corrige el JSON y marca
`"verificado": true` con la fecha y la referencia contrastada. `Diseno.comprobar()`
detecta automáticamente huecos y solapamientos al cargar, así que un error de posición
no pasa desapercibido.

Si el usuario pide generar igualmente, usa `--acepto-diseno-no-verificado` **y advierte
en la respuesta** de que el fichero debe pasar por el validador de la sede antes de
darlo por bueno.

## 5. Añadir el diseño de un modelo nuevo

1. Copia `disenos/190.json` como plantilla.
2. Abre el anexo de diseños de registro de la orden del modelo.
3. Traduce cada campo a una entrada `{"nombre", "desde", "hasta", "tipo"}`.
   - Los tramos sin uso van como `{"tipo": "X"}` (blancos).
   - Los importes van como `"I"` y su signo como `"S"` con `campo_importe`.
   - Los campos con valor fijo, como `"C"`.
4. Los campos deben cubrir **exactamente** las posiciones 1..250 de cada registro; el
   cargador lo comprueba y falla si hay hueco o solapamiento.
5. Genera un fichero de prueba con 2-3 registros e impórtalo en el formulario de la sede.

## 6. Validar antes de subir

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/validar_fichero.py salidas/190-2025.txt --modelo 190 --detallar 3
```

Comprueba codificación ISO-8859-1, longitud de registro, separador CRLF, tipos de
registro y presencia de la cabecera; y descompone los primeros registros campo a campo
para una revisión visual. Revisa siempre a ojo el primer registro de detalle: es donde
se ven los desplazamientos.

## 7. Reglas de normalización que aplica el motor

- Texto en **mayúsculas y sin acentos**, conservando `Ñ` y `Ç`; se trunca si excede.
- NIF sin guiones ni espacios, 9 posiciones.
- Importes en **céntimos**, sin coma, alineados a la derecha con ceros.
- Signo en campo propio: `" "` positivo, `"N"` negativo.
- Numéricos alineados a la derecha con ceros; alfanuméricos a la izquierda con espacios.

## 8. Antes de generar, cuadra

No generes un fichero sin haber cuadrado los totales contra las autoliquidaciones
periódicas. Es la comprobación que evita el 90 % de los requerimientos:

| Informativa | Debe cuadrar con |
|---|---|
| 190 | Suma de los cuatro (o doce) modelos 111 |
| 180 | Suma de los modelos 115 |
| 193 | Suma de los modelos 123 |
| 390 | Suma de los modelos 303 |
| 347 | Libros registro de IVA, y con el 347 de la contraparte |
| 349 | Casillas 59/60 del 303 y libros de facturas emitidas |
| 200 | Contabilidad, cuentas depositadas, 190/180/193 y 347 |

Si un cuadre no sale, **para y explica la diferencia** antes de generar nada.

## 9. Plazos y recargos

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py plazo      --notificacion 15/09/2026 --meses 1
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py plazo      --notificacion 15/09/2026 --dias-habiles 10
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py voluntaria --notificacion 03/10/2026
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py recargo    --fin-plazo 20/07/2026 --presentacion 05/11/2026 --cuota 4500
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py ejecutivo  --cuota 4500
```

El cálculo de días hábiles solo excluye sábados y domingos: pasa los festivos con
`--festivos 12/10/2026,01/11/2026`. Verifica el calendario laboral estatal, autonómico
y local antes de apurar un plazo.
