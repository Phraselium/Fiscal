# asesoria-fiscal-es

Plugin de Claude Code para el trabajo diario de un despacho de asesoría fiscal en España.
Cubre el control de la cartera, el análisis normativo con cita de artículos, los
procedimientos tributarios, Intrastat y la generación de ficheros para la sede
electrónica. Diseñado para usarse con ~85 clientes sin quemar contexto ni inventar cifras.

## Instalación

```
/plugin marketplace add Phraselium/Fiscal
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Guía completa en **[INSTALACION.md](INSTALACION.md)**.

Después:

```bash
pip install -r requirements.txt                        # openpyxl, solo para el control
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py --instalar-hook # bloquea commits con datos privados
python3 tests/test_plugin.py                            # 54 pruebas
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py revisar                   # qué cifras hay que contrastar
```

Y completa `config/configuracion.md` con los datos del despacho — pero **no lo subas
relleno**: el verificador de privacidad falla si detecta que ya no tiene placeholders.

## Contexto de uso

Despacho con ~85 clientes, control en **Control.xlsx** (matriz cliente × modelo) y
software **Sage Despachos Connected** (migración desde ContaPlus). Los clientes entregan
por cuatro canales: contabilidad en Sage, Excel, papel y PDF escaneado.

## Qué hace y qué no

| Hace | No hace |
|---|---|
| Responde sobre la cartera sin leer el Excel entero | Accede a la sede de la AEAT |
| Cuadra modelos entre sí y con la contabilidad | Firma con certificado o Cl@ve |
| Consulta parámetros y avisa de los no fiables | **Presenta** declaraciones |
| Normaliza documentación de clientes | Sustituye a Sage en lo que Sage ya hace |
| Redacta escritos, alegaciones y recursos | Sustituye la revisión del profesional |

**Sage genera y presenta los modelos.** El plugin no compite con eso: prepara los datos de
entrada, cuadra lo que Sage saca y cubre lo que Sage no cubre (Intrastat, 720, 232, 210,
escritos y procedimientos).

## Tres reglas de diseño

1. **Las cifras no se memorizan, se consultan.** `scripts/parametros.py` marca cada dato
   como `estable`, `verificado`, `sin_verificar` o `volatil`, con su fuente y su fecha.
   Lo que no es fiable sale marcado como tal en el entregable.
2. **El control no se lee entero.** `scripts/control.py` devuelve colas filtradas: un
   `resumen` cuesta ~600 tokens frente a los ~15.000 de volcar la matriz.
3. **Nada se presenta automáticamente.** Todo es borrador hasta que lo revisa una persona.

## Comandos

Escribe `/` en Claude Code y los verás todos con su descripción. `/fiscal` es el índice.

**Día a día** — `/cartera` · `/cierre-trimestre` · `/cuadrar` · `/calendario` · `/documentacion`

**Por impuesto** — `/iva` · `/irpf` · `/sociedades` · `/retenciones` · `/autonomos` ·
`/informativas` · `/patrimonio`

**Modelos** — `/modelo <n>` sirve para cualquiera · `/campana-renta` · `/cierre-fiscal` ·
`/intrastat` · `/generar-fichero`

**Hacienda y clientes** — `/requerimiento` · `/procedimientos` · `/consulta-fiscal` ·
`/alta-cliente` · `/despacho`

**Mantenimiento** — `/verificar-normativa` · `/verificar-diseno` · `/sage` · `/privacidad`

No hace falta usarlos: preguntando en lenguaje normal se carga solo lo que haga falta.

## Skills

**Operativas del despacho**: `control-de-cartera` (el Control.xlsx),
`sage-despachos` (migración y reparto de tareas con Sage),
`documentacion-de-clientes` (los cuatro canales de entrada).

**Transversales**: `marco-fiscal-espanol` (reglas de trabajo, jerarquía de fuentes,
prohibición de inventar cifras), `catalogo-modelos-aeat`, `calendario-fiscal`,
`gestion-de-despacho`, `generacion-de-ficheros`.

**Por impuesto**: `irpf`, `iva`, `impuesto-sociedades`, `retenciones-y-censos`,
`autonomos-y-modulos`, `informativas-y-facturacion`,
`patrimonio-sucesiones-y-no-residentes`, `procedimientos-tributarios`, `intrastat`.

**Por modelo**: `modelo-036-037`, `modelo-100`, `modelo-111`, `modelo-115-180`,
`modelo-123-193`, `modelo-130-131`, `modelo-190`, `modelo-200`, `modelo-202`,
`modelo-210`, `modelo-232`, `modelo-303`, `modelo-347`, `modelo-349`, `modelo-390`,
`modelo-714-718`, `modelo-720-721`.

## Agentes

- **`revisor-fiscal`** — segunda revisión antes de presentar. Rehace cálculos, cuadra
  entre modelos y clasifica los hallazgos por gravedad.
- **`redactor-fiscal`** — escritos a la Administración, notas internas y comunicaciones
  a cliente.

## Scripts

```bash
# Estado de la cartera (NO leas el Excel entero)
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py --fichero Control.xlsx resumen
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py --fichero Control.xlsx cola --estado Revisar
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py --fichero Control.xlsx cliente "EJEMPLO CLIENTE SL"
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py --fichero Control.xlsx huecos

