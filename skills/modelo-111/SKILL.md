---
name: modelo-111
description: Modelo 111, autoliquidación de retenciones e ingresos a cuenta del IRPF sobre rendimientos del trabajo, actividades económicas, premios y determinadas imputaciones. Casillas, claves de percepción, tipos aplicables, presentación negativa, plazos, inaplazabilidad de la deuda y cuadre con el resumen anual 190. Úsala para preparar o revisar el 111 de cualquier periodo.
---

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

Verifica los tipos del ejercicio en `config/parametros-fiscales.md`.

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
fichero del 190 con este plugin, ver la skill `modelo-190` y
`scripts/generar_informativa.py`.
