# Ficha: Probability of Backtest Overfitting (PBO) y validación cruzada CSCV

- **Fuente:** David H. Bailey, Jonathan M. Borwein, Marcos López de Prado y Qiji Jim Zhu, *The Probability of Backtest
  Overfitting*, Journal of Computational Finance (versión revisada de febrero de 2015). SSRN 2326253. Copia leída: web
  del autor, `davidhbailey.com/dhbpapers/backtest-prob.pdf`, 34 págs., SHA-256 `d8bfbada…a63d` (no se sube al repositorio).
- **Leída por / fecha:** Claude · 2026-10-20 · **texto completo**
- **Bloque:** A · **Estado:** REVISADA (pendiente de aplicar en H2)

## 1. Qué problema aborda
No mide si una estrategia es buena, sino si **el proceso de elegir la mejor entre N es fiable** o si está eligiendo
ruido. Las técnicas habituales contra el sobreajuste (sobre todo el *holdout*, una única partición fuera de muestra)
no tienen en cuenta cuántas configuraciones se probaron antes de elegir.

## 2. Qué método propone
- **Definición:** hay sobreajuste si la configuración que es la mejor dentro de muestra (IS) queda, en promedio, **por
  debajo de la mediana** fuera de muestra (OOS). **PBO** = probabilidad de que la mejor IS quede por debajo de la mediana
  OOS (def. 2.2, pág. 10).
- **CSCV** (validación cruzada combinatoria simétrica, alg. 2.3, págs. 11–12):
  1. Matriz M de T × N: los resultados (pérdidas y ganancias) de **todas** las N configuraciones probadas, en las
     mismas T fechas.
  2. Se parte en S bloques temporales iguales (S par), **sin barajar** (respeta la dependencia temporal).
  3. Para cada una de las C(S, S/2) combinaciones: la mitad de bloques es IS y la otra mitad OOS; se elige la mejor IS
     y se mira su rango relativo ω fuera de muestra; logit λ = ln(ω / (1−ω)).
  4. PBO = proporción de combinaciones con λ ≤ 0.
- Además da: **degradación** (relación entre el rendimiento IS y OOS de la elegida; con sobreajuste suele ser
  negativa), **probabilidad de pérdida** OOS de la elegida y **dominancia estocástica** (si elegir con el backtest es
  mejor que elegir al azar entre las N).

## 3. Supuestos y limitaciones (según los autores, sección 5)
- Exige **información completa de todas las pruebas**; ocultar pruebas infravalora el sobreajuste, y añadir pruebas
  condenadas a fallar para que una destaque lo sesga al revés.
- **Búsquedas guiadas** (como una optimización genética): las columnas deben ser el **resultado final de cada
  búsqueda**, no los pasos intermedios.
- **No evalúa si el backtest es correcto:** con costes mal puestos o información del futuro, la PBO se calcula sobre
  datos falsos.
- Solo ve los cambios de régimen presentes en los datos.
- Una PBO alta no excluye que haya estrategias con habilidad (p. ej. muchas buenas y parecidas).
- **No se debe usar la PBO para guiar la búsqueda** ni como función objetivo: "cuando una medida se convierte en
  objetivo, deja de ser una buena medida".
- S grande rompe la estructura temporal; S pequeño da pocas combinaciones. Proponen S = 16 como valor razonable.
  T debería ser el doble de las observaciones usadas para elegir.

## 4. Afirmaciones, por tipo
| Afirmación | Tipo | Dónde |
|---|---|---|
| El holdout falla por 5 motivos: el investigador pudo usar ese tramo; conoce qué pasó en ese periodo; con muestras pequeñas no concluye nada (citan ≥ 1.000 observaciones); consume datos valiosos; y no tiene en cuenta el número de pruebas | Conclusión publicada | Págs. 6–7 |
| En un paseo aleatorio, la mejor regla estacional entre 8.800 combinaciones da Sharpe 1,27 y PSR de 2,83 ("significativa al 99 %"), pero su PBO es del 55 %; con un efecto estacional real inyectado, PBO del 13 % | Conclusión publicada (ejemplo con datos simulados) | Págs. 25–27 |
| Con sobreajuste, cuanto más alto el Sharpe IS, más bajo tiende a ser el OOS: **no se escapa del sobreajuste exigiendo un Sharpe IS más alto** | Conclusión publicada | Pág. 16 |
| C(12,6) = 924 y C(24,12) = 2.704.156 combinaciones; error típico máximo con S = 16: 0,0044 | **Hecho verificado** | Cálculo propio (registro de esta ficha) |
| **Errata del paper:** con S = 16 salen **12.870** combinaciones, no 12.780 (pág. 11). No cambia ninguna conclusión | **Hecho verificado** | Cálculo propio |
| El "filtro por Ret/DD alto" del curso es justamente el tipo de criterio que el paper muestra que no protege | Interpretación nuestra | Auditoría privada del curso |
| SQX descarta las estrategias que no pasan los filtros: **sin cambiar eso, no tendremos las N columnas** que la PBO necesita | Hipótesis por comprobar | Tareas 3a y 7 (solo se guardaron las que pasaron) |

## 5. Qué podemos implementar con nuestros datos y herramientas
- CSCV es sencillo de programar (ordenar, partir, combinar); con S = 16 son 12.870 combinaciones: asumible en Python.
- **Requisito crítico de datos:** la serie diaria de resultados de **cada** estrategia probada, en fechas comunes.
  SQX guarda una curva diaria por estrategia guardada (`dailyEquity.bin` dentro del `.sqx`, formato binario por
  descifrar) y las operaciones exportables a CSV; hay que comprobar si se pueden conservar también las descartadas.

## 6. Qué control o prueba del laboratorio cambia
- **H2:** PBO por CSCV como medida de **calidad del proceso de selección** de cada familia, junto al DSR (que evalúa la
  estrategia elegida). Umbral a fijar antes de mirar (los autores sugieren rechazar con PBO > 0,05 en el marco
  clásico).
- **Piloto de la 0003:** además de coste y supervivencia, medir si SQX permite **conservar todas** las estrategias
  probadas con su serie diaria; si no, la PBO no es calculable y hay que replantear cómo se registra la búsqueda.
- **Generación genética:** contar como pruebas los resultados finales de cada búsqueda (cada reinicio o isla), según
  los autores.
- **Banco de pruebas adversarias (C11):** "mejor regla entre muchas sobre un paseo aleatorio" debe dar PBO alta; "con
  efecto real inyectado" debe dar PBO baja. Es la misma prueba del paper y sirve para validar nuestra implementación.
- **Prohibido** usar la PBO como objetivo de la búsqueda.

## 7. Evidencia en contra o críticas conocidas
- Los propios autores dicen que CSCV es **una** implementación posible y que con autocorrelación fuerte o información
  estructural pueden ser mejores otros métodos (sección 5.1). **Pendiente:** buscar críticas publicadas y alternativas
  (p. ej. *Reality Check* de White 2000 y *SPA* de Hansen, citados en la tradición de pruebas múltiples).
