---
name: gestion-de-despacho
description: Gestión interna del despacho de asesoría fiscal — alta y onboarding de clientes, hoja de encargo y alcance del servicio, apoderamientos y certificados, control de documentación pendiente, comunicación con el cliente, obligaciones del despacho como sujeto obligado de prevención del blanqueo (Ley 10/2010), protección de datos, conservación de expedientes y responsabilidad profesional. Úsala para dar de alta un cliente, definir el alcance de un encargo o revisar los controles internos del despacho.
---

# Gestión del despacho

## 1. Alta de un cliente — checklist completo

### Documentación a recabar
- [ ] DNI/NIE del titular y de los administradores; escritura de constitución y estatutos
- [ ] Escritura de nombramiento del administrador vigente y poderes
- [ ] Titularidad real (Ley 10/2010) y estructura de participación
- [ ] Modelo 036/037 vigente y últimas declaraciones presentadas (al menos 4 ejercicios)
- [ ] Certificado de estar al corriente con la AEAT y con la TGSS
- [ ] Últimas cuentas anuales depositadas y balance de sumas y saldos actual
- [ ] Contratos relevantes: arrendamientos, préstamos, laborales, con vinculadas
- [ ] Datos bancarios y titularidad de las cuentas
- [ ] Certificado digital o apoderamiento para actuar ante la AEAT

### Alta administrativa
- [ ] **Apoderamiento** en el Registro de Apoderamientos de la AEAT (trámites
      `GENERALDATPRO`, `GENERALLEY58`, `RECURSOSREC` y los específicos por modelo)
- [ ] Configuración de **días de cortesía** (hasta 30 al año, con 7 días de antelación)
- [ ] Alta en el software del despacho y en el calendario de obligaciones
- [ ] Carpeta de expediente según la estructura de `config/configuracion.md`
- [ ] Hoja de encargo firmada
- [ ] Ficha de PBC/FT y de protección de datos

### Diagnóstico inicial (el que evita heredar problemas ajenos)
- [ ] Deudas pendientes con la AEAT y la TGSS; aplazamientos en curso
- [ ] Procedimientos abiertos: requerimientos, comprobaciones, recursos
- [ ] Ejercicios no prescritos y su situación
- [ ] BIN y deducciones pendientes de aplicar, con su documentación de origen
- [ ] Coherencia entre las últimas declaraciones (303 ↔ 390 ↔ 347 ↔ 200)
- [ ] Contingencias detectadas → **comunicarlas por escrito al cliente antes de asumir
      el encargo**, dejando claro qué se hereda y qué no

## 2. Hoja de encargo

Define por escrito, como mínimo:

| Apartado | Contenido |
|---|---|
| Partes | Identificación completa |
| **Alcance** | Qué modelos y obligaciones se asumen, y **cuáles no** (laboral, mercantil, contable, tributos locales, autonómicos, extranjería) |
| Periodo | Ejercicios cubiertos; expresamente, si se revisan o no ejercicios anteriores |
| Obligaciones del cliente | Entregar documentación completa y veraz en los plazos fijados |
| Plazos internos | Fecha límite de entrega de documentación por periodo |
| Honorarios | Importe, periodicidad, trabajos excluidos y su tarifa |
| Responsabilidad | Límites; el asesor responde de su trabajo, no de datos no facilitados |
| Confidencialidad y protección de datos | Encargado del tratamiento (art. 28 RGPD) |
| PBC/FT | Obligación de identificación y de colaboración |
| Terminación | Preaviso, entrega de documentación y devolución de expedientes |

El **alcance** es la cláusula que evita el 90 % de los conflictos. Sé explícito con lo
excluido: nadie discute lo que está escrito.

## 3. Control de documentación pendiente

Regla operativa: **sin documentación no hay declaración**, pero el silencio del cliente no
exime al despacho de avisar. Deja rastro:

```
Semana −3 del trimestre: solicitud de documentación por escrito
Semana −2: primer recordatorio
Semana −1: SEGUNDO RECORDATORIO con advertencia expresa de las consecuencias
           (recargo del art. 27 LGT, o presentación con los datos disponibles)
Antes del vencimiento: comunicación de la decisión tomada y su justificación
```

