# AUDITORÍA MAESTRA DEL LABORATORIO DE TRADING ALGORÍTMICO

> Prompt propuesto por la revisión externa 08 (2026-10-20), guardado literalmente. Para usarlo en una **sesión
> independiente** de Claude Code (sin el contexto de quien construyó el laboratorio), en modo de **solo lectura**.
> Nota de Claude: el apartado 5 da por hecho que la 0003 no tiene límite numérico de ejecuciones; desde su versión 3
> sí lo tiene (ver su historial). El auditor debe partir de la versión vigente.

## Revisión independiente de arquitectura, rigor empírico, integración, viabilidad y prioridades

### 1. Tu función

Actúa como un equipo independiente compuesto por:

- Un investigador cuantitativo especializado en detección de ventajas estadísticas y sobreajuste.
- Un estadístico especializado en pruebas múltiples, dependencia temporal e incertidumbre.
- Un ingeniero de software especializado en reproducibilidad, pruebas y automatización.
- Un auditor de datos financieros y ejecución de estrategias.
- Un especialista en StrategyQuant X, backtesting y sistemas de trading minorista.
- Un investigador de sistemas de IA y evaluación experimental.
- Un responsable de seguridad, control de accesos y protección de datos.
- Un analista económico que evalúa costes, tiempo, capital y rentabilidad potencial.

Tu obligación no es validar el trabajo previo ni encontrar argumentos para continuar. Tu obligación es determinar qué tenemos realmente, qué falta, qué genera valor, qué introduce riesgos y cuál es el camino más racional.

Escribe en español, con precisión técnica, sin halagos, sin alarmismo y sin afirmaciones que no puedas respaldar.

### 2. Objetivo global del proyecto

Construir, dentro de los recursos y las limitaciones de un particular, un laboratorio cuantitativo integrado, reproducible, auditable y progresivamente automatizado que permita:

1. Investigar hipótesis de trading de manera sistemática.
2. Diferenciar ventajas estadísticas de resultados producidos por azar, selección múltiple, errores de datos o sobreajuste.
3. Validar estrategias independientemente de StrategyQuant X.
4. Aprovechar de manera controlada IA, Python, SQX, literatura científica, el curso de Imox y los resultados empíricos propios.
5. Comparar los resultados históricos con la ejecución prospectiva en demo.
6. Evaluar la viabilidad económica de cada estrategia en un vehículo concreto.
7. Aprender de los experimentos fallidos sin utilizar datos reservados para rescatar estrategias.
8. Limitar el gasto, el tiempo y la complejidad hasta que la evidencia justifique ampliar el proyecto.

La finalidad económica es investigar si existe una ventaja explotable neta de costes. No des por hecho que existe.

### 3. Restricciones absolutas

ANTES DE EMPEZAR:

- Lee README.md, CLAUDE.md, docs/hoja_de_ruta.md, todas las decisiones, h0/ficha.md, los protocolos vigentes, el registro de experimentos y las pruebas relevantes.
- Revisa el código del núcleo, el guardián, las pruebas automatizadas y las configuraciones pertinentes.
- Contrasta las afirmaciones de los documentos con las evidencias disponibles.
- Identifica contradicciones entre documentación, código, registros y estado declarado.
- Distingue lo verificado de lo afirmado, supuesto, pendiente o inconcluso.

SEGURIDAD Y ALCANCE:

- Esta es una auditoría de solo lectura.
- No modifiques archivos, configuraciones, decisiones ni registros.
- No ejecutes SQX, backtests, generación de estrategias, descargas de datos ni órdenes de trading.
- No accedas, listes, abras ni intentes deducir el contenido de data/sealed/ o de cualquier otra ubicación protegida.
- No eludas controles de seguridad, hooks, permisos ni restricciones.
- No abras cuentas, no utilices credenciales y no realices compras.
- No accedas a cuentas reales ni ejecutes operaciones reales.
- No publiques datos, identificadores, licencias, credenciales ni materiales privados.
- Si una comprobación exige ejecutar código, modificar el sistema o acceder a datos protegidos, descríbela como prueba pendiente y especifica un procedimiento seguro para una sesión posterior autorizada.
- No declares resuelto un problema de seguridad basándote exclusivamente en una inspección estática.
- No alteres la decisión 0003 ni la consideres aprobada. Su estado debe seguir siendo el que conste en el repositorio.

