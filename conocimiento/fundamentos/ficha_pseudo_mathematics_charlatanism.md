# Ficha: Pseudo-Mathematics and Financial Charlatanism (sobreajuste y longitud mínima del backtest)

- **Fuente:** David H. Bailey, Jonathan M. Borwein, Marcos López de Prado y Qiji Jim Zhu, *Pseudo-Mathematics and
  Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance*, Notices of the American
  Mathematical Society 61(5), mayo 2014, 458–471. SSRN 2308659. Copia leída: web del autor,
  `davidhbailey.com/dhbpapers/backtest-pseudo.pdf` (versión del 1-04-2014), 34 págs., SHA-256 `6e790c41…a0f3e` (no se
  sube). La copia de la AMS no se pudo descargar (devuelve una página web, no el PDF).
- **Leída por / fecha:** Claude · 2026-10-20 · **texto completo**
- **Bloque:** A · **Estado:** REVISADA (aplicable ya a la 0003)

## 1. Qué problema aborda
Con muy pocas pruebas ya es fácil obtener un backtest con Sharpe alto **sin ninguna habilidad**, y casi nunca se informa
de cuántas configuraciones se probaron, así que el inversor no puede juzgar el sobreajuste.

## 2. Qué método propone
- **Máximo esperado del Sharpe** entre N configuraciones sin habilidad (Sharpe real 0), 1 año de datos (ec. 2.4):
  E[max_N] ≈ (1−γ)·Z⁻¹[1−1/N] + γ·Z⁻¹[1−1/(N·e)]. Con y años se divide por √y (ec. 3.1). Cota superior: √(2·ln N).
- **Longitud mínima del backtest (MinBTL)** (teorema 3.1): años necesarios para que el mejor de N, sin habilidad, no
  supere por azar un Sharpe objetivo: MinBTL ≈ (E[max_N] / objetivo)² < 2·ln(N) / objetivo². **Condición necesaria,
  no suficiente**: un backtest más largo puede seguir sobreajustado.

## 3. Supuestos y limitaciones (según los autores)
- Rendimientos aproximadamente normales e IID para la distribución del Sharpe (pág. 8); pruebas **independientes**
  (si no lo son, estimar N efectivo, p. ej. con componentes principales). Con pruebas correlacionadas, la estimación es
  conservadora.

## 4. Afirmaciones, por tipo
| Afirmación | Tipo | Dónde |
|---|---|---|
| Con N = 10 configuraciones y 1 año, el mejor tiene Sharpe esperado ≈ 1,57 aunque ninguna tenga habilidad | **Hecho verificado** (1,57) | Pág. 9; `verificaciones/minbtl_ejemplos_paper.py` |
| Con 5 años de datos, no más de 45 configuraciones independientes para que el mejor por azar no pase de Sharpe 1; con 2 años, 7 | **Hecho verificado** (5,00 y 1,92 años) | Págs. 11–12; misma verificación |
| 7 parámetros binarios (N = 128) dan un máximo esperado superior a 2,6 | **Hecho verificado** (2,62) | Pág. 13 |
| La complejidad del modelo facilita el sobreajuste; **los filtros de análisis técnico** (condiciones que disparan operaciones) actúan como interruptores que multiplican N | Conclusión publicada | Págs. 11–13 |
| El software comercial permite **añadir filtros sin informar** de cuánto aumentan la probabilidad de sobreajuste | Conclusión publicada | Págs. 13–14 |
| Sin memoria en la serie, el sobreajuste da rendimiento OOS ≈ 0; **con memoria (reversión, autocorrelación) da rendimiento OOS negativo**, y cuanto más se optimiza IS, peor OOS (proposiciones 6.1–6.3, demostradas) | Conclusión publicada (con demostración) | Págs. 14–23 |
| No declarar el número de pruebas es análogo al fraude de las predicciones enviadas a muchos y quedarse con los que acertaron | Conclusión publicada | Pág. 23 |
| En una serie aleatoria, la mejor regla estacional entre 8.800 da Sharpe 1,27 y PSR 2,83 (aparentemente significativa) | Conclusión publicada (ejemplo simulado) | Págs. 25–26 |
| **Nuestro reparto:** con 7 años para investigar caben como mucho **~139 configuraciones independientes** antes de que la mejor llegue a Sharpe 1 por azar; con el bloque sellado de ~24 meses, **~7** | **Hecho verificado** (cálculo con sus fórmulas) / la aplicación es interpretación nuestra | Misma verificación |
| Con 2.000 / 10.000 / 100.000 configuraciones independientes en 7 años, la mejor tendría por azar Sharpe ≈ 1,30 / 1,46 / 1,66 | **Hecho verificado** (cálculo) | Misma verificación |
| El tope de **3 candidatas al examen sellado** (0003) queda por debajo de las ~7 que admite un bloque de 24 meses: es coherente | Interpretación nuestra | — |
| Las miles de estrategias de SQX están muy correlacionadas: su N independiente es mucho menor que el número generado, pero **no sabemos cuánto** hasta medirlo | Hipótesis por comprobar (piloto de la 0003) | — |
| La lección 01 del laboratorio ya usaba √(2·ln N) y vio que sobrestima (1,66 frente a 1,60 con N = 1.000): coincide con que es una **cota superior** | Hecho verificado (diario, 2026-10-19) | `aprendizaje/diario.md` |

## 5. Qué podemos implementar con nuestros datos y herramientas
- MinBTL y el máximo esperado son fórmulas de una línea (ya en `verificaciones/`).
- Lo difícil es **estimar N independiente** de una búsqueda de SQX: requiere las series de resultados de todas las
  estrategias probadas (mismo requisito que DSR y PBO).

## 6. Qué control o prueba del laboratorio cambia
- **0003, presupuesto de búsqueda:** el piloto y la fase confirmatoria deben estimar el **N efectivo** de lo generado y
  compararlo con el límite de ~139 independientes del bloque de investigación (para el umbral de Sharpe 1). Si el N
  efectivo lo supera, hay que exigir un listón más alto (DSR) o reducir la búsqueda.
- **0003, examen sellado:** el tope de 3 candidatas queda respaldado.
- **Registro:** declarar siempre N (también los filtros añadidos, que cuentan como pruebas).
- **Auditoría del curso:** búsqueda genética con reinicios + filtros sin informar de N es exactamente el patrón que
  describe el paper.

## 7. Evidencia en contra o críticas conocidas
- Supuesto de normalidad e independencia; los propios autores lo llaman conservador. **Pendiente:** buscar críticas
  publicadas (p. ej. sobre el uso del Sharpe con rendimientos muy no normales, típico de estrategias con stops y objetivos).
