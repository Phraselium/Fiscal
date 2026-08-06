---
name: modelo-190
description: Modelo 190, resumen anual de retenciones e ingresos a cuenta del IRPF — claves y subclaves de percepción, datos por perceptor, situación familiar, dietas exentas con clave L, ejercicio de devengo, cuadre con los modelos 111 y generación del fichero en diseño de registro listo para importar. Úsala en enero para preparar, cuadrar o generar el 190 de un cliente.
---

# Modelo 190 — Resumen anual de retenciones

## 1. Quién y cuándo

- Lo presenta quien haya presentado modelos **111** en el ejercicio (o haya estado
  obligado a ello).
- **Plazo: 1 a 31 de enero** del año siguiente.
- Presentación electrónica; para volúmenes grandes, importando el **fichero** en el
  diseño de registro.

## 2. Claves de percepción

| Clave | Concepto |
|---|---|
| **A** | Rendimientos del trabajo: empleados por cuenta ajena en general |
| **B** | Pensiones y haberes pasivos (subclaves según origen) |
| **C** | Prestaciones y subsidios por desempleo |
| **D** | Prestaciones del sistema público y de sistemas privados de previsión social |
| **E** | Retribuciones a **administradores y miembros de consejos de administración** |
| **F** | Cursos, conferencias, seminarios y elaboración de obras literarias, artísticas o científicas con cesión de derechos |
| **G** | **Actividades profesionales** |
| **H** | Actividades económicas: agrícolas, ganaderas, forestales y empresariales en estimación objetiva |
| **I** | Premios por participación en juegos, concursos, rifas o combinaciones aleatorias |
| **J** | Imputación de rentas por cesión de derechos de imagen |
| **K** | Premios y ganancias de juegos con gravamen especial |
| **L** | **Rentas exentas y dietas exceptuadas de gravamen** |

Las **subclaves** matizan cada clave (p. ej., dentro de G, la subclave distingue el tipo
general del reducido de inicio de actividad; dentro de L, cada subclave identifica el
supuesto de exención: dietas de locomoción, manutención, indemnización por despido,
trabajos en el extranjero del art. 7.p…).

⚠️ La tabla de claves y subclaves se actualiza por orden ministerial. **Verifícala en la
ficha del modelo 190 del ejercicio antes de presentar.**

## 3. La clave L es la que más requerimientos genera

Las dietas exentas y las indemnizaciones por despido **no llevan retención**, pero **sí
deben declararse** en el 190 con clave L y su subclave. Si se omiten:
- La AEAT no ve el importe exento y lo cruza como renta no declarada del trabajador.
- El trabajador recibe una propuesta de liquidación en su Renta.

Revisa siempre las nóminas del ejercicio buscando conceptos exentos antes de generar.

## 4. Datos por perceptor

Además de NIF, nombre y provincia, el 190 recoge para cada perceptor la percepción
íntegra, las retenciones practicadas, las percepciones en especie con sus ingresos a
cuenta efectuados y repercutidos, el ejercicio de devengo (si es distinto del corriente),
la referencia a Ceuta y Melilla, y —en los rendimientos del trabajo— la situación
familiar, el grado de discapacidad, el tipo de contrato, los hijos y ascendientes
computados, las reducciones aplicadas, los gastos deducibles y las pensiones
compensatorias tenidas en cuenta para el cálculo del tipo de retención.

## 5. Generar el fichero

```bash
python3 scripts/generar_informativa.py \
  --modelo 190 --ejercicio 2025 \
  --declarante clientes/<NIF>/declarante.json \
  --detalle    clientes/<NIF>/perceptores.csv \
  --salida     salidas/190-2025.txt \
  --acepto-diseno-no-verificado
```

Columnas del CSV de detalle: `nif_perceptor`, `apellidos_nombre`, `codigo_provincia`,
`clave_percepcion`, `subclave`, `percepcion_integra`, `retenciones_practicadas`, y
opcionalmente `percepcion_especie`, `ingresos_cuenta_efectuados`,
`ingresos_cuenta_repercutidos`, `ejercicio_devengo`. Ver `ejemplos/perceptores_190.csv`.

El generador calcula los totales de la cabecera, valida los NIF y comprueba la estructura.
El diseño incluido está marcado como **borrador**: contrástalo con el anexo de la orden
vigente (`disenos/README.md`) antes de usarlo en producción, y valida siempre el fichero
importándolo en el formulario de la sede.

## 6. Cuadre antes de presentar

- [ ] Σ bases de los cuatro (doce) 111 = Σ percepciones íntegras del 190, por clave
- [ ] Σ retenciones de los 111 = Σ retenciones del 190
- [ ] Nº de perceptores coherente con el TC2 y con el libro de nóminas
- [ ] Todos los profesionales con factura del ejercicio incluidos con clave G
- [ ] Administradores con clave E, no con A
- [ ] Dietas y rentas exentas incluidas con clave L
- [ ] Pagos a proveedores en módulos con retención del 1 % incluidos con clave H
- [ ] NIF de todos los perceptores validados
- [ ] Certificados de retenciones emitidos y enviados a los perceptores

## 7. Corrección de errores

- Antes del fin del plazo: presentar declaración **sustitutiva** con el número
  identificativo de la anterior.
- Después: **complementaria** (solo añade registros) o **sustitutiva** (reemplaza la
  declaración completa). Para corregir un dato erróneo de un perceptor ya declarado, la
  vía correcta suele ser la sustitutiva.
- La presentación fuera de plazo o con datos incorrectos se sanciona por el art. 198 o
  199 LGT (por dato o conjunto de datos), no por el art. 191: no hay perjuicio económico.
