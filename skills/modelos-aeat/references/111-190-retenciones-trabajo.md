# Modelo 111 — Retenciones del trabajo y de actividades económicas

## 1. Quién y cuándo

| Concepto | Detalle |
|---|---|
| Obligados | Quien satisfaga rendimientos sujetos a retención: personas jurídicas, y personas físicas en el ejercicio de su actividad económica |
| Trimestral | 1–20 de abril, julio, octubre y **enero** |
| Mensual | Grandes empresas (INCN > 6.010.121,04 €): 1–20 del mes siguiente |
| Resumen anual | Modelo **190**, del 1 al 31 de enero |

⚠️ Si el cliente está dado de alta en la obligación (casilla del 036) debe presentar el
modelo **aunque no haya retenido nada**: presentación **negativa**. Si ya no va a retener
nunca más, hay que **darle de baja la obligación** en el 036; si no, la AEAT reclamará el
modelo cada periodo.

## 2. Estructura

| Bloque | Casillas | Contenido |
|---|---|---|
| Rendimientos del trabajo — dinerarios | 01-03 | Nº perceptores, base, retenciones |
| Rendimientos del trabajo — en especie | 04-06 | Nº perceptores, valor, ingresos a cuenta |
| Actividades económicas — dinerarias | 07-09 | Profesionales, agrícolas, módulos |
| Actividades económicas — en especie | 10-12 | |
| Premios — dinerarios | 13-15 | |
| Premios — en especie | 16-18 | |
| Ganancias por aprovechamientos forestales | 19-24 | |
| Contraprestaciones por cesión de derechos de imagen | 25-27 | |
| **Total** | 28 | Suma de retenciones e ingresos a cuenta |
| A deducir (complementaria) | 29 | |
| **Resultado** | 30 | |

## 3. Tipos aplicables

| Concepto | Tipo |
|---|---|
| Trabajo por cuenta ajena | Procedimiento general del art. 80 ss. RIRPF (tipo individual por trabajador) |
| Administradores y consejeros | **35 %**; **19 %** si el INCN de la entidad < 100.000 € |
| Actividades profesionales | **15 %** |
| Profesionales en inicio de actividad (año de inicio + 2 siguientes) | **7 %**, previa comunicación escrita del perceptor |
| Cursos, conferencias, seminarios, obras literarias | **15 %** |
| Actividades agrícolas y ganaderas | **2 %** (1 % engorde de porcino y avicultura) |
| Actividades forestales | **2 %** |
| Actividades empresariales en módulos (art. 95.6 RIRPF) | **1 %** |
| Premios de juegos, concursos y rifas | **19 %** |
| Cesión de derechos de imagen | **24 %** |

Verifica los tipos del ejercicio: `python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar retenciones`.

## 4. Errores frecuentes

1. **Aplazar el 111.** Las retenciones son deuda **inaplazable** (art. 65.2.b LGT): la
   solicitud se inadmite y la deuda pasa a ejecutiva desde el día siguiente al fin del
   plazo voluntario, con recargo del 5-20 %. Es el error más caro del modelo.
2. Retener el 15 % a un profesional que está en su periodo de inicio y podía aplicar el
   7 % (o al revés, aplicar el 7 % sin la comunicación escrita del perceptor).
3. Consignar al administrador en el bloque de trabajo sin diferenciar la clave: en el 190
   va con **clave E**, y el descuadre aparece en enero.
4. No incluir las **dietas exentas**: no llevan retención, pero sí van al 190 con
   **clave L**. Omitirlas es la causa habitual del requerimiento del 190.
5. Olvidar la **regularización del tipo de retención** cuando cambian las circunstancias
   del trabajador (art. 87 RIRPF).
6. Retenciones en especie: hay que consignar el **ingreso a cuenta**, no la retención.
7. Facturas de profesionales sin retención por descuido del proveedor: **la obligación de
   retener es del pagador**, con independencia de lo que ponga la factura.

## 5. Cuadre

- [ ] Σ bases de los cuatro (doce) modelos 111 = base del 190, desglosada por clave
- [ ] Σ retenciones = retenciones del 190
- [ ] Retenciones del 111 ↔ cuentas 4751 y 4750 de la contabilidad
- [ ] Gasto de personal y de servicios profesionales ↔ bases declaradas
- [ ] Certificados de retenciones emitidos antes del inicio de la campaña de Renta
      (art. 108.3 RIRPF)

## 6. Presentación

Electrónica con certificado. Resultado a ingresar mediante NRC o domiciliación (hasta el
día 15). Presentación **negativa** si no hubo retenciones en el periodo pero subsiste la
obligación censal.

## 7. Relación con el 190

El 190 es el detalle por perceptor de lo declarado agregado en los 111. Para generar el
fichero del 190 con este plugin, ver `scripts/generar_informativa.py`.


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
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/generar_informativa.py \
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
