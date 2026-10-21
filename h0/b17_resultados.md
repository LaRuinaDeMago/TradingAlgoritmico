# B17 – Resultados del control negativo de la búsqueda (plan: `h0/b17_plan_control_negativo.md`)

Fecha: 2026-10-21 · Registros n.º 149–222 · SQX 145.3191-dev · Generación **aleatoria** del Builder, H1, datos quemados
USDCHF (decisión 0002) frente a dos series sintéticas sin ventaja. Todo es familia `H0-proceso` (regla 7): 9.053
estrategias generadas (50 de calibración + 3.000 de la v1 inválida + 3.001 de la v2 + 3.002 de la v3), ninguna candidata.

## Veredicto: **D1** (con la v3, sin costes): el embudo de filtros **no distingue** los datos reales del ruido

| Versión | Qué | Embudo F completo (real · nulos) | T1 (Fisher, real > nulos) | Validez del control | Estado |
|---|---|---|---|---|---|
| v1 (n.º 159–181) | con costes, banco de capacidad 1.000 | no se analiza | — | **inválida**: SQX desalojó por fitness y mezcló los brazos | descartada sin mirar métricas |
| v2 (n.º 182–203) | con costes (spread 2, deslizamiento 1) | 1/1.000 · 2/2.001 | p = 0,70 | **S falla** (persistencia en un nulo) | **INCONCLUSO** |
| v3 (n.º 204–222) | sin costes | 2/1.000 · **16/2.002** | **p = 0,99** | **S0 se cumple** | **D1** |

**Qué significa D1** (regla fijada antes de ver los datos):
1. En el piloto, **pasar un embudo de filtros de este tipo no cuenta como evidencia**: en datos sin ninguna ventaja lo
   pasa el **0,8 % sin costes** y el **0,1 % con costes**; en los datos reales, lo mismo o menos.
2. **B19** tiene que comparar siempre con una **distribución nula simulada con los mismos costes**, además de corregir
   sobre el universo completo de pruebas y reservar datos.
3. **El valor de SQX como generador no está demostrado** con este procedimiento (dato para A12).

**Lo que D1 NO dice:** que SQX sea inútil, ni que no haya ventaja en EURUSD. Puede que el USDCHF quemado no tenga
ventaja que encontrar, y no se probó la generación genética, ni el walk-forward, ni Monte Carlo, ni otros mercados.
Lo que sí dice: **con estas herramientas, "pasa los filtros" es compatible con el azar.**

## Datos clave

- **Persistencia dentro/fuera de muestra (Spearman del Sharpe):** v2 con costes: real 0,134 · nulos 0,055 y 0,221;
  v3 sin costes: real −0,009 · nulos −0,062 y −0,084. El real cae siempre **dentro del rango de los nulos**.
- **Por qué falló S en la v2:** el Sharpe se correlaciona con la frecuencia de operaciones (≈ −0,3 en todos los
  brazos y en los dos tramos) **solo con costes**; sin costes esa correlación desaparece (≈ 0) y la persistencia
  también. Los costes castigan igual en los dos tramos a las estrategias que operan mucho o con operaciones pequeñas.
  La hipótesis de la tendencia por tramos quedó refutada (n.º 203). **Defecto del plan:** con costes, "sin ventaja"
  no implica "sin persistencia".
- **"Espectacular por azar" (M4):** en datos sin ventaja, la mejor estrategia por Sharpe dentro de muestra llega a
  **7,8** (v3, nulo 1) y a 3,4 (v2, nulo 1); fuera de muestra, nada.
- **Mediana de operaciones dentro de muestra:** 61–72 en todos los brazos (comparables; el barajado no cambió mucho
  cuánto operan).

## Trampas de SQX descubiertas (pasan a `ESTADO_Y_CONTINUACION.md` §4 y al piloto)

1. **El banco tiene capacidad** (`<Rankings><MaxStrategies>`, 1.000 de fábrica) y, lleno, **desaloja las de peor
   fitness** (Ret/DD dentro de muestra) **sin avisar**. En la v1 borró 17 de las 40 estrategias de prueba de H0 (8 sin
   copia, n.º 181). Para guardar todo (C13): capacidad mayor que lo que se va a generar, y comprobar antes y después.
2. **Genera alguna más de las pedidas** (7 hilos): 1.001 y 1.002 en lugar de 1.000. Se usan todas.
3. **Descarta automáticamente** las estrategias "con problemas" (p. ej. sin operaciones) antes de contarlas.
4. **Hipótesis por verificar:** las métricas parecen **recortadas a un máximo** (Ret/DD = 10,0 y factor de beneficio =
   5,0 exactos en las mejores de varios brazos). Si se confirma, ordenar por esas columnas no distingue entre las
   mejores.
5. **Estado que deja en el PC:** `Builder/Results` tiene ahora ~7.000 estrategias y la configuración restaurada vuelve a
   capacidad 1.000: **la próxima generación desalojará** hasta 1.000. Antes de volver a usar el Builder, guardar el
   banco en una carpeta (o decidir qué conservar).

## Consecuencias para el proyecto

- **B19** (protocolo estadístico del piloto): la referencia es la distribución nula simulada con los mismos costes y el
  mismo procedimiento; comparar con cero no vale. El generador `b17_sintetico.py` y el análisis `b17_analizar.py`
  quedan como piezas reutilizables, con tests.
- **Piloto de la 0003:** debe incluir su propio control negativo con el mismo motor y los mismos filtros que use (no
  vale el de B17 si cambian la generación o los filtros), y fijar la capacidad del banco.
- **A12 (licencia):** a fecha de hoy, no hay evidencia de que la búsqueda de SQX con filtros típicos distinga ventaja de
  ruido. Eso no impide renovar, pero cualquier decisión de pago debería esperar a un piloto con su control negativo.
- **Coste medido:** 9.053 estrategias en ~1 h de máquina; casi todo el tiempo, arranques de `sqcli` y exportaciones del
  banco, que crecen con su tamaño (de 22 s a 74 s).
