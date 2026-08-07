---
name: generacion-de-entregables
description: Producir los entregables del despacho: ficheros de declaraciones en el diseño de registro oficial de la AEAT, Intrastat, hojas de Excel, informes para el cliente, notas internas y escritos a Hacienda. Úsala cuando haya que generar un documento o un fichero, no solo calcularlo.
---

# Generación de entregables

## Qué se puede producir

| Entregable | Herramienta |
|---|---|
| Fichero de una informativa (190, 347, 349, 180, 193…) | `scripts/generar_informativa.py` |
| Fichero Intrastat para el portal de Aduanas | `scripts/generar_intrastat.py` |
| **Excel**: informes, cuadres, colas de trabajo, listados de facturas | `scripts/generar_excel.py` |
| Validar un fichero antes de subirlo | `scripts/validar_fichero.py` |
| Informe al cliente, nota interna, escrito a Hacienda | Plantillas de abajo |

Todos se invocan como `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/<script>.py`; empieza
por `--help`.

## Antes de generar nada: cuadra

No produzcas un fichero sin cuadrar los totales contra las autoliquidaciones del periodo.
Si un cuadre no sale, **para y explica la diferencia**. Detalle en
`references/ficheros-aeat.md`.

## Ficheros de la AEAT

Los diseños de registro se distribuyen como **borradores**: el generador aborta salvo que
se pase `--acepto-diseno-no-verificado`, e imprime qué bloques faltan por contrastar con
la orden ministerial. Es intencionado: un diseño con las posiciones mal produce ficheros
que Hacienda rechaza, o peor, acepta con los datos desplazados.

El flujo termina en un fichero pendiente de importar en la sede, nunca en una
presentación.

## Excel

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_excel.py \
  --datos informe.json --salida informe.xlsx --titulo "Cierre 2T/2026"
```
Acepta CSV o JSON y produce una hoja con cabecera, anchos ajustados, formato de importe
español y totales. Para varias hojas, pasa un JSON con `{"hojas": {...}}`.

## Documentos escritos

**Informe o comunicación al cliente**: empieza por la conclusión y la acción con su fecha
límite. Lenguaje llano, sin latinajos. Importes `1.234,56 €`. Cierra con el aviso legal
de `config/configuracion.md`.

**Nota interna**: `ANTECEDENTES · NORMATIVA · ANÁLISIS · CONCLUSIÓN · RIESGOS · ACCIONES
Y PLAZOS`.

**Escrito a la Administración**:
```
AL <ÓRGANO> — Expediente: <...>   CSV: <...>
D./D.ª <representante>, con NIF <...>, en nombre de <obligado>, NIF <...>,
según apoderamiento que consta en el Registro de Apoderamientos de la AEAT, DICE:

HECHOS            (un hecho por ordinal, con el documento que lo acredita)
FUNDAMENTOS DE DERECHO   (un argumento por ordinal; el más fuerte primero)
SOLICITA          (pretensión concreta y ejecutable)
DOCUMENTOS QUE SE ACOMPAÑAN
```
No reconozcas hechos no acreditados ni aportes documentación no requerida.

## Facturación

Requisitos de la factura, simplificadas, rectificativas, SII y VeriFactu en
`references/facturacion-e-informativas.md`. Las fechas de VeriFactu se han aplazado dos
veces: consúltalas antes de asesorar.
