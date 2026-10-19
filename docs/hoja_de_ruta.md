# Proyecto Trading Algorítmico — Hoja de ruta definitiva (v1.1)

Transcripción de `hoja_de_ruta_v1.1.pdf` (Diego, 20-oct-2026). Si hay diferencias, manda el PDF.

## Objetivo y alcance

Construir un laboratorio de investigación cuantitativa que integre IA, StrategyQuant X (SQX) y validación propia, capaz de decir con evidencia si una estrategia tiene ventaja real o es ruido.

Construir el laboratorio es un objetivo técnico razonable. Obtener ingresos fiables es una hipótesis que el laboratorio tendrá que demostrar o descartar. Equipo: Diego (decisión, mercado, curso SQX de Imox) y Claude (código, validación, auditoría).

**Techo realista:** un proceso reproducible, que sabe cuántas hipótesis ha probado, no usa información del futuro, mide su mejora frente a referencias sencillas y sabe decir cuándo no hay evidencia suficiente. Más API o más estrategias no suben el techo; solo lo sube mejor evidencia.

## Principios

Estas siete reglas están por encima de cualquier resultado atractivo.

1. **Poder concluir "no hay edge".** Si el sistema no puede llegar honestamente a esa conclusión, sus resultados positivos tampoco son fiables.
2. **Trazabilidad total.** Hashes de datos y código, versiones de dependencias, configuración de costes, semillas aleatorias y registro de todos los experimentos, incluidos los fallidos, y de las decisiones de selección (parámetros, mercados, filtros, periodos y cambios posteriores). Se estima el número efectivo de pruebas, no solo el de estrategias.
3. **Datos sellados.** Un conjunto final inaccesible a la investigación. Antes de abrirlo se fija por escrito quién accede, qué estrategia se evalúa, qué métricas se calculan y qué decisión se toma con cada resultado. Una vez examinado, deja de ser prueba final para la siguiente iteración. También se congela el procedimiento (estrategia, costes, métricas, criterios de aprobación y código evaluador) y cada acceso queda registrado.
4. **Referencias comparables.** Estrategias aleatorias con la misma exposición, frecuencia, costes y restricciones; comprar y mantener; reglas simples de tendencia y reversión a la media.
5. **IA con hipótesis preregistradas.** La IA propone y las reglas deterministas deciden. Diego aprueba cualquier paso a dinero real.
6. **Nada entra sin demostrar valor.** Una API, un modelo o un agente solo se queda si mejora las decisiones de forma demostrable.
7. **Presupuesto y salida.** El proyecto tiene límites medibles (dinero, duración, ejecuciones de SQX, llamadas de API, tiempo de cómputo e iteraciones) y criterios para abandonarlo.

## Dos veredictos por estrategia

Cada estrategia recibe dos veredictos independientes. Una puede tener esperanza positiva y no servir para una cuenta fondeada, o cumplir los límites sin rentabilidad neta atractiva.

| Veredicto | Pregunta | Qué mide | Resultados posibles |
|---|---|---|---|
| EDGE | ¿Hay ventaja real? | Resultado fuera de muestra neto de costes y frente a referencias, con intervalos de incertidumbre, tamaño de muestra, concentración de beneficios y corrección por selección entre múltiples estrategias | FAVORABLE · DESFAVORABLE · INCONCLUSO |
| VIABILIDAD (una por vehículo) | ¿Sirve en este vehículo concreto? | Riesgo de ruina o de suspender el reto según las reglas contractuales exactas y con escenarios de ejecución adversa, costes de ejecución del broker y reglas propias de Darwinex Zero, cada fondeada o capital propio | VIABLE · NO VIABLE · INCONCLUSO |

Solo pasa a demo una estrategia con EDGE favorable y VIABILIDAD favorable para un vehículo concreto. INCONCLUSO significa reunir más evidencia o descartar, nunca aprobar.

## Arquitectura

La IA propone; las reglas y Diego deciden.

```
SQX: generación (datos de Darwinex)  <── propone experimentos ──  IA analista (Claude)
        │                                                          lee resultados del núcleo,
        ▼                                                          hipótesis preregistradas,
Núcleo Python (registro inmutable, versiones y hashes)  ─────────► nunca decide ni opera
        ▼
Validación determinista (veredictos EDGE y VIABILIDAD)
        ▼  solo con aprobación de Diego
Ejecución demo y real (MT4/MT5, Darwinex Zero, fondeadas)
        ▼
Monitor de tres capas (operativa, riesgo y degradación) ──realimenta──► Núcleo
```

El núcleo registra todo lo que pasa por el sistema. La IA lee resultados y propone experimentos, pero la validación determinista decide y solo Diego autoriza el paso a real. El monitor separa protección operativa, límites de riesgo y detección estadística de degradación.

## Herramientas y forma de trabajo

Claude Code, instalado en el PC donde está SQX, es el banco de trabajo: maneja SQX por línea de comandos, construye y ejecuta el código y mantiene el registro. Las reglas del proyecto se imponen técnicamente, no solo por escrito.