Si el entorno o los permisos no permiten verificar algo, decláralo explícitamente. Nunca eludas una limitación para completar la auditoría.

### 4. Revisión técnica y empírica del estado actual

Determina:

A. Qué capacidades están demostradas y cuáles no.

B. Qué demuestran exactamente las pruebas de reproducibilidad actuales y qué no demuestran.

C. Si los registros permiten reconstruir cada experimento, incluyendo código, datos, versiones, configuraciones, costes, semillas, resultados y decisiones de selección.

D. Si existen riesgos de pérdida de información, resultados sobrescritos, colisiones de nombres, registros incompletos, dependencias no fijadas o estados no reproducibles.

E. Si los controles de acceso y la protección del bloque sellado son suficientes, sin intentar acceder a él.

F. Si las fechas, zonas horarias, granularidad, datos históricos, spreads, comisiones, swaps y deslizamientos están correctamente tratados o requieren pruebas adicionales.

G. Si la futura reconstrucción independiente de SQX puede detectar errores de anticipación, sesgos temporales, costes mal aplicados y discrepancias en las operaciones.

H. Qué contradicciones existen entre la hoja de ruta, las decisiones 0001–0003, los protocolos, el código y las evidencias.

Para cada hallazgo indica la evidencia concreta, su alcance, su gravedad y cómo comprobarlo de forma segura.

### 5. Auditoría de la decisión 0003

Analiza expresamente:

- El reparto propuesto entre investigación, datos sellados y validación prospectiva.
- La viabilidad de exportar e importar los datos por fechas sin contaminación temporal.
- La elección provisional de EURUSD frente a los mercados del curso de Imox.
- La validez de utilizar los 24 meses propuestos como examen final y si la muestra esperada permite extraer conclusiones.
- El límite de 20 familias de hipótesis.
- La ausencia actual de un límite numérico de ejecuciones de SQX.
- El presupuesto de dinero, tiempo, cómputo, llamadas de IA y número de experimentos.
- Los criterios de abandono y sus posibles contradicciones.
- Las condiciones de seguridad anteriores a cualquier descarga.
- Los riesgos de que el bloque sellado influya directa o indirectamente en la selección de estrategias.

Propón los cambios mínimos necesarios para que la decisión sea coherente, verificable y económicamente responsable.

No inventes un número óptimo de ejecuciones sin estimar primero la capacidad de cómputo, el coste por lote, el tamaño de la búsqueda y la finalidad estadística. Explica qué datos faltan para fijarlo antes de la investigación confirmatoria.

### 6. Auditoría de las herramientas y su posible integración

Evalúa por separado y como sistema:

- StrategyQuant X y su interfaz de línea de comandos.
- Python, el núcleo del laboratorio y el registro de experimentos.
- Git, GitHub, las versiones de código y las evidencias.
- Claude Code.
- Otros modelos de IA como revisores adversarios.
- Papers, documentación oficial y curso de Imox.
- Transcripción y análisis de vídeos.
- Bases de datos, informes y visualizaciones.
- Automatización de experimentos.
- VPS, monitorización y ejecución prospectiva.
- APIs, almacenamiento, privacidad y costes recurrentes.

Para cada herramienta responde:

1. ¿Qué problema concreto resuelve?
2. ¿Qué mejora medible puede aportar?
3. ¿Existe una alternativa gratuita o más sencilla?
4. ¿Qué coste directo y de mantenimiento introduce?
5. ¿Qué nuevos riesgos o grados de libertad añade?
6. ¿Cuándo debería incorporarse?
7. ¿Cómo mediríamos si realmente aporta valor?
8. ¿Qué condición justificaría retirarla?

No recomiendes una herramienta por ser novedosa, potente o utilizada por profesionales.

### 7. Investigación científica y curso de Imox

Diseña una metodología para extraer conocimiento de artículos, documentación y vídeos sin convertirlos automáticamente en verdades.

Para cada fuente, el sistema debe distinguir:

- Afirmaciones originales del autor.
- Supuestos y limitaciones.
- Interpretaciones nuestras.
- Hipótesis nuevas.
- Pruebas concretas que podrían confirmar o refutar cada hipótesis.
- Referencias y trazabilidad hacia la fuente original.

Propón un piloto de transcripción y análisis de pocos vídeos antes de procesar el conjunto completo.

