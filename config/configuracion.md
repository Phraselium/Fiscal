# Configuración local del despacho

> Este fichero es la **configuración del plugin**. Complétalo con los datos reales antes
> de trabajar. Todas las skills y comandos lo leen para firmar escritos, generar ficheros
> y calcular plazos internos. No se distribuye con datos: los placeholders
> `PENDIENTE_COMPLETAR` deben rellenarse en cada instalación.

## 1. Datos del presentador (obligatorios para generar ficheros)

| Campo | Valor |
|---|---|
| Denominación social / nombre | `PENDIENTE_COMPLETAR` |
| NIF del presentador | `PENDIENTE_COMPLETAR` |
| Persona de contacto | `PENDIENTE_COMPLETAR` |
| Teléfono de contacto | `PENDIENTE_COMPLETAR` |
| Email | `PENDIENTE_COMPLETAR` |
| Domicilio | `PENDIENTE_COMPLETAR` |
| Certificado digital de representación | `PENDIENTE_COMPLETAR` |
| Colaborador social (convenio AEAT) | Sí / No — `PENDIENTE_COMPLETAR` |

> El NIF y el nombre del presentador se escriben en el **registro de tipo 1** de todas
> las declaraciones informativas y en la cabecera del fichero Intrastat.

## 2. Ámbito territorial

| Campo | Valor |
|---|---|
| Territorio común (AEAT) | Sí |
| CCAA principal para tributos cedidos | `PENDIENTE_COMPLETAR` |
| Clientes en territorio foral (Álava, Bizkaia, Gipuzkoa, Navarra) | `PENDIENTE_COMPLETAR` |
| Clientes en Canarias (IGIC) / Ceuta y Melilla (IPSI) | `PENDIENTE_COMPLETAR` |

En territorio foral **no** se aplica la normativa estatal: la skill debe avisar y detenerse.

## 3. Criterios internos

1. **Prudencia interpretativa**: ante dos lecturas razonables, la posición conservadora es
   la recomendación; la alternativa se expone con el riesgo cuantificado.
2. **Trazabilidad**: toda conclusión relevante cita artículo y, si existe, doctrina (DGT)
   o jurisprudencia (TEAC, TS).
3. **Revisión humana obligatoria**: todo lo que genera el plugin es **borrador**.
4. **Colchón de plazo**: 5 días hábiles antes del vencimiento oficial.
5. **Sin justificante no hay gasto**: no se computa gasto ni deducción sin factura
   completa (art. 6 RD 1619/2012) o justificante equivalente admitido.
6. **Ningún fichero se presenta automáticamente**: el plugin genera el fichero; la
   presentación es un acto humano con certificado.

## 4. Estructura de expedientes

```
clientes/<NIF>-<nombre-corto>/
  ├── 00-ficha.md                 # datos censales, obligaciones, calendario
  ├── 01-censal/                  # 036/037, IAE, apoderamientos
  ├── 02-periodicas/<ejercicio>/  # 303, 111, 115, 123, 202, 130/131
  ├── 03-anuales/<ejercicio>/     # 390, 190, 180, 100, 200, 347, 349, 720/721
  ├── 04-contabilidad/<ejercicio>/
  ├── 05-requerimientos/
  ├── 06-intrastat/<ejercicio>/
  └── 07-correspondencia/
salidas/                          # ficheros generados listos para importar
```

## 5. Aviso legal estándar

> El presente documento constituye una opinión profesional basada en la normativa vigente
> en la fecha de emisión y en la información facilitada por el cliente. No vincula a la
> Administración tributaria. Cualquier modificación normativa, doctrinal o jurisprudencial
> posterior, o cualquier dato no comunicado, puede alterar las conclusiones expuestas.

## 6. Cartera (opcional)

Si mantienes aquí la lista de clientes, las skills la usarán para el calendario y los
avisos. Formato sugerido:

```
| NIF | Nombre | Régimen IRPF/IS | Régimen IVA | Periodicidad | Modelos | CCAA | Intrastat |
|-----|--------|-----------------|-------------|--------------|---------|------|-----------|
```
