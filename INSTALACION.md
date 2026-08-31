# Instalación

Hay dos formas de usar esto, según dónde trabajes.

| | Claude Code | claude.ai (web, escritorio, móvil) |
|---|---|---|
| Cómo se instala | Marketplace | Subiendo un `.zip` |
| Comandos `/` | ✅ los 10 | ❌ no existen en claude.ai |
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
├── referencias/      8 materias, con el detalle en subcarpetas
├── flujos/           9 ficheros — los comandos convertidos en procedimientos
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

### Actualizar — **no es automático**

Una skill de claude.ai es una **copia**, no un enlace al repositorio. Aunque el repo
cambie, tu skill se queda en la versión que subiste. Para actualizarla:

```bash
git pull
python3 scripts/empaquetar_skill.py
```

y vuelve a subir el `.zip` en Ajustes → Capacidades → Skills. Sustituye a la anterior.

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

Claude Code refresca los marketplaces **en segundo plano**, así que acaba enterándose
solo de los cambios del repositorio. Pero eso no es inmediato, y hasta que no reinicias
sigues usando lo que se cargó al arrancar la sesión.

Para forzarlo:

```
/plugin marketplace update asesoria-fiscal-es
```

y **reinicia Claude Code**: las skills y los comandos se cargan al arrancar.

**Comprueba que ha entrado por la versión, no por lo que recuerdes.** Abre `/plugin` y mira
la que tienes instalada:

| Versión | Qué verás |
|---|---|
| `1.0.0` | La estructura vieja: 34 skills, una por modelo. No entró la actualización. |
| `2.0.0` | La actual: 9 skills por tipo de trabajo y 11 comandos, con `/bancos`. |

Si sigue en `1.0.0` después de reiniciar, desinstala y vuelve a instalar:

```
/plugin uninstall asesoria-fiscal-es@asesoria-fiscal-es
/plugin marketplace update asesoria-fiscal-es
/plugin install asesoria-fiscal-es@asesoria-fiscal-es
```

Después de actualizar, vuelve a pasar `parametros.py revisar`: los parámetros volátiles
siguen necesitando verificación en cada ejercicio, la actualice quien la actualice.

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

**Después de cambiar skills o comandos**, tres cosas que no se hacen solas:

```bash
# 1. sube la version en .claude-plugin/plugin.json y en marketplace.json
# 2. actualiza el inventario en .claude-plugin/huella.json
python3 scripts/empaquetar_skill.py   # 3. regenera el .zip de claude.ai
```

La versión es lo único que mira Claude Code para decidir si recarga el plugin: si cambias
las skills y no la subes, nadie del despacho verá el cambio aunque el repositorio esté
bien. `tests/test_plugin.py` falla si te lo saltas.
