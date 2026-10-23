# B20 – ¿Recorta SQX Ret/DD y el factor de beneficio? (plan escrito ANTES de calcular)

Fecha: 2026-10-23 · Autor: Claude · Asunto B20 de `PENDIENTES.md`; puerta de la fase 0 de la 0004 (§4).

## Pregunta

En B17, las mejores estrategias de varios brazos tenían **Ret/DD = 10,0** y **factor de beneficio = 5,0 exactos**.
¿Es un tope de SQX? Si lo es, ordenar o seleccionar por esas columnas no distingue entre las mejores (el curso elige
"las de mayor Ret/DD", fase 1 §5), y el análisis tiene que recalcularlas.

## Fuentes

- **Documentación instalada de SQX** (`C:\StrategyQuantX145\docs`, 2026-10-23): `overview/stats-metrics.md` define
  `ReturnDDRatio` ("Return / drawdown ratio") y `ProfitFactor` ("gross profit to gross loss") **sin mencionar ningún
  tope**; la búsqueda de "cap", "clamp", "limited to" o "maximum value" no encuentra nada sobre estas métricas.
- **Datos ya existentes, sin lanzar SQX:** `lab_h0\b21\Results_B21.csv`, la exportación de las 7.003 estrategias
  (registro n.º 226), con las columnas de las que salen las dos métricas, en IS y en OOS (14.006 casos).

## Método (`h0/configs/b20_recorte_metricas.py`, 3 tests con dos controles negativos)

Se recalcula cada métrica con las columnas que la definen: Ret/DD = beneficio neto / drawdown; PF = |ganancia media /
pérdida media| × (Win/Loss ratio). Se excluye la franja ±5 % alrededor del supuesto tope.

- **Control (que la fórmula sea la de SQX):** donde lo recalculado está claramente por **debajo** del tope, el valor de
  SQX coincide (diferencia ≤ 2 % o ≤ 0,02) en al menos el **99 %** de los casos. Si no, la fórmula no es la de SQX y la
  prueba **no vale** (INCONCLUSO), sin buscar otra fórmula mirando los datos.
- **Prueba:** donde lo recalculado está claramente por **encima** del tope.

## Decisión (fijada ahora)

- **SÍ recorta:** el control pasa, **todos** los casos por encima valen exactamente el tope, y el máximo de la columna
  de SQX es el tope.
- **NO recorta:** el control pasa y **ninguno** de los casos por encima vale el tope.
- **INCONCLUSO:** cualquier otra cosa (incluida una mezcla, o que no haya casos por encima).

**Consecuencias si recorta:** en la fase 1, C ordena con la columna de SQX tal cual (reproducción fiel, empates
resueltos por una regla fija) y L con las métricas recalculadas (borrador de la fase 1, §5). Los filtros de B17
(Ret/DD ≥ 2, PF ≥ 1,2 y ≥ 1,1) están **por debajo** de los topes, así que un recorte no cambia qué estrategias pasaron:
la conclusión D1 de B17 no se ve afectada. Se cuenta además cuántas estrategias empatan en el tope.

## Lo que no demuestra

El comportamiento con otros motores, otros periodos o la build final de SQX; cómo se calculan otras métricas.
