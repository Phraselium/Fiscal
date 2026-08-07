---
name: marco-fiscal-espanol
description: Reglas de trabajo transversales para cualquier tarea de asesoría fiscal española (AEAT, IRPF, IVA, IS, LGT). Úsala SIEMPRE al inicio de cualquier consulta fiscal, cálculo de impuestos, revisión de declaraciones, redacción de escritos a Hacienda o análisis de normativa tributaria. Establece la jerarquía de fuentes, la prohibición de inventar cifras, cómo consultar los parámetros y el formato de los entregables.
---

# Marco de trabajo fiscal

Contrato base. Se aplica por encima de cualquier otra skill.

## 1. Las tres reglas que no se saltan

### No memorices cifras: consúltalas
```bash
python3 scripts/parametros.py buscar iva          # tipos, umbrales, límites
python3 scripts/parametros.py ver is.tipo.microempresa
python3 scripts/parametros.py revisar             # qué NO es fiable
```
Si el parámetro sale como `volatil` o `sin_verificar`, **no lo uses en un entregable sin
contrastarlo**. Escribe `⚠️ SIN VERIFICAR — contrastar en <fuente>` junto al dato. Nunca
presentes como verificado algo que no lo está.

Datos que **siempre** cambian: tipos del IS de microempresa y ERD, límites de módulos,
interés de demora, tramos del RETA, deducciones y escalas autonómicas, tipos temporales de
IVA, calendario de VeriFactu, umbrales de Intrastat.

### No inventes referencias
Cita el **artículo concreto**. Si no estás seguro del número de una consulta de la DGT o
del ECLI de una sentencia, describe el criterio sin numerarlo y márcalo como pendiente de
localizar. Una referencia inventada es peor que ninguna.

### No leas el control entero
Para cualquier pregunta sobre varios clientes usa `scripts/control.py` (skill
`control-de-cartera`). Volcar la matriz al contexto cuesta ~15.000 tokens y no hace falta.

## 2. Antes de responder

1. **Ejercicio fiscal**. Si no está claro, pregúntalo: la respuesta cambia cada año.
2. **Territorio**: común, foral (Álava, Bizkaia, Gipuzkoa, Navarra), Canarias (IGIC),
   Ceuta/Melilla (IPSI). En foral **no** aplica la normativa estatal: avisa y detente.
3. **CCAA** si hay IRPF, ISD, ITP o IP de por medio.
4. **Régimen del contribuyente** y cifra de negocios del año anterior.

## 3. Jerarquía de fuentes

Ley → Reglamento → doctrina vinculante (DGT, TEAC art. 239.8 LGT) → jurisprudencia (TS,
TJUE, que prevalece en IVA) → criterios internos (`config/configuracion.md`).

En ISD, ITP-AJD, IP y en el tramo autonómico del IRPF, la norma de la **CCAA desplaza** a
la estatal en lo que haya asumido.

Normas base: LGT 58/2003 · LIRPF 35/2006 y RIRPF 439/2007 · LIVA 37/1992 y RIVA 1624/1992 ·
LIS 27/2014 y RIS 634/2015 · RGAT 1065/2007 · TRLIRNR 5/2004 · ISD 29/1987 · ITPAJD 1/1993 ·
IP 19/1991 · facturación RD 1619/2012 · VeriFactu RD 1007/2023.

## 4. Método

```
HECHOS → CALIFICACIÓN → SUJECIÓN → DEVENGO → BASE → TIPO/CUOTA
      → OBLIGACIONES (modelo, plazo, forma) → RIESGO → RECOMENDACIÓN
```

Ante una posición discutible, cuantifica siempre: cuota + recargo o sanción + intereses =
exposición total, y la probabilidad de comprobación con su motivo.

## 5. Prohibiciones

- No presentes nada ante la AEAT. El plugin **prepara**; presenta una persona con
  certificado, desde Sage o desde la sede.
- No propongas simulación, ocultación de rentas, facturación falsa ni interposición
  societaria artificiosa. Economía de opción sí; fraude no.
- No trates ninguna salida como definitiva sin revisión humana.
- No escribas en el Control.xlsx sin `--simular` primero y confirmación del usuario.

## 6. Entregables

**Nota interna**: `ANTECEDENTES · NORMATIVA · ANÁLISIS · CONCLUSIÓN · RIESGOS ·
ACCIONES Y PLAZOS`.

**A cliente**: empieza por la conclusión y la acción con su fecha límite. Lenguaje llano.
Importes `1.234,56 €`. Cierra con el aviso legal de `config/configuracion.md`.

**A la Administración**: `HECHOS` numerados → `FUNDAMENTOS DE DERECHO` → `SOLICITA` →
documentos que se acompañan. Ver agente `redactor-fiscal`.

## 7. Convenciones

Fechas `DD/MM/AAAA`. Importes con `.` de miles y `,` decimal. Modelo + periodo + ejercicio
(«303, 2T/2025»). Distingue días **hábiles** de naturales; los plazos por meses van de
fecha a fecha (art. 30.4 Ley 39/2015). Valida los NIF antes de usarlos
(`scripts/lib/validaciones.py`).

## 8. Datos de clientes

Alta sensibilidad económica. No los reproduzcas fuera del expediente; anonimiza en
plantillas y ejemplos. El despacho es sujeto obligado de la Ley 10/2010: ante indicios de
operativa sospechosa, escálalo al responsable de cumplimiento, no lo resuelvas como un
problema técnico.

## 9. Herramientas

| Necesidad | Herramienta |
|---|---|
| Estado de la cartera, qué falta, qué vence | `scripts/control.py` |
| Tipos, umbrales, límites | `scripts/parametros.py` |
| Plazos, recargos del art. 27 y 28 | `scripts/calcular_plazos.py` |
| Validar NIF, NIE, CIF, NIF-IVA, IBAN, NC8 | `scripts/lib/validaciones.py` |
| Intrastat | `scripts/generar_intrastat.py` |
| Ficheros de informativas fuera de Sage | `scripts/generar_informativa.py` |
