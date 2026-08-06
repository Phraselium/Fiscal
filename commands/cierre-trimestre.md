---
description: Ejecuta el cierre trimestral completo de un cliente y prepara todos sus modelos
argument-hint: <cliente o NIF> <trimestre, p. ej. 3T/2026>
---

Cierre trimestral de: **$ARGUMENTS**

1. **Determinar obligaciones**: lee el 036/037 del cliente (o su ficha en el expediente) y
   lista los modelos que le corresponden en este periodo. Usa la skill `calendario-fiscal`.

2. **Documentación**: verifica que está completa. Enumera expresamente lo que falta:
   facturas emitidas y recibidas, extractos bancarios conciliados, nóminas y seguros
   sociales, contratos nuevos, movimientos de inmovilizado.

3. **Contabilidad**: conciliación bancaria, periodificación, revisión de cuentas puente y
   de partidas pendientes de aplicación.

4. **Modelos**, en este orden y cuadrando entre sí:
   - **303** — libros de IVA emitidas y recibidas; AIB e ISP en devengado *y* deducible;
     casilla 67 contra la 72 del periodo anterior
   - **111** — nóminas, profesionales, administradores, dietas exentas
   - **115** — alquileres de local; comprobar retención y referencias catastrales
   - **123** — dividendos e intereses devengados en el periodo
   - **130/131** — acumulado desde el 1 de enero, con arrastre de negativos
   - **202** — solo en abril, octubre y diciembre
   - **349** — si hay operaciones intracomunitarias; comprobar periodicidad
   - **Intrastat** — si supera el umbral; días 1-12 del mes siguiente

5. **Cuadres cruzados**:
   - Casilla 59 del 303 ↔ clave E del 349
   - Casillas 10-11 del 303 ↔ clave A del 349 ↔ casillas 36-37
   - Bases del 111 ↔ gasto de personal y de servicios profesionales
   - Base del 115 ↔ cuenta 621

6. **Resultado**: tabla con modelo, resultado, plazo de presentación, plazo de
   domiciliación y fecha límite interna.

7. **Avisos al cliente**: importes a ingresar, fecha de cargo, y cualquier incidencia
   detectada (retenciones no practicadas, facturas sin datos, NIF-IVA no validados).

Marca claramente todo lo que quede pendiente de confirmación del cliente.
