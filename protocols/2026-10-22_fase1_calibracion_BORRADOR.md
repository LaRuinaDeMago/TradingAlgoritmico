# Fase 1 – Calibración del embudo (B17 mejorado) · BORRADOR v0

Estado: **BORRADOR v0** (diseño) · Redactado por: Claude, 2026-10-22, a petición de Diego ("mejorar el embudo de B17
para que sea más realista y en consonancia con lo que buscamos") · Marco: decisión 0004 v3 (P3, P4, P7, P12, P13) y 0003
v6 §3 · Aprobado por: — · Fecha de aprobación: —

> **Qué falta para la v1 (la que se congela y se ejecuta):** los huecos marcados **[PENDIENTE: …]**, que dependen de la
> fase 0 (B20, B21), de la ficha del método del curso (B22), de los costes (B5) y de A23. La v1 se escribe rellenando
> esos huecos, **no** rediseñando; se sube a git antes de la primera orden. Regla de trabajo: versión mínima que responda
> la pregunta (ESTADO §7).

## 1. Pregunta

¿Distingue nuestro embudo (generación, filtros, selección, construcción de cartera y, en su caso, el ciclo de IA) una
**ventaja sembrada de tamaño económicamente útil** de **datos sin ventaja**, con un procedimiento parecido al que de
verdad usaríamos? Si sí, hay permiso con evidencia para escalar (C23). Si no, sabremos qué pieza falla.

Superarla **no** demuestra ninguna estrategia rentable: demuestra capacidad para distinguir ciertos tipos de señal de
ciertos tipos de ruido (0004 §1).

## 2. Qué cambia frente a B17 y por qué

| B17 | Fase 1 | Por qué |
|---|---|---|
| Generación aleatoria | **Genética**, como la del curso y como la usaríamos | B17 no probó el motor real |
| Embudo genérico (IS/OOS) | Dos embudos: **C = el del curso, tal cual** (B22) y **L = el del laboratorio** (sin seleccionar con el fuera de muestra, con corrección por número de pruebas) | Probar el curso con justicia y medir si nuestras correcciones aportan |
| Un tipo de ruido (barajar velas) | **Tres familias de nulos**, separadas entre desarrollo y aceptación | Barajar destruye la agrupación de volatilidad y la estacionalidad (límite escrito en B17) |
| Sin ventaja sembrada | **Ventaja sembrada** con dos formas y tres tamaños | Medir la potencia, no solo los falsos positivos |
| Medida: cuántas pasan (Fisher) | **Expectativa neta por operación** e incertidumbre en un **tramo reservado**, por estrategia y **por cartera** | Lo que importa es lo que gana la cartera fuera de la selección (C24, P1) |
| Sin costes (v3) o costes que rompían el control (v2) | **Costes realistas**, juzgando siempre contra el nulo con los mismos costes | Lección de B17: la referencia es el nulo simulado, no el cero |
| 22 meses de USDCHF | Si Diego aprueba A23: **USDCHF 2003-01 → 2024-10** | Más operaciones y más regímenes |
| Sin IA | Brazo **L + IA** frente a L sin IA | Prueba de la 0001 (H3) y de C23 (a) |

## 3. Datos (ningún dato de investigación)

- Base: USDCHF M1 quemado (0002). **[PENDIENTE: A23 — ventana 2023-01 → 2024-10 o 2003-01 → 2024-10]**. Mismo camino de
  importación y comprobaciones de B1: recuentos, margen de calentamiento de un mes y volumen.
- Tres tramos en cada serie: **IS** (generación y filtros), **OOS** (lo usa el embudo C para seleccionar, como el curso;
  el embudo L lo usa solo dentro del walk-forward) y **RESERVA** final (último ≈ 20 %, **ningún embudo la toca**: es el
  examen de cada brazo).

## 4. Brazos

| Familia | Construcción | Uso |
|---|---|---|
| **N1 barajado** | La de B17 (`b17_sintetico.py`): formas de vela barajadas, deriva cero | Desarrollo |
| **N2 días barajados** | Se barajan **días enteros** (con sus formas de vela), deriva cero: conserva la estacionalidad intradía y la volatilidad dentro del día | Desarrollo |
| **N3 signo por bloques** | Se conserva la serie real de tamaños de movimiento (agrupación de volatilidad, regímenes, estacionalidad) y se **invierte al azar la dirección de cada día** (vela reflejada: máximo ↔ mínimo); deriva cero | **Aceptación** (familia que no interviene en el desarrollo) |
| **S1 horario** | Un nulo + deriva fija +δ en una franja horaria fija cada día | Desarrollo (sobre N2) |
| **S2 momentum condicional** | Un nulo + deriva en la dirección de la vela H1 anterior cuando su cuerpo supera un umbral fijo | **Aceptación** (sobre N3; forma distinta de la del desarrollo) |
| **Real** | USDCHF quemado sin tocar | Continuidad con B17; no decide nada |

- **Tamaños sembrados** (P3.2): δ tal que la **regla ideal** (la que conoce la ventaja) obtenga un Sharpe anual neto de
  costes de **0,5 · 1 · 2** en el tramo RESERVA. El de 0,5 es el mínimo que nos importaría operar; si el embudo no ve
  ni el de 2, no ve nada útil. La regla ideal es una referencia, no un objetivo para SQX.
- **Limitación escrita** (P3.2): una ventaja sembrada tan simple puede ser más fácil o más difícil de encontrar que una
  real; por eso la de aceptación tiene otra forma (S2) que la de desarrollo (S1).
- **Tamaño sembrado, sin ambigüedad:** el Sharpe ideal es **neto** de los costes del §6; la v1 escribe además, para cada
  tamaño, la expectativa por operación de la regla ideal, cuántas operaciones produce en IS, OOS y RESERVA, y cuándo deja
  de funcionar (fuera de su franja o condición). La potencia se mide **desde la generación** (SQX tiene que descubrir la
  ventaja desde cero), nunca dándole una estrategia que ya la trae.
- **Validez de los nulos** (que no sean "fáciles" para SQX): antes de usarlos, cada familia se compara con el real en lo
  que **debe** conservar (N2: perfil horario de la volatilidad; N3: agrupación de volatilidad y colas), y en todos los
  brazos se compara el número de operaciones y su duración, como en B17. Si una familia se aleja de lo que dice
  conservar, se corrige antes de ejecutar.
- **Tres funciones separadas** (revisión 16): *desarrollo* (N1, N2, S1: se miran y se corrige el embudo), *calibración*
  (los mismos brazos de desarrollo con réplicas nuevas: miden potencia y falsos positivos de la versión corregida) y
  *aceptación* (N3, S2: versión congelada, una vez, sin corregir después). El walk-forward interno del embudo L tampoco
  se usa para elegir variantes mirando sus resultados.
- **Semillas** fijadas en la v1 antes de ejecutar; las réplicas de aceptación **no se miran** hasta congelar los embudos.
- **Réplicas:** R por familia **[PENDIENTE: R según la precisión buscada y el tiempo medido de un brazo completo]**. La
  unidad de observación es la réplica; con pocas réplicas el resultado es exploratorio (tabla de límites en el §8).

## 5. Embudos (iguales en todos los brazos)

- **Generación:** genética, **[PENDIENTE: parámetros del curso (B22) y N por brazo según el tiempo medido]**. Capacidad
  del banco por encima de lo generado, con recuento antes y después de cada brazo (B17, B21).
- **C, curso tal cual:** filtros, umbrales y orden de los pasos de la ficha del método (B22), incluida la selección con
  OOS, walk-forward, Monte Carlo y el retest de mayor precisión. **Atajo:** las **configuraciones `.cfx` del propio
  curso** (Builder, Retester, Optimizer, ya extraídas en `LAB_PRIVADO_CURSO`) son la especificación más exacta: se cargan
  cambiando solo símbolo, fechas, costes y capacidad del banco; los vídeos completan el orden de los pasos y la
  selección manual ("las 50–100 de mayor Ret/DD"). **[PENDIENTE: B22 para lo que no esté en los `.cfx`]**
- **L, laboratorio:** los mismos bloques de robustez pero **sin elegir con el OOS** (walk-forward dentro de IS + OOS
  como un tramo más del walk-forward), filtros por **expectativa neta por operación** y su incertidumbre (C24), umbral
  ajustado al número de estrategias probadas (B19), y comprobación de que Ret/DD y PF no están recortados (B20).
- **Cartera** (P1): regla fijada antes, igual en C y L: **[PENDIENTE: p. ej. hasta k supervivientes, de menor a mayor
  correlación de sus resultados en IS, con el mismo riesgo cada una]**.
- **L + IA:** tras ver **solo los brazos de desarrollo**, Claude propone hasta **3 cambios** al embudo L, cada uno
  registrado como cambio de proceso (regla 8) con su motivo; se congela la versión final **antes** de abrir la
  aceptación. Se compara con L sin IA.
- **Comparaciones justas** (revisión 16): C, L y L + IA con el **mismo** número de estrategias generadas, el mismo tiempo
  de cálculo y el mismo presupuesto de variantes; se registran además la intervención humana, las variantes probadas y,
  en el brazo con IA, el modelo, las instrucciones y los cambios propuestos. Dos preguntas separadas: ¿mejora la IA la
  calidad? y ¿la mejora lo suficiente para justificar su coste (C23 d)?
- **Referencias sencillas** (C20) en todos los brazos: una regla de tendencia con parámetros fijos y entradas al azar
  con la misma frecuencia y costes.

## 6. Costes e integridad

- Costes **[PENDIENTE: B5; mientras tanto, los de SQX por defecto para el vehículo previsto, escritos en la v1]**, más un
  escenario adverso (deslizamiento × 2). Los mismos en todos los brazos.
- P12: el retest de mayor precisión es obligatorio para lo que llegue a cartera; el ratio realizado se mide en las
  operaciones (C24 c).

## 7. Medidas y criterios de aceptación (los números se fijan en la v1, antes de ejecutar)

Todo en el tramo RESERVA de los brazos de **aceptación** (N3, S2):

1. **Falsos positivos de cartera:** fracción de réplicas N3 en las que la cartera final tiene expectativa neta positiva
   con la confianza fijada **[PENDIENTE: nivel]**. Criterio: ≤ **[PENDIENTE]**.
2. **Potencia:** fracción de réplicas S2 en las que la cartera final captura la ventaja (expectativa neta positiva con la
   misma confianza), por tamaño. Criterio: ≥ **[PENDIENTE]** en el tamaño 1 (Sharpe ideal 1).
3. **Por estrategia:** tasa de falsos positivos del embudo (como M1 de B17) y supervivencia en S2.
4. **Comparaciones:** C frente a L; L + IA frente a L; las dos frente a las referencias sencillas. Con incertidumbre por
   remuestreo por bloques (B19), no solo con recuentos.
5. **Diagnósticos, sin decidir:** el brazo real; las rachas y caídas observadas frente a las esperadas (C24 d).

**Reglas de decisión** (P3.5):
- **Pasa** el embudo que cumple 1 y 2 → permiso para el piloto (fase 3) con ese embudo y para el escalón (b) de C23.
- **Ninguno pasa** → no se escala; se identifica la pieza (los brazos de desarrollo lo dicen) y se prueba una versión
  nueva **con réplicas de aceptación nuevas** (P3.4); como máximo **[PENDIENTE: n.º de vueltas]** antes de replantear.
- Si C y L pasan, se elige el de menor coste por candidata válida (C21). Si solo pasa C, el método del curso queda
  validado en lo que importa.

## 8. Presupuesto y plazo (P13)

**[PENDIENTE: cifras en la v1]**: horas de CPU, horas de Diego, plazo de calendario y llamadas de IA (0 por API en esta
fase: el ciclo lo hace Claude Code).

**Lo medido (registro n.º 204–222):** en B17, generar **1.000 estrategias aleatorias** (USDCHF H1, 21 meses) tardó
**74–87 s**, y cada brazo completo (exportar el banco antes y después, cargar y comprobar la plantilla) unos **5–6 min**.
**Lo que no está medido:** la generación genética, el walk-forward, Monte Carlo y el retest de mayor precisión sobre
las supervivientes, ni el efecto de 22 años de datos (A23), que puede multiplicar el tiempo por ~10. **Primer paso de la
v1: medir un brazo completo** (genética + embudo C) y dimensionar N y R con ese número, no con estimaciones.

**Si SQX no se renueva a tiempo (caduca el 2026-11-02, A12): núcleo mínimo antes de esa fecha.** Lo más informativo con
menos brazos: embudos C y L sobre **N3 y S2 (tamaño 1)**, R = 3, con la ventana de datos más corta si hace falta.
Responde si el embudo del curso distingue una ventaja útil de un ruido realista. Se declara como **parcial**: no
sustituye a la calibración completa ni da por sí solo el permiso para escalar.

**Cuántas réplicas hacen falta (revisión 17), con números.** La unidad de observación es la **réplica**, no la
estrategia: las miles de estrategias de una réplica comparten datos, generador y selección, y no son independientes. Si
un embudo no acepta ninguna cartera de ruido en R réplicas, el límite superior de su tasa de falsos positivos (95 %) es
1 − 0,05^(1/R):

| R | Límite superior con 0 aceptadas |
|---|---|
| 3 | 63 % |
| 14 | 19 % |
| 29 | 10 % |

Por eso **el núcleo mínimo (R = 3) es EXPLORATORIO**: sirve para encontrar errores, comprobar que el experimento
funciona y ver si hay diferencias grandes. **Nunca se presenta como "embudo calibrado"**. La calibración completa fija R
en la v1 según la precisión que necesitemos (orientativo: ~30 réplicas por familia de aceptación para acotar los falsos
positivos en torno al 10 %), lo que solo es viable si la medición del brazo completo dice que cada réplica cuesta poco.

**Interpretación fijada antes de ver resultados** (revisión 17):

| Resultado | Qué significa | Qué se hace |
|---|---|---|
| C y L aceptan ruido N3 | Ningún embudo discrimina con estos controles | No se escala; se mira en desarrollo qué pieza deja pasar el ruido |
| C y L no capturan S2 | Sin potencia para ese tamaño: o el embudo, o SQX no genera esa forma | Se comprueba el tamaño 2; si tampoco, se mira si el generador puede expresar la regla ideal |
| C ≈ L, los dos rechazan ruido y capturan S2 | Los dos funcionan; nuestras correcciones no añaden | Se usa el más barato (C21); el método del curso queda validado en lo que importa |
| L mejor que C | Mejor discriminación (no solo "rechaza más") con el mismo presupuesto | L pasa al piloto; se anota qué pieza marcó la diferencia |
| C y L parecidos e inconcluyentes | Puede ser el diseño de los controles, falta de potencia o que no hay mejora | No se concluye "inútiles": se revisan controles y potencia antes de nada más |

La unidad final sigue siendo la **cartera**: un embudo "gana" si produce carteras que discriminan ruido de señal, no si
aprueba o rechaza más estrategias.

## 9. Qué no demuestra

Nada sobre EURUSD ni ningún mercado real; nada sobre ventajas de formas muy distintas a S1 y S2; nada sobre ejecución
real. Es una prueba del procedimiento, con datos quemados y sintéticos (familia `H0-proceso`, regla 7).

## 10. Lo que hay que construir (mínimo)

- `b17_sintetico.py`: añadir N2 (días barajados), N3 (signo por bloques) y la siembra S1/S2, con tests como los de B17.
- `b17_analizar.py` → análisis de la fase 1: expectativa neta en RESERVA, cartera por regla, remuestreo por bloques
  (probablemente con A18: numpy/scipy).
- Plantillas del Builder genético y del Retester con los embudos C y L (scripts que se paran si algo no está donde se
  espera, como en H0).
