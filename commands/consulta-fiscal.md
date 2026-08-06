---
description: Resuelve una consulta fiscal con análisis normativo y nota para el expediente
argument-hint: <la consulta>
---

Resuelve la consulta: **$ARGUMENTS**

Carga la skill `marco-fiscal-espanol` y aplica su método de análisis:

```
1. HECHOS         qué ha pasado, quién, cuándo, importes, documentación
2. CALIFICACIÓN   qué tipo de renta u operación es
3. SUJECIÓN       sujeto, no sujeto, exento
4. DEVENGO        cuándo nace la obligación y a qué periodo se imputa
5. BASE           cuantificación, gastos deducibles, reglas de valoración
6. TIPO Y CUOTA   tipo aplicable, deducciones y bonificaciones
7. OBLIGACIONES   modelo, plazo, forma de presentación, obligaciones formales
8. RIESGO         cuota + recargo o sanción + intereses si la AEAT discrepa
9. RECOMENDACIÓN
```

Requisitos de la respuesta:

- **Cita el artículo concreto** de cada norma que apliques.
- Si hay doctrina de la DGT o del TEAC relevante, indícala. Si no estás seguro del número
  de la consulta o del ECLI, describe el criterio y márcalo como pendiente de localizar la
  referencia. **No inventes referencias.**
- Verifica en fuente oficial cualquier cifra, tipo, umbral o plazo. Si no puedes
  verificarlo, escríbelo como `⚠️ SIN VERIFICAR — contrastar en <fuente>`.
- Si la respuesta depende de la CCAA, del ejercicio o del régimen del contribuyente y no
  lo sabes, **pregúntalo antes** de responder.
- Cuantifica el riesgo de las posiciones discutibles en una tabla.
- Entrega el resultado como **nota interna** con el formato de la skill, lista para
  archivar en el expediente.

Si el usuario pide además la comunicación al cliente, redáctala aparte en lenguaje llano,
empezando por la conclusión y la acción que debe realizar, y cerrando con el aviso legal
de `config/configuracion.md`.