Prioriza la literatura sobre:

- Sobreajuste y selección entre múltiples estrategias.
- Deflated Sharpe Ratio, PBO y procedimientos de comparación múltiple.
- Validación temporal, walk-forward y fugas de información.
- Costes, deslizamiento y ejecución.
- Dependencia entre operaciones e incertidumbre estadística.
- Robustez, cambios de régimen y degradación.
- Riesgo de ruina, tamaño de posición y viabilidad del vehículo.
- Evaluación experimental de modelos de IA.

Comprueba las fuentes y evita presentar métodos estadísticos como garantías universales. No copies material protegido a repositorios públicos.

### 8. Diseño del aprendizaje empírico

Propón un ciclo de aprendizaje que permita:

1. Registrar hipótesis antes de probarlas.
2. Contabilizar familias, variantes, filtros, mercados, parámetros y cambios de proceso.
3. Documentar fallos y sus causas.
4. Detectar patrones recurrentes de fallo.
5. Generar nuevas hipótesis sin modificar retrospectivamente las pruebas.
6. Mantener intacto el bloque sellado.
7. Comparar los resultados nuevos con referencias apropiadas y con el proceso anterior.

Define cómo evaluaríamos si la IA mejora la investigación frente a un proceso sin IA, mediante tareas controladas, errores sembrados, calidad de resultados, falsas alarmas, tiempo y coste.

No utilices como métrica principal el número de estrategias generadas ni el número de estrategias que superan filtros internos.

### 9. Criterios económicos y de abandono

Define un marco que distinga:

- Viabilidad técnica del laboratorio.
- Calidad estadística de una estrategia.
- Ventaja neta de costes.
- Viabilidad en el vehículo previsto.
- Coherencia entre backtest y demo.
- Rentabilidad potencial frente al riesgo, el capital y los costes del proyecto.

Separa los gastos únicos de los recurrentes, el tiempo de trabajo, el coste de los datos, las licencias, las APIs y la infraestructura.

No inventes probabilidades de éxito ni estimaciones de rentabilidad futura sin evidencia suficiente.

Propón criterios que permitan continuar, corregir, pausar o abandonar. Un resultado inconcluso no debe convertirse automáticamente en favorable.

### 10. Entregables obligatorios

Entrega un informe estructurado con:

1. **Veredicto ejecutivo:** estado real del proyecto y si merece continuar.
2. **Inventario de capacidades:** demostrado, parcial, pendiente o desconocido.
3. **Hallazgos críticos:** contradicciones, defectos, riesgos y evidencia.
4. **Mapa de arquitectura objetivo:** componentes, responsabilidades, entradas, salidas e interdependencias.
5. **Auditoría de la decisión 0003:** mantener, modificar o rechazar cada apartado.
6. **Matriz de oportunidades:** valor esperado, coste, complejidad, riesgos, prioridad y condiciones de entrada.
7. **Lista explícita de cosas que NO debemos construir todavía.**
8. **Plan de trabajo priorizado:** siguiente tarea, dependencias, criterio de aceptación y evidencia requerida.
9. **Presupuesto y criterios de salida:** qué debe fijarse y qué información falta.
10. **Preguntas que requieren una decisión de Diego**, separadas de las cuestiones técnicas que puedes resolver con la evidencia disponible.

Para cada recomendación distingue entre:

- Evidencia observada.
- Inferencia razonable.
- Hipótesis que requiere prueba.
- Decisión que corresponde a Diego.

No modifiques el repositorio. No ejecutes las pruebas pendientes. No presentes una arquitectura futura como si ya estuviera implementada.

### 11. Criterio final

La pregunta rectora es:

¿Qué cambios aumentan realmente nuestra capacidad de encontrar una ventaja de mercado explotable y distinguirla del azar, por unidad de dinero, tiempo y complejidad, sin introducir sesgos o riesgos superiores al beneficio esperado?

Prioriza la calidad de la evidencia sobre la cantidad de herramientas.

El resultado debe ser un plan realista para llevar el laboratorio al máximo nivel que permitan los recursos de un particular, con rigor profesional, crecimiento modular y una posibilidad explícita de concluir que no existe una ventaja explotable.

No intentes demostrar que el proyecto merece continuar. Determina bajo qué condiciones merece continuar y qué evidencia nos obligaría a detenerlo.
