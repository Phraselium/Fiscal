---
name: modelo-036-037
description: Modelos 036 y 037, declaración censal de alta, modificación y baja — cuándo usar cada uno, páginas y casillas clave, alta de actividad, epígrafes IAE, opciones y renuncias de regímenes de IVA e IRPF, alta en el ROI, obligaciones de retener, cambio de domicilio fiscal, baja de actividad y errores censales que generan requerimientos. Úsala para dar de alta, modificar o dar de baja a un cliente en Hacienda.
---

# Modelos 036 y 037 — Declaración censal

## 1. Cuál usar

**037 (simplificado)** solo si se cumplen **todas** estas condiciones: persona física
residente, con NIF definitivo, no gran empresa, sin regímenes especiales de IVA salvo
simplificado / agricultura / recargo de equivalencia / criterio de caja, sin operaciones
intracomunitarias, sin actuar por representante y sin ser sujeto a regímenes especiales
de IRPF distintos de los ordinarios.

**En caso de duda, usa el 036.** Nunca falla y admite todo.

## 2. Plazos

| Situación | Plazo |
|---|---|
| Alta previa al inicio de actividad | **Antes** del inicio |
| Modificación de datos | 1 mes desde el hecho que la motiva |
| Baja por cese | 1 mes desde el cese |
| Baja por fallecimiento | 6 meses desde el fallecimiento (herederos) |
| Opción o renuncia a regímenes con efectos en el año siguiente | **Diciembre** del año anterior |
| Opción por la modalidad del art. 40.3 del pago fraccionado del IS | **Febrero** |
| Alta en ROI | Antes de la primera operación intracomunitaria (la AEAT tarda hasta 3 meses) |

## 3. Contenido por páginas

| Página | Contenido |
|---|---|
| **1** | Causas de presentación: alta, modificación, baja. NIF e identificación |
| **2** | Representantes, domicilio fiscal, domicilio a efectos de notificaciones, sucesiones y transformaciones |
| **3** | Actividades económicas, **epígrafes IAE**, locales y su superficie |
| **4** | **IVA**: regímenes aplicables, ROI (casillas 582 alta / 584 baja), prorrata, criterio de caja, deducciones anteriores al inicio (casilla 504), ventanilla única |
| **5** | **IRPF / IS**: estimación directa u objetiva, pagos fraccionados, obligación de **retener** (casillas 700 y siguientes: 111, 115, 123, 124, 126, 128, 216) |
| **6** | Relación de socios y partícipes, grandes empresas, regímenes especiales, grupos |

## 4. Alta de una actividad — secuencia

```
1. Determinar el epígrafe o epígrafes del IAE
2. Elegir régimen de IRPF: directa normal / directa simplificada / objetiva
3. Elegir régimen de IVA: general / simplificado / recargo de equivalencia /
   REAGP / RECC / exenta
4. Marcar obligaciones de retener que se van a asumir (111, 115...)
5. Alta en ROI si va a operar con la UE
6. Marcar la deducción de cuotas soportadas antes del inicio (casilla 504) si procede
7. Presentar ANTES del inicio, y solo después dar de alta en RETA
```

**Casilla 504**: permite deducir el IVA soportado antes de iniciar la entrega de bienes o
prestación de servicios (art. 111 LIVA). Se olvida sistemáticamente en altas con
inversión inicial fuerte (obras, maquinaria, local). Márcala.

## 5. Errores censales que generan requerimientos

| Error | Consecuencia |
|---|---|
| Alta en la obligación del 111 y no presentar el modelo | Requerimiento cada trimestre. Solución: presentar negativa **o** dar de baja la obligación |
| Cese de actividad sin baja censal | Se sigue exigiendo 303, 111 y 130 indefinidamente |
| No comunicar el cambio de **domicilio fiscal** | Las notificaciones se hacen válidamente en el antiguo; se pierden plazos |
| Facturar sin IVA a la UE sin estar en el ROI | La operación no está exenta: se liquida el 21 % con sanción |
| No renunciar a módulos en diciembre cuando ya no se cumplen requisitos | Se tributa en un régimen que no corresponde |
| Epígrafe IAE que no se corresponde con la actividad real | Problemas en comprobación y en la retención del 1 % del art. 95.6 RIRPF |
| Alta de actividad después de haber empezado a facturar | Infracción del art. 198 LGT |

## 6. Cambios de régimen y su plazo

| Cambio | Cuándo |
|---|---|
| Renuncia a estimación objetiva (módulos) | Diciembre del año anterior, o de forma **tácita** presentando el 130 del 1T en plazo |
| Revocación de la renuncia a módulos | Diciembre, tras 3 años de vinculación |
| Renuncia al régimen simplificado de IVA | Va unida a la renuncia a módulos en IRPF |
| Opción por el RECC (criterio de caja) | Diciembre del año anterior |
| Opción por la prorrata especial | En la **última autoliquidación** del ejercicio (art. 28.1 RIVA) |
| Alta en REDEME (devolución mensual) | Noviembre del año anterior |
| Opción por la modalidad 40.3 del pago fraccionado del IS | Febrero |

## 7. Baja de actividad

1. Modelo 036/037 marcando la baja y la fecha de cese.
2. Baja en el **RETA** (hasta 3 días naturales después del cese).
3. Presentar las **últimas autoliquidaciones** del periodo en curso.
4. Modelo 390 y resúmenes anuales del ejercicio de cese.
5. Regularizar el IVA de los bienes de inversión si procede.
6. Baja de la obligación de retener y de los epígrafes IAE.
7. Conservar la documentación durante los plazos de prescripción (4 años; 10 si hay BIN).

Una sociedad no se «da de baja» con el 036: debe **disolverse y liquidarse** ante notario
e inscribirse en el Registro Mercantil. Hasta entonces sigue obligada a presentar el 200.

## 8. Apoderamientos y notificaciones

- Sin **apoderamiento** vigente en el Registro de Apoderamientos de la AEAT, el despacho
  no puede presentar ni recibir notificaciones del cliente.
- Trámites habituales: `GENERALDATPRO` (declaraciones), `GENERALLEY58` (procedimientos),
  `RECURSOSREC` (recursos), y los específicos por modelo.
- Personas jurídicas: notificación electrónica obligatoria (**DEHú**). Se entiende
  rechazada a los **10 días naturales** sin acceder.
- **Días de cortesía**: hasta 30 al año, solicitados con 7 días de antelación.
- Revisa cada trimestre que los apoderamientos de la cartera siguen vigentes.
