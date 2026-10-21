# B17 – Control negativo de la búsqueda (plan escrito ANTES de ejecutar)

Fecha: 2026-10-21 · Autor: Claude · Asunto B17 de `PENDIENTES.md`, adelantado a antes del 02-11 por decisión de Diego
(2026-10-21). Decisión 0003 v6 §3 (control negativo del piloto); revisiones 11 y 12.

## Pregunta

¿El proceso de búsqueda de SQX con un embudo de filtros típico **distingue datos con estructura real de datos que, por
construcción, no tienen ninguna ventaja**? Y, en todo caso: **¿cuántas estrategias "buenas" fabrica el puro azar?**

Esto no busca estrategias: es una prueba de proceso con **datos quemados** (decisión 0002) y datos sintéticos.
Todo lo generado es familia `H0-proceso` y cuenta como hipótesis (regla 7). No se gastan datos de investigación.

## Brazos (los tres pasan por el mismo camino de importación de B1, para que nada los distinga salvo los datos)

| Brazo | Símbolo | Datos |
|---|---|---|
| Real | `USDCHF_B1` | velas M1 reales de la ventana quemada, ya importadas en B1 |
| Nulo 1 | `USDCHF_SINT1` | sintéticas, semilla 1 (`h0/configs/b17_sintetico.py`) |
| Nulo 2 | `USDCHF_SINT2` | sintéticas, semilla 2 |

**Datos sin ventaja:** cada vela real se descompone en su forma (salto desde el cierre anterior; máximo, mínimo y
cierre relativos a su apertura; volumen); las formas se barajan y se recompone la serie con las mismas horas y deriva
cero. Reparto de movimientos idéntico al real; ninguna dependencia temporal ni tendencia. Tests en
`tests/test_b17_sintetico.py`. **Límite conocido:** barajar destruye también la agrupación de volatilidad y la
estacionalidad intradía, que no son ventaja pero sí cambian cómo opera una estrategia; por eso se compara también el
número de operaciones entre brazos.

## Búsqueda (idéntica en los tres brazos)

Plantilla `h0/configs/b17_preparar_builder.py`: la del Builder de H0 (generación **aleatoria**, H1, spread 2,
deslizamiento 1, sin comisión ni swap, sin filtros ni cross checks) cambiando solo el símbolo, el inicio
(**2023.02.01**, margen de calentamiento de B1-bis), el número de estrategias N y un tramo **fuera de muestra
2024.04.01–2024.10.30** (dentro de muestra: 2023.02.01–2024.03.31). Sin filtros en SQX: **se guardan todas** las
estrategias generadas (C13) y el embudo se aplica después, igual para todos, en `h0/configs/b17_analizar.py`.

**N:** calibración con 50 estrategias en el brazo real (excluidas del análisis). Regla fijada:
N = mín(1.000, tiempo que cabe en 30 min por brazo), redondeado hacia abajo a múltiplos de 50; si N < 200, se para y
se replantea. El mismo N en los tres brazos.

## Embudo F (fijado ahora; umbrales genéricos de practicante, no los del curso)

- Dentro de muestra: operaciones ≥ 100, factor de beneficio ≥ 1,20, Ret/DD ≥ 2,0.
- Fuera de muestra: operaciones ≥ 20, beneficio neto > 0, factor de beneficio ≥ 1,10.

## Medidas y pruebas (fijadas ahora)

- **M1 – Tasa de falsos positivos:** fracción de estrategias de cada brazo nulo que pasa F completo.
- **T1 – Discriminación:** prueba exacta de Fisher de una cola: ¿pasan F más estrategias en el brazo real que en los
  nulos juntos? Nivel 0,05.
- **M2 – Persistencia:** correlación de Spearman entre Sharpe dentro y fuera de muestra (estrategias con ≥ 30
  operaciones dentro y ≥ 10 fuera), con p por permutación (2.000, semilla 17).
- **M3:** mediana del beneficio neto fuera de muestra del 10 % de estrategias con mejor Ret/DD dentro de muestra.
- **M4 – "Espectacular por azar":** la mejor estrategia por Sharpe dentro de muestra de cada brazo nulo, con sus cifras.

## Reglas de decisión (fijadas ahora)

- **S (validez del control):** en cada brazo nulo, Spearman con p ≥ 0,01 (sin persistencia). Si un nulo muestra
  persistencia fuerte, hay una fuga en el generador o en el backtest: **no se concluye nada** y se investiga.
- **D1:** si T1 **no** es significativa → "el embudo F no distingue estos datos reales del ruido". Consecuencia: en el
  piloto, pasar un embudo así **no cuenta como evidencia**; B19 tendrá que apoyarse en correcciones sobre el universo
  completo y en datos reservados; y el valor de SQX como generador no está demostrado (dato para A12).
  Ojo: puede deberse a que el USDCHF quemado no tenga ventaja; D1 no dice que SQX sea inútil, dice que **sus pasos por
  el embudo son compatibles con el azar**.
- **D2:** si T1 es significativa → el embudo detecta algo en estos datos. **No** es una ventaja operable (datos
  quemados, costes simplificados, sin examen); se registra el tamaño del efecto.
- En los dos casos, **M1 es el resultado principal**: cuánto aprueba el embudo cuando no hay nada que aprobar.

## Pasos

1. Generar `USDCHF_SINT1.csv` y `USDCHF_SINT2.csv` desde E_A de B1 (`lab_h0/b1/EA1`).
2. Importarlos (mismo instrumento, `EETUS`, `format=MetaTrader4 bar format`) y comprobar con los requisitos de B1:
   recuento de filas, zona declarada, y reexportación frente al archivo sintético (precios idénticos; volumen recortado
   solo donde supere 2³¹−1, como en el brazo real).
3. Exportar la configuración del Builder antes de tocarlo.
4. Calibración (50 en el brazo real) → N.
5. Para cada brazo: exportar el banco `Builder/Results` antes; cargar la plantilla y comprobarla; generar; exportar el
   banco después.
6. Restaurar el Builder y comprobarlo.
7. Analizar con `b17_analizar.py`. Todo por el ejecutor con registro; commit antes de cada orden; nada más usando la CPU.

## Lo que esta prueba NO demuestra

Que haya o no ventaja en EURUSD; nada sobre la generación genética (solo aleatoria); nada sobre filtros más
sofisticados (walk-forward, Monte Carlo); con N del orden de cientos, solo efectos grandes son detectables.
