# Instalación

Hay dos formas de usar esto, según dónde trabajes.

| | Claude Code | claude.ai (web, escritorio, móvil) |
|---|---|---|
| Cómo se instala | Marketplace | Subiendo un `.zip` |
| Comandos `/` | ✅ los 27 | ❌ no existen en claude.ai |
| Subagentes | ✅ revisor y redactor | ❌ se aplican como procedimiento |
| Conocimiento fiscal | ✅ | ✅ |
| Scripts (parámetros, plazos, cuadres, ficheros) | ✅ | ✅ |
| Control de cartera sobre tu `Control.xlsx` | ✅ | ⚠️ hay que adjuntar el fichero y depende de `openpyxl` |

**Si trabajas con la cartera entera y con ficheros del despacho, usa Claude Code.**
Para consultas fiscales sueltas desde el móvil o el navegador, claude.ai basta.

---

# A. claude.ai

## 1. Consigue el paquete

Descarga [`dist/asesoria-fiscal-es.zip`](dist/asesoria-fiscal-es.zip) del repositorio, o
constrúyelo tú:

```bash
git clone https://github.com/Phraselium/Fiscal.git
cd Fiscal
python3 scripts/empaquetar_skill.py
# → dist/asesoria-fiscal-es.zip
```

## 2. Súbelo

En claude.ai: **Ajustes → Capacidades → Skills → Subir skill**, y elige el `.zip`.

## 3. Úsalo

Pregunta con normalidad. La skill se activa sola cuando detecta una consulta fiscal
española:

> «¿Este alquiler de local lleva retención?»
> «Me ha llegado un requerimiento del 303 de 2024, ¿qué plazo tengo?»
> «Repartimos dividendos en marzo, ¿cuándo se devenga la retención?»

Para los flujos de trabajo, pídelos por su nombre: «haz el cierre trimestral de este
cliente», «prepara la contestación a este requerimiento», «cuadra estos modelos».

### Qué contiene el paquete

```
asesoria-fiscal-es/
├── SKILL.md          enrutador: qué hay y dónde está
├── referencias/      34 ficheros — el conocimiento, uno por materia y por modelo
├── flujos/           26 ficheros — los comandos convertidos en procedimientos
├── revision/          2 ficheros — revisor y redactor como procedimientos
├── scripts/          herramientas en Python
├── datos/            parametros.json
└── disenos/          diseños de registro de las informativas
```

Claude lee solo el fichero que necesita, no las 300 KB.

### Limitaciones en claude.ai

- **El control de cartera** necesita que adjuntes tu `Control.xlsx` a la conversación, y
  que el entorno tenga `openpyxl`. Si no lo tiene, pídele que lo instale.
- **No hay comandos de barra**: `flujos/` recoge los mismos procedimientos, pero se
  invocan pidiéndolos con palabras.
- **No hay subagentes**: la revisión independiente se aplica como procedimiento, no como
  una segunda pasada aislada.
- **Los datos de tus clientes viajan a la conversación** cuando adjuntas ficheros.
  Valóralo antes de subir un control con 85 clientes.

### Actualizar

Vuelve a construir el `.zip` y súbelo otra vez; sustituye a la versión anterior.

---

# B. Claude Code

## 1. Instala el plugin

```
/plugin marketplace add Phraselium/Fiscal
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Reinicia Claude Code. Comprueba escribiendo `/fiscal`: si sale el índice, está instalado.

## 2. Instala la dependencia

```bash
pip install openpyxl
```

Solo la necesita el control de cartera; el resto funciona con la biblioteca estándar de
Python 3.10 o superior.

## 3. Prepara el directorio de trabajo

Tu `Control.xlsx` va **en tu carpeta, no dentro del plugin**:

```
mi-despacho/          ← abre Claude Code aquí
├── Control.xlsx
├── clientes/
└── salidas/
```

Pruébalo: «¿cómo vamos este trimestre?».

## 4. Configura el despacho

```bash
cp "$CLAUDE_PLUGIN_ROOT/config/configuracion.md" ./configuracion-despacho.md
```

Rellena NIF del presentador, CCAA de referencia y criterios internos. **No subas ese
fichero a ningún repositorio público.**

## 5. Revisa qué cifras hay que verificar

```bash
python3 "$CLAUDE_PLUGIN_ROOT/scripts/parametros.py" revisar
```

Saca los parámetros `volatil` y `sin_verificar`. Contrástalos con `/verificar-normativa`
antes de usarlos en un entregable.

## Actualizar

```
/plugin marketplace update asesoria-fiscal-es
```

Después de actualizar, vuelve a pasar `parametros.py revisar`.

---

# C. Si vas a modificar el plugin

```bash
git clone https://github.com/Phraselium/Fiscal.git
cd Fiscal
pip install -r requirements.txt
python3 scripts/comprobar_privacidad.py --instalar-hook
python3 tests/test_plugin.py
```

Y en Claude Code, para que los cambios se apliquen al instante:

```
/plugin marketplace add /ruta/absoluta/a/Fiscal
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Trabajando desde el repo, los scripts funcionan sin `CLAUDE_PLUGIN_ROOT`: las rutas usan
`${CLAUDE_PLUGIN_ROOT:-.}`, que cae en `.` si la variable no está definida.

**Antes de cada commit**, el hook comprueba que no se cuela ningún dato de cliente. Para
vigilar también las razones sociales de tu cartera:

```bash
cp datos/nombres_privados.ejemplo.txt datos/nombres_privados.txt
```

**Después de cambiar skills o comandos**, regenera el paquete de claude.ai:

```bash
python3 scripts/empaquetar_skill.py
```

El `.zip` versionado en `dist/` no se actualiza solo.