| Pieza | Función |
|---|---|
| CLAUDE.md | Reglas duras y tareas activas que cada sesión de Claude Code lee al empezar |
| Bloqueos automáticos (hooks) | Impiden leer data/sealed/ sin un protocolo aprobado |
| registry/ | Registro de experimentos y accesos; solo se añade, nunca se borra |
| h0/ficha.md | Ficha de viabilidad con estado y evidencia por capacidad |

Reparto: Diego decide y aprueba; Claude Code construye, ejecuta y registra; Claude en el chat diseña y audita resultados.

## Contexto: mercados, datos y vehículos

El curso de Imox trabaja oro, Nasdaq y DAX, y después divisas, con datos de Darwinex para generar estrategias. Todo lo que sigue son candidatos pendientes de verificar en H0, no decisiones.

| Elemento | Situación | Riesgo o nota |
|---|---|---|
| Oro, Nasdaq, DAX | Mercados del curso | Muy minados por usuarios de SQX; el primer mercado se elige con criterios fijados antes de ver backtests |
| Divisas | Fase posterior | Mismo criterio de selección |
| Datos Darwinex | Fuente para generar | Coherentes con Darwinex; si se ejecuta en otro broker, modelar sus costes |
| MetaTrader 4 | Plataforma de Imox para fondeadas y capital propio | Confirmar compatibilidad con la exportación de SQX |
| Darwinex Zero | Candidato a primer vehículo real | Verificar condiciones vigentes, instrumentos, costes y límites |
| Axi Select | Vehículo posterior | Verificar condiciones vigentes |
| Cuentas fondeadas | Vehículo posterior | Simular límite diario, pérdida máxima, trailing drawdown y fases |

**SQX disponible:** edición Ultimate, build 143.2708, en prueba gratuita de 14 días. La documentación oficial confirma una interfaz de línea de comandos (sqcli.exe) desde la build 127; qué permite realmente se verifica en H0.

## Hitos

Cada hito tiene que cumplir su criterio de salida antes de empezar el siguiente.

1. **H0 – Ficha de viabilidad técnica.** Salida: cada capacidad verificable marcada SÍ o NO; lo que aún no se ha podido probar queda como INCONCLUSO. Plazo: dentro de la prueba gratuita de SQX.
2. **H1 – Puente SQX.** Salida: recorrido completo sin errores (generar, exportar, ejecutar en la plataforma prevista, recuperar las operaciones y reproducir de forma independiente). Incluye un registro mínimo de experimentos desde el primer ensayo. Que funcione no demuestra ningún edge.
3. **H2 – Motor de validación.** Salida: emite EDGE y VIABILIDAD con incertidumbre explícita, con la definición de EDGE favorable (medida principal, dependencia entre operaciones, costes y criterio de comparación) fijada antes de evaluar nada, y reproduce resultados de forma independiente.
4. **H3 – IA analista.** Salida: hipótesis preregistradas contrastadas con datos no vistos; se compara con un proceso sin IA, con criterios fijados antes, para ver si mejora las decisiones de investigación.
5. **H4 – Validación prospectiva en demo.** Salida: monitor de tres capas probado antes de operar (apagado de emergencia, límites de riesgo, recuperación tras desconexión) y resultados en demo coherentes con lo validado.
6. **H5 – Operación real, vehículo a vehículo.** Salida: para Darwinex Zero, cada fondeada o capital propio, VIABILIDAD propia, comprobación de que las condiciones reales coinciden con las simuladas y autorización independiente de Diego. Se empieza con tamaño mínimo.
7. **H6 – Panel.** Interfaz sobre un motor ya validado.

## H0: comprobaciones y decisiones pendientes

Ver `h0/ficha.md` (lista viva con estado y evidencia).

**Siguiente paso de Diego:** instalar Claude Code en el PC de SQX, crear la carpeta del proyecto con CLAUDE.md y pedirle que empiece la tarea 1 del H0. Pendiente confirmar qué día de la prueba es y el sistema operativo.

## Criterios de abandono y presupuesto

El proyecto se detiene o se replantea si ocurre cualquiera de estas situaciones. Las cifras concretas se fijan en H0, antes de ver ningún resultado.

- H0 demuestra que el flujo completo exige demasiada intervención manual.
- Se agota el presupuesto de experimentación sin ninguna estrategia con veredicto EDGE favorable.
- Las estrategias aprobadas no baten de forma clara a las referencias comparables en los datos sellados.
- En demo, los resultados se apartan de lo validado más de lo que explica la varianza esperada.
- Se supera el límite de tiempo o dinero acordado.

Concluir "no hemos encontrado edge" es un resultado válido del proyecto, no un fracaso del laboratorio.

## Fuentes

- [StrategyQuant: Introduction to CLI](https://strategyquant.com/doc/cli-command-line/introduction-to-cli/)
- StrategyQuant: soporte y ediciones
