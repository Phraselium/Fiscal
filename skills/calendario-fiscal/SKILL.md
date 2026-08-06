---
name: calendario-fiscal
description: Calendario del contribuyente y planificación del trabajo del despacho — obligaciones mes a mes, campañas trimestrales y anuales, plazos de presentación y domiciliación, obligaciones mercantiles y registrales, y generación del calendario personalizado de un cliente según sus modelos. Úsala para saber qué toca presentar, planificar el trimestre o construir el calendario de obligaciones de un cliente.
---

# Calendario fiscal y planificación del despacho

> Los plazos son los ordinarios. **Verifica cada año el calendario del contribuyente
> publicado por la AEAT**: hay adaptaciones por festivos, y la campaña de Renta y el 347
> cambian de fechas con frecuencia. Si el último día es inhábil, se traslada al siguiente
> hábil.

## 1. El año del despacho

| Mes | Obligaciones |
|---|---|
| **Enero** | 1–20: 111, 115, 123, 216, 349 del 4T. 1–30: **303 del 4T**, 390, 130/131 del 4T. 1–31: **190, 180, 193, 184, 165, 233, 270, 345, 346** y demás resúmenes anuales. Legalización de libros del ejercicio cerrado en junio. Opciones y renuncias que debieron hacerse en diciembre |
| **Febrero** | **347**. Modelo 848 (INCN a efectos de IAE) hasta el 14. Opción por la modalidad 40.3 del pago fraccionado del IS (036). Preparación del cierre contable |
| **Marzo** | **720 y 721** (hasta el 31). Cierre contable del ejercicio anterior. Formulación de cuentas anuales (plazo: 3 meses desde el cierre) |
| **Abril** | 1–20: 111, 115, 123, 130/131, 303, 349, **202** del 1T. Inicio de la **campaña de Renta** |
| **Mayo** | Campaña de Renta. Modelo 289 (CRS) |
| **Junio** | Fin de la campaña de Renta (domiciliación cierra antes). Junta general de aprobación de cuentas (6 meses desde el cierre) |
| **Julio** | 1–20: modelos del 2T. **1–25: modelo 200** del IS. 1–31: modelo **718**. Depósito de cuentas en el Registro Mercantil (1 mes desde la aprobación) |
| **Agosto** | Mes de menor actividad. Los plazos de los procedimientos tributarios **no** se suspenden en agosto (a diferencia del ámbito judicial). Buen momento para revisiones y planificación |
| **Septiembre** | Preparación del 3T. Modelo 360 (devolución de IVA soportado en la UE, hasta el 30) |
| **Octubre** | 1–20: modelos del 3T, incluido el **202** |
| **Noviembre** | **Modelo 232** (operaciones vinculadas). Modelo 102 (2.º plazo del IRPF, habitualmente el día 5). Alta en REDEME para el año siguiente |
| **Diciembre** | 1–20: **202** (3.er pago del IS). **Cierre fiscal**: última oportunidad para ajustes del ejercicio. Opciones y renuncias de régimen con efectos en el año siguiente (036/037): módulos, RECC, prorrata especial |

## 2. Rutina trimestral

```
Semana −3   Reclamar documentación al cliente (facturas, extractos, nóminas)
Semana −2   Contabilizar, conciliar bancos, cuadrar IVA soportado y repercutido
Semana −1   Calcular modelos, cuadrar entre sí, revisión por segunda persona
Día 15      Cierre de domiciliaciones → presentar todo lo domiciliado
Día 20      Cierre del plazo → presentar lo que se paga por NRC
Día 21+     Archivar justificantes con CSV, comunicar resultados al cliente,
            revisar obligaciones censales y apoderamientos que caducan
```

## 3. Plazos de domiciliación

La domiciliación **cierra antes** que la presentación. Regla general:

| Modelo | Presentación | Domiciliación |
|---|---|---|
| Trimestrales (303, 111, 115, 123, 130, 202) | Hasta el 20 | Hasta el **15** |
| 303 y 130 del 4T | Hasta el 30 de enero | Hasta el **25 de enero** |
| 200 | Hasta el 25 de julio | Hasta el **20 de julio** |
| 100 | Fin de campaña | Unos días antes (verificar) |

Si se pasa la fecha de domiciliación, hay que pagar por **NRC**. Es la causa nº 1 de
presentaciones fuera de plazo evitables: fija el aviso interno el día 12.

## 4. Obligaciones mercantiles y registrales

| Obligación | Plazo (ejercicio natural) |
|---|---|
| Formulación de cuentas anuales | 3 meses desde el cierre → 31 de marzo |
| Legalización de libros contables | 4 meses desde el cierre → 30 de abril |
| Aprobación por la junta general | 6 meses desde el cierre → 30 de junio |
| Depósito de cuentas en el Registro Mercantil | 1 mes desde la aprobación → 30 de julio |
| Declaración de titular real | Con el depósito |

El **cierre registral** por no depositar cuentas durante un año impide inscribir casi
cualquier acto societario. Adviértelo a los clientes que se retrasan.

## 5. Construir el calendario de un cliente

```
1. Leer el modelo 036/037 vigente: qué obligaciones tiene dadas de alta
2. Determinar periodicidad (trimestral vs. mensual por INCN, REDEME o SII)
3. Añadir las anuales según sus circunstancias:
   · ¿opera con la UE?            → 349 (+ Intrastat si supera el umbral)
   · ¿tiene vinculadas?           → 232 en noviembre
   · ¿bienes en el extranjero?    → 720/721 en marzo
   · ¿patrimonio > 2 M€?          → 714 (+ 718 si > 3 M€)
   · ¿es sociedad?                → 200, 202, cuentas anuales y libros
   · ¿retiene?                    → 111/115/123 + 190/180/193
4. Restar 5 días hábiles a cada vencimiento → fecha límite interna
5. Volcar al calendario del despacho con el responsable asignado
```

Con `scripts/calcular_plazos.py` puedes calcular vencimientos concretos y el colchón
interno de 5 días hábiles.

## 6. Fechas que no son de la AEAT y se olvidan

- **Intrastat**: días 1 a 12 del mes siguiente (Departamento de Aduanas).
- **ITP y AJD** (modelo 600) y **donaciones** (651): 30 días hábiles desde el acto.
- **Sucesiones** (650): 6 meses desde el fallecimiento, prorrogables 6 más si se solicita
  en los 5 primeros meses.
- **Plusvalía municipal**: 30 días hábiles inter vivos; 6 meses mortis causa.
- **Encuestas del INE** y **formularios de inversiones exteriores** (D-1A, D-4, ETE del
  Banco de España): según umbral y requerimiento.
- **Renovación de certificados digitales** de la cartera: revísalos cada semestre.
