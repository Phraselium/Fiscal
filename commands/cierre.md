---
description: Cierre trimestral, cierre del ejercicio o campaña de Renta
argument-hint: <trimestral | anual | renta> <cliente> <periodo>
---

**$ARGUMENTS**

Determina de qué cierre se trata y sigue el que corresponda.

**Trimestral** — carga `modelos-aeat` y `control-de-cartera`:
documentación completa → contabilidad conciliada → 303, 111, 115, 123, 130/131, 202 en
abril/octubre/diciembre, 349 → cuadres cruzados → tabla con resultado, plazo,
domiciliación y fecha límite interna.

**Anual (Sociedades)** — carga `consultas-por-impuesto` (sociedades) y `modelos-aeat`:
resultado contable → ajustes extracontables uno a uno con su artículo → reserva de
capitalización **contabilizada** → BIN dentro del límite → tipo del ejercicio verificado
→ cuota diferencial → obligaciones posteriores (232 en noviembre, libros, cuentas).

**Renta** — carga `consultas-por-impuesto` (irpf) y `modelos-aeat`:
datos fiscales contrastados con la documentación → situación familiar a 31/12 → rentas
por componente → compensación de saldos negativos de 4 años → **deducciones autonómicas
una a una** → comparativa individual vs. conjunta.

En los tres casos, cuadra antes de dar nada por bueno y marca lo que quede pendiente de
confirmación del cliente.
