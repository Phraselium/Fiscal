---
name: control-de-cartera
description: Control de cartera sobre el Control.xlsx: qué está pendiente, qué vence, qué hay que revisar y ficha de cada cliente. Úsala siempre que la pregunta sea sobre varios clientes o sobre «qué falta».
---

# Control de cartera

El **Control.xlsx** es el sistema operativo del despacho: una matriz de ~85 clientes ×
~24 columnas de modelo, con el estado de cada presentación. Es la fuente de verdad.

## Regla obligatoria de eficiencia

**Nunca leas el Excel entero para responder.** Son más de 1.100 celdas: volcarlas al
contexto cuesta ~15.000 tokens y hace el trabajo lento y propenso a error. Ejecuta el
subcomando que corresponda y trabaja sobre su salida, que ya viene filtrada.

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/control.py --fichero <ruta> <subcomando>
```

| Pregunta del usuario | Subcomando |
|---|---|
| «¿cómo vamos?», «resumen del trimestre» | `resumen` |
| «¿qué está pendiente de revisar?» | `cola --estado Revisar` |
| «¿a quién le falta el 303?» | `cola --estado Pendiente --modelo 303` |
| «¿cómo está EJEMPLO CLIENTE SL?» | `cliente "EJEMPLO CLIENTE SL"` |
| «¿cómo va el 347 en la cartera?» | `modelo 347` |
| «¿qué vence pronto?» | `vencimientos --dias 30` |
| «¿qué alquileres faltan por facturar?» | `alquileres` |
| «revisa el control» | `huecos` |
| «marca el 303 de X como presentado» | `marcar --cliente X --modelo 303 --estado Presentado` |
| «pásame la matriz a CSV» | `exportar --formato csv` |

Añade `--json` en `cola` cuando vayas a procesar el resultado; `--limite 0` para no truncar.

## Estados y su significado

Flujo de trabajo declarado en el propio control:

```
Sin dato → Documentación → Pendiente → Revisar → Presentado → Liquidación pendiente
```

| Estado | Significado |
|---|---|
| **Sin dato** | Sin información, por confirmar |
| **Documentación** | Esperando documentación del cliente |
| **Pendiente** | En preparación, aún por presentar |
| **Revisar** | Preparado; **requiere revisión antes de presentar** |
| **Presentado** | Presentado ante la AEAT |
| **Liquidación pendiente** | Presentado; pendiente de pago |
| **No aplica** | El modelo no corresponde a este cliente |
| **Baja** | Cliente u obligación de baja |

**Revisar es la cola crítica**: es trabajo terminado que no se ha presentado porque falta
un par de ojos. Es donde se pierden los plazos. Sácala la primera en cualquier resumen.

## Marcas entre corchetes

Los estados llevan marcas: `Presentado [T, env]`. Las que aparecen en el control:

| Marca | Lectura |
|---|---|
| `env` | Enviado (al cliente o por correo) |
| `neg` | Declaración negativa |
| `0` | A cero |
| `s.act` | Sin actividad |
| `aplz` | Aplazamiento solicitado o concedido |
| `+` / `−` | Resultado a ingresar / a devolver o compensar |
| `compras` / `ventas` | Clave de la operación en el 347 |
| `cli` | Gestionado por el cliente |
| `SII` | Cliente en Suministro Inmediato de Información |
| `T`, `V`, `O` | **Pendiente de confirmar con el despacho.** No las interpretes ni las escribas sin preguntar |

Al marcar una celda, **conserva las marcas existentes** salvo que el usuario pida
cambiarlas: `marcar ... --marca env --marca T`.

## Columnas de ejercicios anteriores

La matriz tiene `347 (2)`, `390 (3)`, `190 (3)`… Son **ejercicios anteriores pendientes**,
no duplicados. Un cliente con `390 (3) Pendiente` arrastra un resumen anual sin presentar
de hace varios años: eso es riesgo de sanción del art. 198 LGT acumulándose, y debe
salir en cualquier informe de situación. No los ignores al hacer recuento.

## Auditoría del control (`huecos`)

Detecta incoherencias internas, no errores fiscales:
- Clientes con `303` en flujo pero `390` marcado «No aplica» (o el par 111/190, 115/180,
  123/193): o falta la exoneración documentada, o el control está mal.
- Sociedades con `200` en flujo y `202` en «No aplica»: revisar si procede el pago
  fraccionado del art. 40.2 LIS.
- Celdas en «Sin dato» que llevan periodos sin resolverse.

Pásalo al empezar cada trimestre. Lo que salga hay que resolverlo con el responsable del
cliente, no corrigiéndolo a ciegas.

## Escribir en el control

`marcar` reescribe el fichero con openpyxl. Antes de usarlo:
1. Ejecuta siempre primero con `--simular` y enseña el cambio al usuario.
2. Usa `--salida` para escribir en una copia si el original está en una carpeta compartida.
3. openpyxl conserva el formato condicional y las fórmulas, pero **no** los complementos
   ni los objetos incrustados (el fichero tiene una webextension). Si el control tiene
   paneles o complementos, trabaja sobre copia y avisa.
4. No hagas cambios masivos sin confirmación explícita, cliente a cliente o con una lista
   revisada por el usuario.

## Qué NO hace este control

No contiene importes, ni cuotas, ni datos censales rellenos (la hoja `Clientes` está
vacía en la plantilla). Para saber si un cliente debe presentar un modelo hay que mirar
su **036/037**, no la matriz. La matriz dice qué se ha hecho, no qué hay que hacer.

Si el usuario pregunta «¿este cliente tiene que presentar el 349?», la respuesta no está
en el control: está en su situación censal y en sus operaciones. Dilo así.
