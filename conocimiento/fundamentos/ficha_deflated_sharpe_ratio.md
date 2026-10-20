# Ficha: Deflated Sharpe Ratio (DSR)

- **Fuente:** David H. Bailey y Marcos López de Prado, *The Deflated Sharpe Ratio: Correcting for Selection Bias,
  Backtest Overfitting and Non-Normality*, Journal of Portfolio Management (2014). SSRN 2460551. Copia leída: web del
  autor, `davidhbailey.com/dhbpapers/deflated-sharpe.pdf`, versión del 31-07-2014, 22 págs., SHA-256 `ca4a1e83…10b5`
  (no se sube al repositorio).
- **Leída por / fecha:** Claude · 2026-10-20 · **texto completo** (fórmulas comprobadas en la imagen de las págs. 8 y 10)
- **Bloque:** A · **Estado:** REVISADA (pendiente de aplicar en H2)

## 1. Qué problema aborda
El Sharpe de la mejor estrategia elegida entre muchas está inflado por dos causas: la **selección entre muchas pruebas**
(el máximo de muchos Sharpe es positivo aunque el Sharpe real de todas sea 0) y los **rendimientos no normales**
(asimetría y colas gruesas), agravados por muestras cortas.

## 2. Qué método propone
DSR = probabilidad de que el Sharpe real supere un umbral SR₀ que **crece con el número de pruebas** (ec. 2, pág. 8):

DSR = Z[ (SR − SR₀)·√(T−1) / √(1 − γ₃·SR + (γ₄−1)/4·SR²) ],
SR₀ = √V[{SRₙ}] · ((1−γ)·Z⁻¹[1−1/N] + γ·Z⁻¹[1−1/(N·e)])

SR = Sharpe de la estrategia elegida (no anualizado, en la frecuencia de los datos), T = nº de observaciones,
γ₃ = asimetría, γ₄ = curtosis, N = nº de pruebas **independientes**, V[{SRₙ}] = varianza de los Sharpe de todas las
pruebas, γ ≈ 0,5772 (Euler-Mascheroni), Z = normal estándar. Es el *Probabilistic Sharpe Ratio* (PSR) con el umbral
desplazado por la selección.

## 3. Supuestos y limitaciones (según los autores)
- Los Sharpe de las pruebas de una misma "clase de estrategia" siguen aproximadamente una normal (pág. 7).
- N son pruebas **independientes**; con M pruebas correlacionadas hay que estimar un N efectivo, por ejemplo
  N̂ = ρ̂ + (1−ρ̂)·M con la correlación media ρ̂ (apéndice A.3), o con medidas de información. Los autores advierten que
  la correlación media puede estar ella misma sobreajustada si M > T.
- La aproximación del máximo esperado sobreestima ligeramente con menos de ~50 pruebas (pág. 18).
- Hay que conocer **todas** las pruebas (N y su varianza): sin registro completo, no se puede calcular.

## 4. Afirmaciones, por tipo
| Afirmación | Tipo | Dónde |
|---|---|---|
| "Un backtest sin controlar la amplitud de la búsqueda no vale nada, por excelente que sea" | Conclusión publicada | Pág. 3 |
| El método *holdout* (una sola partición IS/OOS) **no impide** el sobreajuste por selección: aplicado suficientes veces, los falsos positivos pasan a ser **esperables** | Conclusión publicada | Pág. 6 |
| Con efectos de memoria (reversión), el sobreajuste tiende a **maximizar pérdidas** fuera de muestra | Conclusión publicada (demostrada en *Pseudo-Mathematics*) | Págs. 5–6 |
| Los ejercicios de pruebas múltiples deben **planificarse antes**; la teoría, no la potencia de cálculo, decide qué probar. Regla de parada tipo "problema de la secretaria" (muestrear ~37 % y quedarse con el primero que supere a todos) | Conclusión publicada (regla práctica) | Págs. 10–11 |
| Las ecuaciones 1–2 reproducen exactamente el ejemplo del paper: SR₀ = 0,1132, DSR = 0,9004 (N=100); 0,9505 (N=46); 0,9505 con rendimientos normales y N=88 | **Hecho verificado** | `verificaciones/dsr_ejemplo_paper.py` |
| Con V = 1/2 anual, el umbral anualizado que debe superar la mejor estrategia sube de 1,11 (N=10) a 1,79 (N=100), 2,30 (N=1.000), 2,44 (N=2.000), 2,73 (N=10.000) y 3,10 (N=100.000) | **Hecho verificado** (cálculo con la ec. 1; el valor de V es el del ejemplo, no el nuestro) | Misma verificación |
| En nuestro laboratorio, las estrategias de una misma generación de SQX estarán muy correlacionadas: su N efectivo será mucho menor que el número generado | Interpretación nuestra | — |
| Los topes de búsqueda de la 0003 (2.000 en el piloto; techos de 10.000 por familia y 100.000 en total) importan directamente: cada orden de magnitud más de búsqueda sube el listón que debe superar una candidata | Interpretación nuestra | — |

## 5. Qué podemos implementar con nuestros datos y herramientas
- El cálculo es sencillo (biblioteca estándar; numpy/scipy solo para estimar asimetría, curtosis y correlaciones a gran
  escala, asunto A18).
- Requisito: registrar **todas** las estrategias probadas con su serie de rendimientos (o al menos su Sharpe), no solo
  las que pasan filtros. SQX guarda resultados por estrategia; hay que exportarlos sistemáticamente.
- Estimar N efectivo: correlación media entre las series de rendimientos de las estrategias probadas (A.3), con la
  advertencia de los autores sobre M > T.

## 6. Qué control o prueba del laboratorio cambia
- **H2:** el DSR es candidato a **medida principal de EDGE** (o a una de ellas), calculado con el N efectivo de todo
  lo probado en la familia. Umbral de aceptación a fijar antes (el paper usa 95 %).
- **Registro:** cada experimento de búsqueda debe dejar el Sharpe (y la serie de rendimientos) de **cada** estrategia
  probada, también las descartadas, para poder calcular V[{SRₙ}] y N.
- **0003:** refuerza los topes de búsqueda y la planificación previa; respalda que el holdout del curso (OOS usado para
  seleccionar) no basta.
- **Banco de pruebas adversarias (C11):** un caso sembrado útil es "mejor de N estrategias aleatorias": el validador
  tiene que darle un DSR bajo.

## 7. Evidencia en contra o críticas conocidas
- El propio paper reconoce la dependencia del supuesto de normalidad de los Sharpe entre pruebas y la dificultad de
  estimar N efectivo. Proponen como complemento el umbral de Harvey y Liu (2014), basado en el control de la tasa de
  falsos descubrimientos (Benjamini-Hochberg). **Pendiente:** buscar críticas publicadas al DSR (p. ej. sobre su
  sensibilidad a la estimación de N), según la regla 3 de `conocimiento/README.md`.
