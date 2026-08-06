---
description: Prepara, revisa o genera cualquier modelo tributario español
argument-hint: <número de modelo> [ejercicio/periodo] [cliente]
---

Prepara el modelo indicado: **$ARGUMENTS**

Procedimiento:

1. Carga la skill `marco-fiscal-espanol` y `config/parametros-fiscales.md`.
2. Identifica el modelo en la skill `catalogo-modelos-aeat`. Si existe una skill
   específica (`modelo-303`, `modelo-190`, `modelo-200`…), úsala como referencia
   principal.
3. Confirma con el usuario los datos que falten y que cambien el resultado: ejercicio,
   periodo, régimen del contribuyente, CCAA, cifra de negocios del año anterior.
4. Localiza la documentación de partida en el expediente del cliente. Si no la
   encuentras, pídela explícitamente antes de calcular.
5. Calcula el modelo casilla a casilla, mostrando el detalle del cálculo.
6. **Cuadra** contra los modelos relacionados (periódicos ↔ resumen anual ↔ contabilidad).
   Si algo no cuadra, para y explica la diferencia antes de continuar.
7. Si el modelo admite fichero, ofrece generarlo con `scripts/generar_informativa.py` y
   validarlo con `scripts/validar_fichero.py`.
8. Indica el plazo de presentación, el de domiciliación y la fecha límite interna
   (vencimiento − 5 días hábiles).

Recuerda al final que el resultado es un **borrador** que requiere revisión humana y que
la presentación se hace en la sede electrónica con certificado.
