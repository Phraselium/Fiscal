# asesoria-fiscal-es

Plugin de Claude Code para el trabajo diario de un despacho de asesoría fiscal en España.
Cubre los modelos de la AEAT, el análisis normativo con cita de artículos, los
procedimientos tributarios, Intrastat, y la **generación de ficheros en los diseños de
registro oficiales listos para importar en la sede electrónica**.

## Instalación

```
/plugin marketplace add <usuario>/<repositorio>
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Después, completa `config/configuracion.md` con los datos del despacho y revisa
`config/parametros-fiscales.md`.

## Qué hace y qué no

| Hace | No hace |
|---|---|
| Calcula y cuadra cualquier modelo | Accede a la sede electrónica de la AEAT |
| Genera el fichero en el diseño de registro oficial | Firma con certificado o Cl@ve |
| Valida el fichero antes de subirlo | **Presenta** declaraciones |
| Redacta escritos, alegaciones y recursos | Domicilia pagos |
| Analiza normativa citando artículos | Sustituye la revisión del profesional |

El flujo es: **datos → cálculo → fichero → validación → revisión humana → importación y
presentación en la sede con certificado**. Todo lo que produce el plugin es un borrador.

## Comandos

| Comando | Para qué |
|---|---|
| `/modelo <n>` | Prepara, revisa o genera cualquier modelo |
| `/cierre-trimestre` | Cierre trimestral completo de un cliente |
| `/cierre-fiscal` | Cierre contable y fiscal del ejercicio (ajustes del IS) |
| `/campana-renta` | Prepara o revisa una declaración de IRPF |
| `/requerimiento` | Analiza una notificación de Hacienda y prepara la contestación |
| `/consulta-fiscal` | Resuelve una consulta con nota para el expediente |
| `/alta-cliente` | Onboarding con diagnóstico y calendario |
| `/calendario` | Obligaciones y plazos, generales o de un cliente |
| `/generar-fichero` | Fichero de una declaración listo para importar |
| `/intrastat` | Declaración Intrastat de un periodo |
| `/verificar-normativa` | Contrasta y actualiza los parámetros fiscales |
| `/verificar-diseno` | Contrasta un diseño de registro con la orden oficial |

## Skills

**Transversales**: `marco-fiscal-espanol` (reglas de trabajo, jerarquía de fuentes,
prohibición de inventar cifras), `catalogo-modelos-aeat` (todos los modelos, quién los
presenta y cuándo), `calendario-fiscal`, `gestion-de-despacho`, `generacion-de-ficheros`.

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
# Fichero de una informativa en diseño de registro
python3 scripts/generar_informativa.py --modelo 190 --ejercicio 2025 \
  --declarante ejemplos/declarante.json --detalle ejemplos/perceptores_190.csv \
  --salida salidas/190-2025.txt

# Intrastat listo para el portal de Aduanas
python3 scripts/generar_intrastat.py --flujo expedicion --periodo 2026-07 \
  --declarante ejemplos/declarante_intrastat.json \
  --lineas ejemplos/movimientos_intrastat.csv --salida salidas/intrastat-D-2026-07.csv

# Validar y descomponer campo a campo
python3 scripts/validar_fichero.py salidas/190-2025.txt --modelo 190 --detallar 3

# Plazos y recargos
python3 scripts/calcular_plazos.py recargo --fin-plazo 20/07/2026 \
  --presentacion 05/11/2026 --cuota 4500

# Validar NIF, NIE y CIF
python3 scripts/lib/validaciones.py 12345678Z B12345674
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

## Verificación de la normativa

El conocimiento del modelo tiene fecha de corte y la normativa tributaria cambia varias
veces al año. `config/parametros-fiscales.md` es una **referencia de trabajo**, no una
fuente oficial. Los datos que exigen verificación en cada ejercicio están marcados, y el
comando `/verificar-normativa` los contrasta contra el BOE, la sede de la AEAT y los
boletines autonómicos.

Cuando el plugin no puede verificar un dato, lo señala con
`⚠️ SIN VERIFICAR — contrastar en <fuente>` en vez de darlo por bueno.

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
