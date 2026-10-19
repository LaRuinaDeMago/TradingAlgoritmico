# Aprendizaje

Este proyecto es también una escuela, para Diego y para Claude. Se aprende **haciendo**: cada lección
nace de algo que acabamos de construir o de un error que acabamos de cometer, y trae un ejercicio que se ejecuta.

## Cómo funciona

- **Lecciones** (`lecciones/`): una por bloque de trabajo. Cada una tiene la misma forma:
  *qué es → por qué importa para no perder dinero → cómo lo hacemos en el laboratorio → ejercicio → preguntas para comprobarlo*.
- **Ejercicios** (`ejercicios/`): scripts cortos y reproducibles (semilla fija) que muestran la idea con números.
- **Glosario** (`glosario.md`): cada término nuevo, explicado en una o dos frases.
- **Diario de lecciones** (`diario.md`): lo que hemos aprendido trabajando, sobre todo de los errores. Claude lo lee al empezar
  cada sesión; así no repite fallos aunque no tenga memoria entre sesiones.

Ritmo: subir de nivel en cada lección, sin repetir lo ya sabido. Si algo no queda claro, se pregunta y se amplía la lección.
Si Diego ya domina algo, se salta.

## Itinerario

Cada nivel acompaña a un hito de la hoja de ruta. Los niveles se tocan entre sí: si un tema hace falta antes, se adelanta.

| Nivel | Hito | Temas |
|---|---|---|
| 1. Herramientas y método | H0 | Git y commits, hashes, registro solo-añadir, reproducibilidad, semillas. **El azar que parece ventaja.** Datos sellados y por qué existen |
| 2. El backtest por dentro | H1 | Velas frente a ticks, spread, comisión, swap y deslizamiento. Sesgo de anticipación (usar el futuro sin querer). Dentro y fuera de muestra. Reproducir SQX en Python |
| 3. ¿Es real o es suerte? | H2 | Distribuciones y colas gordas. Remuestreo (bootstrap) por bloques. Intervalos de confianza. Corrección por pruebas múltiples (Sharpe deflactado, SPA). Estrategias aleatorias de referencia. Walk-forward bien y mal hecho |
| 4. Riesgo y supervivencia | H2 (viabilidad) | Drawdown, riesgo de ruina, tamaño de posición, Kelly fraccionado. Monte Carlo de las reglas de una cuenta fondeada |
| 5. IA con método | H3 | Preregistro de hipótesis. Revisión adversaria. Cómo medir si un modelo aporta (errores sembrados). Sesgos de los LLM |
| 6. Ejecución y vigilancia | H4–H5 | Demo frente a backtest. Detectar degradación (CUSUM, SPRT). Apagado de emergencia. Reconciliar operaciones |

## Lecciones

| # | Lección | Nivel |
|---|---|---|
| 01 | [El azar que parece ventaja, y cómo nos protegemos de él](lecciones/01_azar_y_registro.md) | 1 |
