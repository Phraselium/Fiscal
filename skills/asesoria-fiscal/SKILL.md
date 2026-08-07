---
name: asesoria-fiscal
description: Asesoría fiscal española: reglas de trabajo del despacho, jerarquía de fuentes, prohibición de inventar cifras y dónde está cada cosa. Úsala SIEMPRE al empezar cualquier tarea fiscal española, antes que ninguna otra.
---

# Asesoría fiscal — marco de trabajo

Contrato base del despacho. Se aplica por encima de cualquier otra skill.

## Las tres reglas que no se saltan

### 1. No memorices cifras: consúltalas
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar iva
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py ver is.tipo.microempresa
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py revisar    # qué NO es fiable
```
Lo que salga `volatil` o `sin_verificar` **no se usa en un entregable sin contrastarlo**:
escribe `⚠️ SIN VERIFICAR — contrastar en <fuente>` junto al dato.

Cambian todos los años: tipos del IS de microempresa y ERD, límites de módulos, interés
de demora, tramos del RETA, escalas y deducciones autonómicas, tipos temporales de IVA,
calendario de VeriFactu y umbrales de Intrastat.

### 2. No inventes referencias
Cita el artículo concreto. Si no estás seguro del número de una consulta de la DGT o del
ECLI de una sentencia, describe el criterio sin numerarlo y dilo. Una referencia
inventada es peor que ninguna.

### 3. Nada se presenta
El despacho prepara, calcula y cuadra. Presentar es un acto humano con certificado, desde
Sage o desde la sede. Nunca digas que una declaración «se ha presentado».

## Antes de responder

1. **Ejercicio fiscal**. Si no está claro, pregúntalo: la respuesta cambia cada año.
2. **Territorio**: común, foral (Álava, Bizkaia, Gipuzkoa, Navarra), Canarias (IGIC),
   Ceuta y Melilla (IPSI). En foral la normativa estatal **no** aplica: avisa y detente.
3. **CCAA** si hay IRPF, ISD, ITP o Patrimonio.
4. **Régimen del contribuyente** y cifra de negocios del año anterior.

## Método

```
HECHOS → CALIFICACIÓN → SUJECIÓN → DEVENGO → BASE → TIPO Y CUOTA
      → OBLIGACIONES (modelo, plazo, forma) → RIESGO → RECOMENDACIÓN
```
Ante una posición discutible: cuota + recargo o sanción + intereses = exposición total, y
la probabilidad de comprobación con su motivo.

## Qué skill usar

| Si la tarea es… | Skill |
|---|---|
| Una duda de IVA, IRPF, Sociedades, retenciones, autónomos o patrimonio | `consultas-por-impuesto` |
| Preparar, revisar o cuadrar un modelo concreto | `modelos-aeat` |
| Saber qué falta o qué vence en la cartera | `control-de-cartera` |
| Procesar lo que ha mandado un cliente | `entrada-de-documentos` |
| Producir un fichero, un Excel, un informe o un escrito | `generacion-de-entregables` |
| Ha llegado algo de Hacienda, o hay que calcular un plazo | `procedimientos-y-plazos` |
| Alta de cliente, encargo, calendario, blanqueo | `gestion-del-despacho` |

## Dónde está cada cosa

| Qué | Cómo se referencia |
|---|---|
| Ficheros del plugin: `scripts/`, `datos/`, `disenos/`, `config/` | `"${CLAUDE_PLUGIN_ROOT:-.}"/…` |
| Ficheros del despacho: `Control.xlsx`, expedientes, salidas | Ruta relativa al directorio de trabajo |

## Convenciones

Fechas `DD/MM/AAAA`. Importes `1.234,56 €`. Modelo + periodo + ejercicio («303, 2T/2025»).
Distingue días **hábiles** de naturales; los plazos por meses van de fecha a fecha
(art. 30.4 Ley 39/2015). Valida los NIF antes de usarlos.

## Prohibiciones

No propongas simulación, ocultación de rentas, facturación falsa ni interposición
societaria artificiosa: economía de opción sí, fraude no. No trates ninguna salida como
definitiva sin revisión humana. No escribas en el Control.xlsx sin `--simular` primero.

Los datos de clientes son de alta sensibilidad: anonimiza en plantillas y ejemplos. El
despacho es sujeto obligado de la Ley 10/2010; ante indicios de operativa sospechosa,
escálalo al responsable de cumplimiento en vez de tratarlo como un problema técnico.
