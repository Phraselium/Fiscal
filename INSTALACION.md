# Instalación

## 1. Instalar el plugin

En Claude Code, escribe:

```
/plugin marketplace add Phraselium/Fiscal
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Reinicia Claude Code para que cargue las skills, los comandos y los agentes.

Comprueba que ha entrado con `/plugin` (debe aparecer `asesoria-fiscal-es` como instalado)
y escribiendo `/cartera` — si el comando existe, la instalación es correcta.

## 2. Instalar la dependencia

El control de cartera necesita `openpyxl`; el resto del plugin funciona con la biblioteca
estándar de Python 3.10 o superior.

```bash
pip install openpyxl
```

## 3. Preparar el directorio de trabajo

Crea (o abre) la carpeta desde la que vas a trabajar con Claude Code. **El
`Control.xlsx` va aquí, no dentro del plugin.**

```
mi-despacho/
├── Control.xlsx          ← tu fichero de control
├── clientes/             ← expedientes
└── salidas/              ← ficheros generados
```

Los scripts se invocan con `${CLAUDE_PLUGIN_ROOT}`, así que encuentran sus datos estén
donde estén; los ficheros tuyos se buscan en el directorio desde el que trabajas.

Prueba:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/control.py" --fichero Control.xlsx resumen
```

O simplemente pídeselo a Claude: «¿cómo vamos este trimestre?».

## 4. Configurar el despacho

Copia la configuración a un fichero local y rellénala ahí:

```bash
cp "$CLAUDE_PLUGIN_ROOT/config/configuracion.md" ./configuracion-despacho.md
```

Rellena NIF del presentador, CCAA de referencia, certificado y criterios internos. **No
subas este fichero a ningún repositorio público.**

## 5. Revisar qué cifras hay que verificar

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/parametros.py" revisar
```

Saca los parámetros marcados como `volatil` (cambian cada ejercicio) y `sin_verificar`.
Contrástalos con `/verificar-normativa` antes de usarlos en un entregable.

---

## Si vas a modificar el plugin

Clónalo y añádelo como marketplace local, así los cambios se aplican al instante:

```bash
git clone https://github.com/Phraselium/Fiscal.git
cd Fiscal
pip install -r requirements.txt
python3 scripts/comprobar_privacidad.py --instalar-hook
python3 tests/test_plugin.py
```

Y en Claude Code:

```
/plugin marketplace add /ruta/absoluta/a/Fiscal
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Trabajando desde el directorio del repo, los scripts funcionan sin `CLAUDE_PLUGIN_ROOT`:
las rutas usan `${CLAUDE_PLUGIN_ROOT:-.}`, que cae en `.` si la variable no está definida.

**Antes de cada commit**, el hook de pre-commit comprueba que no se cuela ningún dato de
cliente. Si quieres vigilar también las razones sociales de tu cartera:

```bash
cp datos/nombres_privados.ejemplo.txt datos/nombres_privados.txt
# y edítalo con los nombres a vigilar (el fichero está en .gitignore)
```

## Actualizar

```
/plugin marketplace update asesoria-fiscal-es
```

Después de actualizar, vuelve a pasar `parametros.py revisar`: los parámetros volátiles
siguen necesitando verificación en cada ejercicio, la actualice quien la actualice.