# Cuadre entre modelos antes de presentar
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py --plantilla > cliente-2025.json
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/cuadrar.py --datos cliente-2025.json

# Parámetros fiscales, con aviso de los que no son fiables
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py ver verifactu.fecha_obligatoriedad
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py revisar

# Fichero de una informativa en diseño de registro
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_informativa.py --modelo 190 --ejercicio 2025 \
  --declarante ejemplos/declarante.json --detalle ejemplos/perceptores_190.csv \
  --salida salidas/190-2025.txt

# Intrastat listo para el portal de Aduanas
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_intrastat.py --flujo expedicion --periodo 2026-07 \
  --declarante ejemplos/declarante_intrastat.json \
  --lineas ejemplos/movimientos_intrastat.csv --salida salidas/intrastat-D-2026-07.csv

# Validar y descomponer campo a campo
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/validar_fichero.py salidas/190-2025.txt --modelo 190 --detallar 3

# Plazos y recargos
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/calcular_plazos.py recargo --fin-plazo 20/07/2026 \
  --presentacion 05/11/2026 --cuota 4500

# Validar NIF, NIE y CIF
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/lib/validaciones.py 12345678Z B12345674
```

Solo requieren Python 3.10+ de la biblioteca estándar. Sin dependencias externas.

## Diseños de registro

`disenos/*.json` describe, para cada modelo, qué campo ocupa cada posición del registro de
250 caracteres. El motor (`scripts/lib/registro.py`) no contiene lógica de ningún modelo:
cuando la AEAT publica una orden que cambia un diseño, se actualiza el JSON.

Los diseños que se distribuyen son **borradores** (`"verificado": false`). El generador
**se niega a escribir** un fichero con un diseño no verificado salvo que se pase
`--acepto-diseno-no-verificado`, y en todo caso imprime qué bloques faltan por contrastar.
Es intencionado: un diseño con posiciones erróneas produce ficheros que la AEAT rechaza,
o peor, que acepta con los datos desplazados.

Para ponerlos en producción: `/verificar-diseno <modelo>` y `disenos/README.md`.

## Privacidad

El plugin es código publicable; los datos del despacho no lo son. Tres capas:

1. **`.gitignore`** excluye toda hoja de cálculo, `clientes/`, `salidas/`, certificados
   y `datos/nombres_privados.txt`.
2. **`scripts/comprobar_privacidad.py`** revisa lo que va a subirse y falla si encuentra
   NIF, NIE o CIF **con letra de control válida** (un identificador inventado casi nunca
   valida; uno real, siempre), IBAN correctos, correos, teléfonos, ficheros prohibidos, o
   nombres de tu lista privada.
3. **Hook de pre-commit** con `--instalar-hook`: ningún commit se crea sin pasar la
   comprobación.

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py            # lo versionado
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py --staged   # lo que va a commit
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/comprobar_privacidad.py --historial # busca en todo el historial
```

Para vigilar los nombres de tu cartera, copia `datos/nombres_privados.ejemplo.txt` a
`datos/nombres_privados.txt` (ignorado por git) y pon un nombre por línea. Sin él, la
comprobación cubre identificadores y ficheros, pero no razones sociales.

Los ejemplos de `ejemplos/` usan NIF sintéticos y nombres inequívocamente ficticios. Las
pruebas generan sus identificadores en tiempo de ejecución, así que ningún NIF con letra
de control válida aparece escrito en el repositorio.

**Si algo privado llega a subirse**, no basta con corregirlo en un commit nuevo: hay que
reescribir el historial y forzar el push. Y aun así, GitHub conserva los commits
huérfanos accesibles por su SHA hasta que ejecuta su recolección de basura, y cualquier
fork o caché previo mantiene la copia. Ante una fuga real de datos de cliente, reescribe,
fuerza el push y abre un ticket a GitHub Support para que purguen los objetos.

## Pruebas

```bash
python3 tests/test_plugin.py      # 54 pruebas, ~0,2 s
python3 tests/test_plugin.py -v   # detalle
```

Cubren lo que puede romperse en silencio y costar dinero: validación de NIF, NIE, CIF,
IBAN y NC8; interpretación de importes en formato español e inglés; que los diseños de
registro cubran exactamente 250 posiciones; signo y codificación de los ficheros
generados; cómputo de plazos por meses y por días hábiles; los cuadres entre modelos; el
parseo del control; la coherencia de `parametros.json`; y que no haya datos privados
versionados.

Incluyen pruebas de regresión de tres defectos reales que aparecieron durante el
desarrollo: clientes con nombre corto que desaparecían del control, importes en formato
inglés multiplicados por 100, y referencias a scripts inexistentes.

## Verificación de la normativa

El conocimiento del modelo tiene fecha de corte y la normativa cambia varias veces al año.
`datos/parametros.json` marca cada dato con su estado y su fuente:

```
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py revisar
!!  VOLATILES (13)        cambian cada ejercicio — verificar SIEMPRE
?   SIN VERIFICAR (9)     del conocimiento del modelo — contrastar
    Fiables sin reverificar: 87/118
```

Dos errores reales detectados al construir esto, que ilustran por qué existe el mecanismo:

- **VeriFactu**: el RD-ley 15/2025 aplazó la obligación a **2027** (1 de enero para
  contribuyentes del IS, 1 de julio para el resto). Cualquier fuente que diga 2025 o 2026
  está desactualizada.
- **Tipos del IS de microempresa y ERD**: están en calendario transitorio decreciente y
  ninguna cifra de memoria es fiable. El parámetro sale sin valor y obliga a consultar el
  manual práctico del ejercicio.

`/verificar-normativa` contrasta los volátiles contra el BOE, la sede de la AEAT y los
boletines autonómicos, y actualiza el JSON con la fecha de verificación.

## Estructura

```
.claude-plugin/    plugin.json y marketplace.json
commands/          comandos de barra
skills/            conocimiento por impuesto, por modelo y transversal
agents/            revisor-fiscal y redactor-fiscal
scripts/           generadores, validador y calculadora de plazos
  lib/             motor de diseño de registro y validaciones
disenos/           diseños de registro en JSON, uno por modelo
config/            configuración del despacho y parámetros fiscales
ejemplos/          ficheros de muestra
plantillas/        plantillas de documentos
```

## Aviso

Este plugin es una herramienta de trabajo para profesionales. No sustituye el criterio
del asesor ni la consulta de la normativa vigente. Nada de lo que produce vincula a la
Administración tributaria, y todo requiere revisión humana antes de presentarse.
