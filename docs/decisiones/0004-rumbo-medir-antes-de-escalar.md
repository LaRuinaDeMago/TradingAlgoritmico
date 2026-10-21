# Decisión 0004 – Rumbo de investigación: medir antes de escalar

Fecha: 2026-10-21 · Estado: **ACEPTADA (versión 3)** el 2026-10-21 por Diego ("me parece perfecto" a la v2 y "vamos a
cerrarlo y guardarlo definitivamente" con los ajustes de la revisión 15), con la redacción de Claude · Complementa a: 0003
v6 (no la sustituye; donde choquen se saca una 0003 v7 explícita, nunca un cambio en silencio) · Cambiarla exige una
decisión nueva que cite a esta, o una versión nueva registrada (P7).

> Origen: conversación Diego–Claude del 2026-10-21 (sin tocar el repositorio) y tres revisiones externas aportadas por
> Diego, de las que solo se incorpora lo nuevo (A21): `docs/revisiones/2026-10-21_13-15_revisiones_0004.md`.
> Diego planteó su objetivo original: aprovechar SQX "al techo", con IA por API y una VPS, para analizar muchísimas
> estrategias, en varios mercados, y acabar con una cartera que tenga ventaja. Esta decisión es cómo se persigue ese
> objetivo sin engañarnos.

## 1. Objetivo operativo

Desarrolla el objetivo A5 de `CLAUDE.md`:

> **Maximizar la probabilidad de descubrir una ventaja neta de costes por cada euro, hora y dato limpio gastados, y
> después la probabilidad de que sobreviva fuera del backtest.**

No sabemos cuánto podemos subir esa probabilidad; los experimentos sirven para medirla. **No encontrar una ventaja útil
dentro del alcance probado es un resultado válido.** "Llevarlo al techo" es el máximo rigor y capacidad de
descubrimiento que permiten nuestro presupuesto y nuestros datos, sin confundir complejidad con ventaja; no el máximo
número de estrategias generadas.

Superar la fase 1 **no** demostraría que tenemos una estrategia rentable: demostraría que tenemos un procedimiento con
capacidad acreditada para distinguir **ciertos** tipos de señal de **ciertos** tipos de ruido. Eso justifica invertir en
la fase siguiente, no saltarse puertas.

## 2. Punto de partida (hechos del registro n.º 1–222)

- **Herramienta:** SQX *Pro Build 145 (Trial)*, build 145.3191 de desarrollo. El circuito por línea de comandos funciona
  (generar, backtest, CSV, MT4/MT5: tareas 3–4); compilar MT, INCONCLUSO (sin MetaTrader, A11).
- **Reproducibilidad:** 1.353 operaciones idénticas en dos backtests, con control negativo que falla al cambiar el
  spread (tarea 4).
- **Integridad de datos (B1):** volumen recortado a 2³¹−1 al importar; sin calentamiento se pierden las primeras
  operaciones; la zona horaria de SQX es solo una etiqueta; con un mes de margen, 1.277 operaciones idénticas (B1-bis SÍ).
- **Control negativo de la búsqueda (B17, D1; `h0/b17_resultados.md`):** con generación **aleatoria** y un embudo de
  filtros típico, en USDCHF quemado H1, sin costes, el embudo aprobó 2 de 1.000 estrategias en datos reales y 16 de 2.002
  en dos series sintéticas sin ventaja (0,8 %; con costes, 0,1 %). En el contraste definido en B17 (Fisher unilateral,
  "real > nulos") no se detectó que el real supere a los nulos (**p = 0,99**). Esto **no demuestra equivalencia
  universal**; sí justifica tratar "pasa los filtros" como compatible con el azar e investigar si el embudo carece de
  capacidad discriminante. En ruido salieron estrategias con Sharpe 7,8 dentro de muestra. No se probaron la generación
  genética, el walk-forward, Monte Carlo ni otros mercados.
- **Límites de los datos (ficha MinBTL):** bajo los supuestos de la ficha, con siete años de datos y unas 139 pruebas
  **efectivamente independientes**, el mejor Sharpe de un escenario nulo puede alcanzar un valor del orden de 1. Es una
  referencia aproximada del riesgo de selección, **no** un límite universal ni una garantía sobre resultados concretos;
  la búsqueda real se evalúa con la dependencia entre variantes y el procedimiento completo. De ahí que el recurso
  escaso sean los datos sin mirar y el tiempo real, no el cálculo.
- **Contaminación:** el curso (fechas vistas hasta al menos 2025-03), el entrenamiento de Claude (hasta 2026-06), la
  experiencia de Diego y lo ya examinado conocen parte del periodo que se sellará (B18, C22).
- **Trampas de SQX:** el banco desaloja por fitness sin avisar al llenarse (B21: `Builder/Results` = 7.003 estrategias
  con capacidad 1.000); posible recorte de métricas (B20: Ret/DD = 10 y factor de beneficio = 5 exactos); backtest solo
  con velas: un stop dentro de una vela es una suposición del simulador.

## 3. Principios

**P1. Dos unidades distintas.**
- **Unidad de decisión económica:** la cartera que de verdad operaríamos (costes, riesgos, pesos, ejecución). Buscamos
  varias ventajas modestas y poco relacionadas, netas de costes, no una estrategia milagrosa.
- **Unidad de registro:** cada hipótesis, estrategia, configuración, combinación, peso o ajuste probado. Que al final
  exista una cartera no reduce la búsqueda a un experimento.
- **Diversificación medida** (correlaciones, contribución al riesgo, amplitud efectiva), no contada por número de
  mercados. **No hay mínimo de mercados.** La ley fundamental (IR ≈ IC·√B) es una guía, no una garantía: contar
  instrumentos no es contar apuestas independientes.

**P2. Toda herramienta demuestra lo que aporta.** SQX, Python y la IA compiten contra una **referencia sencilla** (C20)
con el mismo presupuesto, costes y control nulo. Si la vía compleja no rinde más, no se paga su complejidad ni su
licencia (C21). La IA se compara con y sin IA (C7).

**P3. El embudo se calibra antes de decidir con él.**
1. **Dos controles complementarios:** *ruido sin ventaja*, con **varios modelos nulos** (al menos uno con agrupación de
   volatilidad y dependencia temporal), mide cuánto aprueba el proceso por azar (no demuestra que nunca habrá falsos
   positivos en datos reales); *ventaja sembrada* mide si el proceso encuentra ese tipo y tamaño de ventaja (no que
   encontrará cualquier ventaja).
2. **Tamaño sembrado:** el principal es la **ventaja neta mínima que justificaría operar tras costes**, más una escala
   de tamaños menores y mayores para ver dónde deja de detectar. El protocolo explica **cómo se construye** la ventaja
   sembrada y sus limitaciones, para no sembrar algo que el motor detecta solo porque comparte lo que busca.
3. **Proceso completo:** generación, filtros, retoques humanos y de la IA, selección y construcción de la cartera. Los
   falsos positivos se miden también **a nivel de cartera**.
4. **Desarrollo y aceptación separados.** Un juego de controles sirve para desarrollar; otro, solo para aceptar la
   versión final. Siempre que sea viable, el de aceptación difiere del de desarrollo **no solo en las semillas**, sino
   también en familias de modelos nulos, parámetros o condiciones que no hayan intervenido en el ajuste. Las semillas
   se fijan antes de ejecutar y los resultados quedan ocultos hasta la aceptación. La independencia y la
   representatividad de los modelos nulos se **justifican por escrito**; no se presumen por cambiar de semilla. Si se
   ajusta el proceso tras mirar el juego de aceptación, ese juego deja de valer y hace falta otro nuevo.
5. **Dos exámenes:** rechazar el ruido con una tasa baja y detectar la ventaja sembrada económicamente relevante con
   potencia suficiente. Los niveles se fijan en el protocolo de la fase 1, antes de ejecutar.

**P4. Todo cuenta.** Cada variante, combinación, peso y retoque es una prueba (reglas 7 y 8). Para cada candidata el
registro guarda quién la propuso (Diego, Claude, otra IA, SQX), cuántas variantes hubo, cuánto costó y qué filtro la
descartó (B14, C1); se conservan los resultados de todas las estrategias probadas (C13). Las variantes no son pruebas
independientes: la corrección por selección considera la dependencia entre resultados y el procedimiento, no solo su
número.

**P5. Las ventajas publicadas son hipótesis, no recetas.** Tendencia, reversión, efectos horarios, carry y ajuste por
volatilidad se investigan como familias. Ninguna rentabilidad institucional se importa como expectativa: la ventaja
tiene que sobrevivir a **nuestros** instrumentos, datos, costes, tamaño de cuenta y ejecución. No se atribuye ventaja
al carry hasta medir el resultado neto de los swaps realmente aplicables (B5), su variabilidad y la ejecución. Las
ideas humanas o de IA llevan la marca "posible conocimiento posterior" (C22).

**P6. Los costes deciden el terreno de juego.** Antes de investigar un instrumento, su ficha C12 (procedencia,
cobertura, huecos, reloj real, volumen, spread, comisión, swap, deslizamiento). Mercados y plazos se eligen por
viabilidad tras costes y diversificación medible.

**P7. Los criterios se fijan antes y no se mueven.** Estadístico, estimación de incertidumbre (con dependencia
temporal), tamaño de muestra, umbral y decisión que permite tomar se fijan antes de mirar los resultados de cada
prueba. t > 3, DSR y PBO son herramientas, no números por autoridad (C14: no se usan como objetivo de búsqueda).
Cualquier cambio posterior exige una versión nueva del protocolo, registrada como cambio de proceso y justificada;
**nunca** se cambia un umbral porque la candidata no lo pasó. Corregir un defecto metodológico o factual demostrado
sí está permitido, por esta vía.

**P8. Examen sellado: una vez y con todo congelado.** Se examina la cartera que operaríamos, congelada con hashes antes
de abrir (estrategias, pesos, rebalanceo, límites de riesgo, costes, reglas de retirada; C16; con varias candidatas,
corrección múltiple). Si falla, no se repesca. Un bloque abierto **deja de ser virgen para siempre**: puede servir
para investigar, pero no vuelve a presentarse como prueba independiente; una evaluación nueva exige datos o un periodo
genuinamente nuevo, con separación suficiente. El acceso a `data/sealed/` sigue la regla dura 1.

**P9. Tres etapas de evidencia antes del dinero de verdad.**

| Etapa | Qué demuestra | Qué no demuestra |
|---|---|---|
| Backtest y examen sellado | Evidencia histórica que supera los controles | Que se pueda ejecutar |
| Prospectiva simulada (demo o equivalente; VPS si hace falta) | Señales a tiempo, reglas respetadas, resultados coherentes con lo esperado | Ejecución real, deslizamiento, financiación |
| Capital real pequeño | Ejecución, deslizamiento, swaps y costes reales compatibles con la hipótesis | Que siga funcionando siempre |

Duración, observaciones mínimas y criterios de permanencia se derivan antes de cada etapa. Una buena demo **no**
autoriza por sí sola el dinero real. La VPS sirve para incubar candidatas congeladas, no para minar más.

**P10. Andamiaje congelado.** Ningún control ni herramienta nueva sin amenaza concreta, prueba que demuestre el fallo y
criterio de aceptación (A6). El laboratorio no puede convertirse en el proyecto (revisión 10).

**P11. Referencias económicas, no reglas automáticas.** La cartera se compara con su referencia sencilla de la misma
familia y con una alternativa pasiva **acorde a su exposición y riesgo** (un índice mundial no basta para juzgar una
estrategia EURUSD apalancada), mirando por separado rentabilidad neta, riesgo, drawdown, apalancamiento, capital
inmovilizado, correlación, costes, impuestos, horas y coste de oportunidad (A7). No batir al índice no obliga a parar
si hay un beneficio de cartera **medible tras costes**; una correlación baja no basta.

**P12. Integridad temporal: ningún resultado compensa una fuga.** Toda señal, entrada, salida y decisión debe poder
reconstruirse solo con la información disponible en ese instante. Antes de aceptar un resultado se comprueban, según
el caso: cierre de velas, alineación señal–operación, zonas horarias y cambios de horario (en SQX la zona es solo una
etiqueta: B1, B4), datos faltantes y calentamiento (B1), precios ejecutables, suposiciones dentro de la vela
(precisión del backtest), operaciones solapadas y costes. Lo comprobable se comprueba con pruebas, no con la promesa de
una herramienta; el banco de errores sembrados C11 incluye fugas de futuro y desfase de vela. **Un fallo de integridad
invalida la evaluación afectada**; DSR, PBO, walk-forward y Monte Carlo no lo sustituyen. **No se amplía la búsqueda
con un fallo de integridad abierto.**

**P13. Presupuesto por fase y criterio de parada.** Antes de cada fase: la pregunta que responde, su presupuesto
máximo (dinero, horas humanas, horas de cálculo, llamadas de IA, datos que gasta) y el resultado que permite seguir; lo
gastado se registra (A3). Desarrolla la 0003 v6 §3 (presupuesto escalonado, piloto A1b, causas de abandono, tres
objetivos A7); no la sustituye. **El gasto ya hecho no es razón para seguir.** Si una puerta falla, no se amplían el
universo, la potencia ni la IA: se corrige el defecto concreto en una versión nueva comprobable, o se cierra esa línea.
El criterio de éxito no se reinterpreta después.

## 4. Fases y puertas

Cada puerta tiene dos salidas honestas: seguir, o corregir o parar con evidencia. Umbrales, muestras, plazos y
presupuestos se fijan **en el protocolo de cada fase, antes de ejecutarla**, nunca aquí por intuición.

| Fase | Qué se hace | Puerta para avanzar |
|---|---|---|
| **0. Rumbo y condiciones previas** | 0004 aceptada; A22 y decisiones del día en `PENDIENTES.md`. **B21:** exportar o archivar las 7.003 estrategias de `Builder/Results` con identificadores (hash) y metadatos; **leer o restaurar la copia en un lugar separado** y verificar recuento e integridad; ajustar la capacidad en una **copia de trabajo** de la plantilla y **probar** que una generación nueva no desaloja lo que se conserva; no reanudar la búsqueda hasta cerrarlo. **B20:** comprobar con casos conocidos (documentación y estrategia de métricas conocidas) si SQX recorta Ret/DD y factor de beneficio y si eso altera la ordenación o la selección | B21 y B20 cerrados con evidencia registrada |
| **1. Calibración** | Protocolo escrito y en git antes de ejecutar: modelos nulos de desarrollo y de aceptación (P3.4), construcción y tamaños de la ventaja sembrada, niveles de error y detección, presupuesto (P13) y condiciones que impiden escalar. **B19** implementado con tests de errores sembrados; comprobaciones P12 automatizables; **B14** (eventos tipados, registro de hipótesis) antes de la primera tanda que cuente. Se prueba el embudo del curso (genética, walk-forward, Monte Carlo, comprobación en otros mercados) **con el ciclo de IA dentro**, frente a la referencia sencilla, también a nivel de cartera | Supera **los dos exámenes** en el juego de aceptación sin mirar. Si no: defecto corregido en versión nueva o vía cerrada; no se escala |
| **2. Universo y costes** | **B18 ampliada:** la fecha de inicio del sellado sale de revisar **todas** las fuentes de contaminación (curso, conocimiento de Diego, entrenamiento de Claude, pruebas y resultados ya examinados, exposición por herramientas o IA), no se elige antes y se justifica después; regla de la 0003 v6 §1 como mínimo. Protocolo de sellado aprobado. Descarga de datos (con la vía verificada, A22). Fichas **C12**, empezando por EURUSD (0003); otros mercados si se justifican | Universo viable tras costes, diversificación efectiva medida y sellado hecho |
| **3. Búsqueda y cartera** | Piloto con presupuesto fijado (A1b): SQX, referencia sencilla y vía por hipótesis con igual presupuesto y costes; todas las pruebas registradas; cartera construida con reglas previas y congelada | Supera a la distribución nula y a la referencia, con la búsqueda contada (C15) |
| **4. Examen sellado** | La cartera congelada, una sola vez (P8) | Criterio fijado antes, muestra suficiente; si no, INCONCLUSO o rechazada (C9) |
| **5. Prospectiva simulada** | Ejecución congelada en entorno compatible y verificado; código MT compilado (A11) | Coherente con lo esperado según criterio previo |
| **6. Capital real o externo** | Capital propio pequeño (tope fijado por Diego antes de H5, 0003 v6) o asignación externa si es elegible | Ejecución real compatible con la hipótesis; costes, riesgos, impuestos y elegibilidad verificados |

## 5. Escalar (la "máquina")

Escalar es el objetivo (más estrategias, más mercados, IA por API, ejecución desatendida, VPS), pero **solo después de
superar la fase 1** y sin fallos de integridad abiertos (P12). Cada ampliación se justifica por su valor informativo o
económico frente a su coste (P13) y por su coste por candidata válida (C21). Lo de `PENDIENTES.md` §D sigue sin
construirse hasta que se cumpla su condición.

## 6. Asuntos abiertos que toca esta decisión

- **A22 (nuevo): vehículo y datos desde España.** No bloquea la fase 1; el laboratorio debe poder avanzar sin Darwinex.
  Verificado el 2026-10-21 en fuentes oficiales:

  | Cuestión | Estado |
  |---|---|
  | Suscribirse a **Darwinex Zero** desde España | **Documentación oficial favorable:** "sin restricciones geográficas", con posibles restricciones de pago por país (darwinexzero.document360.io, "Who can subscribe?", actualizada 2024-01-30). Falta comprobar el alta y el pago |
  | Operar en Zero (capital nocional) y DarwinIA | El programa existe: capital **nocional**, 15 % de comisión de éxito, requisitos de equity (en la cuenta, no necesariamente depósito propio) y de correlación (help.darwinex.com/darwinia). Falta verificar las condiciones aplicables |
  | Demo de MetaTrader en Darwinex | **NO** para residentes fiscales en España (help.darwinex.com, "How to open and use demo trading accounts") |
  | Cuenta real minorista de Forex/CFD en Darwinex (o migrar de Zero) | Restricción documentada: Sapiens Markets no da de alta a minoristas residentes en España desde el 2024-07-31. Requiere respuesta específica |
  | Datos de Darwinex para SQX (¿exigen cuenta?) | **INCONCLUSO** |

  Afecta a la 0003 v6 (bloque "Prospectivo: Demo"), a C12 y a las fases 5–6. Diego pregunta por escrito (Claude prepara
  el texto).
- **A12, licencia:** Diego, 2026-10-21: no hay prisa; la prueba se puede renovar (no verificado) y, si el proyecto lo
  justifica, se paga. Se decide con la evidencia de la fase 1.
- **Mercados:** EURUSD primero (0003, A19); ampliar es la dirección acordada (Diego), en la fase 2 y con su puerta.

## 7. Qué NO decide

No promete que una cartera vaya a ser rentable; no fija umbrales, plazos, muestras ni presupuestos; no autoriza
comprar, operar en real ni abrir `data/sealed/`; no reabre la pausa de revisiones (A21) salvo B13; no cambia las reglas
duras de `CLAUDE.md`.

## 8. Fuentes

Internas: registro n.º 1–222; `h0/b1_resultados.md`; `h0/b17_resultados.md`; fichas DSR, PBO y MinBTL
(`conocimiento/fundamentos/`); 0003 v6; revisiones 01–15. Externas citadas, **cada una se comprueba con su ficha antes
de sostener una decisión**: Grinold y Kahn; Bailey y López de Prado; Harvey, Liu y Zhu; Chen (*Management Science*,
2025, "Do t-Statistic Hurdles Need to be Raised?"); Hurst, Ooi y Pedersen; Moreira y Muir y la crítica posterior;
ayuda oficial de Darwinex y de Darwinex Zero. **No verificadas y no usadas:** "Harvey, Sancetta y Zhao, NBER 2026" y un
"preprint de agosto de 2026 sobre estrategias generadas con IA".

## Historial de esta decisión

| Versión | Cambios | Origen |
|---|---|---|
| 1 | Cartera en vez de estrategia; dos motores; embudo calibrado; incubadora; andamiaje congelado. Con correcciones: sin mínimo de 8–10 mercados; la cartera no borra la búsqueda; ventajas publicadas como hipótesis; t > 3 no es mágico; el índice es referencia, no regla de parada | Diego y Claude; revisión 13 |
| 2 | P12 (integridad temporal); P13 (presupuesto y parada); desarrollo y aceptación separados; ventaja sembrada ligada al mínimo económico; falsos positivos de cartera; dos unidades; bloque abierto deja de ser virgen; tres etapas antes del dinero real; carry y referencia económica neutrales | Revisión 14 |
| 3 | **Aceptada.** Aceptación independiente también en familias de modelos nulos, no solo semillas; construcción de la ventaja sembrada explicada; B17 (p = 0,99) y MinBTL (139) redactados sin ambigüedad; B21 con copia verificada y prueba de no desalojo; A22 actualizado con la página oficial de Zero; B18 ampliada a todas las fuentes de contaminación; P7 permite corregir defectos demostrados por la vía versionada | Revisión 15; Diego ("me parece perfecto", "cerrarlo y guardarlo definitivamente") |