Si el cliente no aporta y hay que presentar, documenta por escrito qué se presentó, con
qué datos y con qué reservas. Esa comunicación es tu defensa.

## 4. Prevención del blanqueo (Ley 10/2010)

Los asesores fiscales son **sujetos obligados** (art. 2.1.m). Obligaciones mínimas:

- **Identificación formal** del cliente y del **titular real** (participación > 25 %),
  con documento fehaciente y conservación de la copia.
- **Conocimiento de la actividad** y del propósito de la relación de negocio.
- **Seguimiento continuo** de la relación.
- **Medidas reforzadas** con personas con responsabilidad pública (PRP), clientes no
  presenciales, jurisdicciones de riesgo y estructuras societarias complejas.
- **Manual de prevención**, representante ante el SEPBLAC, formación anual del personal y
  examen externo cuando proceda.
- **Abstención y comunicación al SEPBLAC** ante operaciones sospechosas — sin informar al
  cliente (prohibición de revelación, art. 24).
- Conservación de la documentación: **10 años**.

Señales que exigen análisis: pagos en efectivo relevantes, facturación sin sustrato
económico, sociedades sin actividad con movimientos financieros, cambios societarios
injustificados, resistencia a identificar al titular real, operaciones con jurisdicciones
no cooperativas.

⚠️ Si detectas indicios, **no lo resuelvas como un problema técnico**: escálalo al
responsable de cumplimiento. No lo documentes en el expediente ordinario del cliente.

## 5. Protección de datos

- El despacho es **encargado del tratamiento** de los datos de los empleados y clientes de
  su cliente: hace falta contrato del art. 28 RGPD.
- Y **responsable** respecto de los datos de sus propios clientes.
- Registro de actividades de tratamiento, medidas de seguridad, y notificación de brechas
  en **72 horas** a la AEPD.
- Nunca envíes datos fiscales por canales no cifrados. Los certificados digitales de los
  clientes no se comparten por correo electrónico.

## 6. Conservación de expedientes

| Documentación | Plazo |
|---|---|
| Contable y mercantil (Código de Comercio, art. 30) | **6 años** |
| Fiscal, con carácter general | 4 años de prescripción, contados desde el fin del plazo de presentación |
| Con BIN o deducciones pendientes | **10 años** (art. 66 bis LGT), y en la práctica mientras queden saldos por aplicar |
| Bienes de inversión de IVA | 4 años tras el fin del periodo de regularización (9 en inmuebles) |
| PBC/FT | 10 años |
| Facturas y libros registro | Mientras no prescriba el derecho de la Administración |

En la práctica: **conserva 10 años** salvo que exista una razón para más.

## 7. Comunicación con el cliente

- Todo lo relevante, **por escrito**. Una llamada se olvida; un correo se archiva.
- Cada declaración presentada: enviar justificante con **CSV**, importe y fecha de cargo.
- Cada notificación recibida: comunicarla el mismo día, con el plazo de respuesta
  calculado y la fecha límite interna.
- Advertencias de riesgo: siempre por escrito, con la alternativa recomendada y la
  cuantificación de la contingencia.
- Al terminar la relación: entrega ordenada de la documentación y confirmación de la
  revocación de los apoderamientos.

## 8. Responsabilidad profesional

- El asesor responde por **culpa o negligencia** en el desempeño de su encargo, no del
  resultado de una comprobación tributaria.
- La **responsabilidad tributaria** frente a la AEAT es del obligado; el asesor puede
  incurrir en responsabilidad solidaria si colabora activamente en la infracción
  (art. 42.1.a LGT). Es una razón práctica más para no aceptar instrucciones de simular
  operaciones.
- Mantén un seguro de responsabilidad civil profesional adecuado al volumen de la cartera.
- Documenta las advertencias desatendidas: si el cliente decide en contra del criterio del
  despacho, que conste por escrito su decisión.
