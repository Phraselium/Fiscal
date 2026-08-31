# Retenciones y censos

## Quien retiene

Personas juridicas, y personas fisicas **en el ejercicio de su actividad economica**. Un
particular que no ejerce actividad no retiene — salvo que sea arrendatario empresario de
un local, donde retiene el, no el arrendador.

## Tipos

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/parametros.py buscar retenciones
```

Los mas usados: profesionales **15 %** (7 % en el ano de inicio y los 2 siguientes, previa
comunicacion escrita), administradores **35 %** (19 % si el INCN de la entidad < 100.000 €),
alquiler de local **19 %**, capital mobiliario **19 %**, modulos del art. 95.6 RIRPF **1 %**.
El trabajo por cuenta ajena no tiene tipo fijo: procedimiento del art. 80 ss. RIRPF.

## Las tres trampas

1. **El 111 es inaplazable** (art. 65.2.b LGT). Solicitarlo lo inadmite y la deuda entra en
   ejecutiva con recargo del 5-20 %.
2. **No retener el alquiler de local** es la regularizacion mas comun: la AEAT cruza el
   gasto contabilizado con la ausencia de 115. Las excepciones del art. 75.3.g exigen
   prueba — el certificado del grupo 861 caduca al ano.
3. **Dietas y rentas exentas** no llevan retencion pero **si van al 190 con clave L**.
   Omitirlas genera propuestas de liquidacion a los trabajadores.

## Censos: lo que provoca requerimientos

| Error | Consecuencia |
|---|---|
| Alta en la obligacion del 111 y no presentar | Requerimiento cada trimestre. Presenta negativa **o** da de baja la obligacion |
| Cese sin baja censal | Se siguen exigiendo 303, 111 y 130 indefinidamente |
| Facturar sin IVA a la UE sin ROI | La operacion no esta exenta: 21 % + sancion |
| No comunicar el cambio de domicilio fiscal | Notificaciones validas en el antiguo; se pierden plazos |
| No renunciar a modulos en diciembre | Se tributa en un regimen que no corresponde |

**Regla practica**: antes de cada trimestre, contrasta la matriz del control con el 036 de
cada cliente. Las celdas «No aplica» que deberian estar en flujo (y al reves) salen con
`python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py huecos`.

## Modelos

`111`/`190` · `115`/`180` · `123`/`193` · `216`/`296` · `036`/`037` · `840`/`848`.
Cada uno tiene su skill.

---

# Retenciones y obligaciones censales

## 1. Retenciones — quién, qué y cuánto

**Obligados a retener (art. 76 RIRPF, art. 60 RIS)**: personas jurídicas, contribuyentes
de actividades económicas por los rendimientos que satisfagan en el ejercicio de su
actividad, y personas físicas/entidades no residentes con EP.

⚠️ Un particular que **no** ejerce actividad económica **no** retiene, salvo en el
arrendamiento de local a un empresario (ahí retiene el arrendatario empresario, no el
particular arrendador).

### Tabla operativa

| Renta | Modelo | Tipo | Resumen anual |
|---|---|---|---|
| Trabajo por cuenta ajena | 111 | Procedimiento general del art. 80 ss. RIRPF | 190 |
| Administradores / consejeros | 111 | 35 %; **19 %** si el INCN de la entidad < 100.000 € | 190 |
| Profesionales | 111 | 15 % | 190 |
| Profesionales — inicio de actividad (año de inicio + 2 siguientes) | 111 | 7 % (requiere comunicación escrita del perceptor al pagador) | 190 |
| Cursos, conferencias, seminarios, elaboración de obras literarias | 111 | 15 % | 190 |
| Actividades agrícolas y ganaderas | 111 | 2 % (1 % engorde de porcino y avicultura) | 190 |
| Actividades forestales | 111 | 2 % | 190 |
| Actividades empresariales en **estimación objetiva** del art. 95.6 RIRPF | 111 | 1 % | 190 |
| Rendimientos del trabajo en especie | 111 | Ingreso a cuenta | 190 |
| Arrendamiento de inmuebles **urbanos** | 115 | 19 % | 180 |
| Capital mobiliario: dividendos, intereses, seguros | 123 | 19 % | 193 |
| Propiedad intelectual, industrial, arrendamiento de bienes muebles y negocios | 123 | 19 % | 193 |
| Rentas de no residentes sin EP | 216 | 19 % (residentes UE/EEE con intercambio) / 24 % resto | 296 |
| Transmisión de inmuebles por no residente | 211 | 3 % del precio (retención del adquirente) | — |

### Excepciones a la retención en el modelo 115 (art. 75.3.g RIRPF)
No se retiene si:
- El arrendamiento es de **vivienda** por una empresa a sus empleados.
- Las rentas satisfechas al mismo arrendador no superan **900 €/año**.
- El arrendador está obligado a tributar por alguno de los epígrafes del **grupo 861**
  del IAE con cuota no nula, y lo acredita con certificado (modelo del anexo de la
  Orden que aprueba el 115).
- Arrendamientos financieros (leasing).

### Cálculo de la retención del trabajo
Procedimiento general (arts. 80-89 RIRPF): retribuciones íntegras anuales previsibles →
minoraciones (SS, reducciones, mínimo personal y familiar) → aplicación de la escala →
tipo de retención = cuota / retribuciones, con 2 decimales.

- **Límite excluyente**: no se retiene por debajo de los importes de la tabla del
  art. 81 RIRPF (varían según situación familiar y nº de hijos). Verifícalos.
- **Regularización obligatoria** cuando cambian las circunstancias (art. 87 RIRPF).
- Tipos mínimos: 15 % para contratos de duración inferior al año; 18 % para relaciones
  laborales especiales de carácter dependiente (verificar redacción vigente).
- El trabajador comunica su situación con el **modelo 145**; el pagador debe conservarlo.
  Si el trabajador no comunica, se aplican los datos que consten y él responde.

## 2. Plazos

| Periodicidad | Plazo |
|---|---|
| Trimestral | 1–20 de abril, julio, octubre y **enero** |
| Mensual (grandes empresas, INCN > 6.010.121,04 €) | 1–20 del mes siguiente |
| Resúmenes anuales 190, 180, 193, 296 | 1–31 de **enero** |

## 3. Cuadre de resúmenes anuales — checklist

- [ ] Σ bases de los cuatro 111 = base del 190, por clave de percepción
- [ ] Σ retenciones de los cuatro 111 = retenciones del 190
- [ ] Σ 115 = 180; NIF de arrendadores y **referencias catastrales** completas
- [ ] Σ 123 = 193
- [ ] Claves y subclaves correctas (A trabajo, B pensiones, G actividades profesionales,
      H actividades empresariales/agrícolas, I premios, L rentas exentas y dietas)
- [ ] **Clave L** utilizada para dietas exentas y rentas exentas: es la casilla que más
      requerimientos genera si se omite
- [ ] Certificados de retenciones emitidos a los perceptores antes del inicio de la
      campaña de Renta (art. 108.3 RIRPF)
- [ ] Coherencia con el gasto de personal y de servicios exteriores en la contabilidad

## 4. Obligaciones censales — modelos 036 / 037

**037 (simplificado)**: solo personas físicas residentes, sin NIF provisional, no
grandes empresas, no incluidas en regímenes especiales de IVA salvo simplificado,
agricultura, recargo de equivalencia o RECC, y sin obligaciones intracomunitarias. En
la duda, usa el **036**.

### Momentos de presentación
| Situación | Plazo |
|---|---|
| Alta previa al inicio de actividad | **Antes** del inicio |
| Modificación de datos | 1 mes desde el hecho |
| Baja | 1 mes desde el cese |
| Baja por fallecimiento | 6 meses desde el fallecimiento (por los herederos) |
| Alta en ROI (VIES) | Antes de la primera operación intracomunitaria; la AEAT dispone de 3 meses |
| Opción/renuncia a regímenes de IVA e IRPF | Diciembre anterior al año de efectos, o al inicio de la actividad |

### Casillas críticas del 036
| Bloque | Contenido |
|---|---|
| Página 1 | Causa de presentación, NIF, identificación |
| Página 2 | Representantes, domicilio fiscal y domicilio a efectos de notificaciones |
| Página 3 | Actividades económicas, epígrafes IAE, locales |
| Página 4 | **IVA**: regímenes, ROI (cas. 582/584), prorrata, RECC, deducciones previas al inicio (cas. 504) |
| Página 5 | **IRPF/IS**: estimación directa/objetiva, pagos fraccionados, retenciones que se van a practicar (cas. 700 ss.) |
| Página 6 | Relación de socios, sucesiones, grandes empresas |

### Errores censales que provocan requerimientos
- Estar dado de alta en el 111 y **no presentar** el modelo aunque no haya retenciones →
  hay que presentar **negativa** o cursar la baja de la obligación.
- Alta en ROI no solicitada antes de facturar sin IVA a un cliente de la UE.
- No comunicar el cambio de domicilio fiscal → notificaciones válidas en el antiguo.
- No renunciar a módulos en plazo (diciembre) cuando el cliente ya no cumple requisitos.
- Cese de actividad sin baja censal → obligación de seguir presentando declaraciones.

## 5. IAE — modelos 840 / 848

- Exentos del pago (art. 82 TRLHL): personas físicas siempre; sujetos pasivos del IS y
  entidades del art. 35.4 LGT con **INCN < 1.000.000 €**; los dos primeros periodos
  impositivos de inicio de actividad.
- **Aunque estén exentos**, hay obligación de darse de alta en los epígrafes vía 036/037.
- Modelo 840: alta, variación y baja de los **no exentos**. Plazo: 1 mes desde el inicio.
- Modelo 848: comunicación del INCN cuando se deja de estar exento.

## 6. Notificaciones y apoderamientos

- **DEHú / dirección electrónica habilitada única**: obligatoria para personas jurídicas
  y entidades del art. 35.4 LGT. Las notificaciones se entienden rechazadas a los
  **10 días naturales** si no se accede (art. 43.2 Ley 39/2015).
- **Días de cortesía**: hasta 30 días naturales al año, solicitados con 7 días de
  antelación, en los que la AEAT no pone notificaciones. Configúralos por cliente.
- **Apoderamiento**: Registro de Apoderamientos de la AEAT (trámites GENERALDATPRO,
  GENERALLEY58, RECURSOSREC…) o apud acta. Sin apoderamiento vigente no se puede
  presentar ni recibir notificaciones en nombre del cliente.
- Verifica trimestralmente que los apoderamientos de la cartera no han caducado.
