# Estado del proyecto y punto de continuación

**Actualizado: 2026-10-22.** Tras la segunda sesión local (21-10), dos días de conversación de rumbo **sin
experimentos nuevos**: decisión 0004 y diseño cerrado de la fase 1. Último registro: **n.º 222**.
Este documento es el **punto de entrada al reiniciar una sesión**. Si algo aquí contradice a un archivo más específico,
manda el más específico (estado de H0: `h0/ficha.md`; asuntos abiertos: `docs/decisiones/PENDIENTES.md`; hechos:
`registry/experimentos.jsonl`), y se corrige este documento.

## 0. Al empezar una sesión nueva (en este orden)

1. Leer `CLAUDE.md` (reglas duras y objetivo), **este documento**, `aprendizaje/diario.md` (errores ya vistos) y
   `docs/decisiones/PENDIENTES.md` (todo lo abierto).
2. Comprobar el banco de trabajo:
   `python -m unittest discover -s tests` (41/41) · `python .claude/hooks/guardian.py --autotest` (44/44) ·
   `PYTHONPATH=src python -m lab verificar` (222 entradas o más) · `python -I h0/configs/comprobar_evidencias.py`
   (0 fallos) · `git status` limpio · `git fetch` y sin divergencias con `origin/claude/proyecto-2026-fps66g`.
3. Si la sesión es de terminal: abierta con `claude_lab.cmd` (la cabecera no debe decir "API Usage Billing"; si pide
   iniciar sesión, `/login` con la suscripción).
4. Mirar si Diego ha resuelto algo de la sección 6 y seguir por la sección 7.

## 1. Objetivo y fase

- **Objetivo** (`CLAUDE.md`, A5 adoptado el 2026-10-21): un laboratorio de investigación cuantitativa **para trading
  algorítmico**, integrado (SQX, Python, IA y datos como herramientas que deben demostrar lo que aportan), para
  descubrir, validar y explotar ventajas netas de costes, o demostrar con evidencia que no las hemos encontrado y
  detenernos. **Concluir "no hay edge" es un resultado válido.**
- **Decisión vigente:** 0003 **v6, aceptada** (reparto de datos por regla, EURUSD, 0 € reales hasta superar la demo,
  presupuesto escalonado con piloto, referencias preregistradas, control negativo, tres objetivos en el abandono).
- **Rumbo: 0004 v3, aceptada** (`docs/decisiones/0004-rumbo-medir-antes-de-escalar.md`): medir antes de escalar.
  Cartera como unidad de decisión (cada prueba como unidad de registro); SQX, IA y Python frente a una referencia
  sencilla; embudo calibrado con ruido y con ventaja sembrada (controles de desarrollo y de aceptación separados);
  integridad temporal (P12) y presupuesto por fase (P13); fases 0–6 con puertas. Escalar (millones de estrategias,
  IA por API, VPS, muchos mercados) es el objetivo de Diego, **después** de superar la fase 1.
- **Visión de Diego (2026-10-21): "la máquina", llevarla al techo y ser mejor que nadie.** Tres capas que casi nadie
  junta: (1) **minería masiva** (SQX, VPS, muchos mercados); (2) **ciclo de mejora con IA** (Claude Code y, si se
  demuestra útil, por API: "cambia este indicador, ¿qué pasa si…?", preparar tandas, leer resultados); (3) **un medidor
  de errores dentro** (controles nulos, ventaja sembrada, todo contado). La ventaja que buscamos es la de proceso: con
  la capa 3, las capas 1 y 2 dejan de fabricar estrategias bonitas y pasan a encontrar lo que hay. La fase 1 no está
  para tumbar la idea: da permiso para escalar; si el embudo no distingue a la primera, **la IA tiene que demostrar que
  sabe mejorarlo** (iteraciones contadas, con controles de aceptación sin mirar). Ruta de escalado: C23 en
  `PENDIENTES.md`. Posibilidad pequeña pero real; no se promete, se persigue en serio.
- **Correspondencia entre las fases de la 0004 y los hitos de la hoja de ruta** (revisión completa del 2026-10-22; las
  fechas de la 0003 §3 siguen siendo hitos de revisión, no obligaciones):

  | Hito (hoja de ruta) | Dónde cae en la 0004 |
  |---|---|
  | H0 ficha técnica | Fase 0 |
  | H2 motor de validación (EDGE con incertidumbre) | Fase 1: B19 implementado y probado en la calibración |
  | H3 IA analista frente a sin IA (0001) | Fase 1, con datos sintéticos: el ciclo de IA es un brazo del embudo, comparado con el mismo embudo sin IA |
  | H1 reconstrucción independiente en Python | Comprobación P12, **antes del piloto (fase 3)**: reproducir operación a operación algunas estrategias de SQX |
  | H1 puente a MetaTrader (compilar y ejecutar) | **Antes de la fase 5** (A11; para compilar vale cualquier MetaTrader de demo, no hace falta Darwinex) |
  | Veredicto VIABILIDAD por vehículo | Fases 5–6, con el vehículo que salga de A22 |
  | H4 demo · H5 real · H6 panel | Fase 5 · fase 6 · después |
- **Fase: H0 (viabilidad técnica), casi cerrada = fase 0 de la 0004.** Siguiente: fase 1 (calibración), **no antes**
  de cerrar la fase 0 (sección 7).

## 2. Qué está demostrado (H0) y qué no

| Tarea H0 | Estado | Evidencia clave |
|---|---|---|
| 0. Banco de trabajo | SÍ | n.º 5–8; agujero de PowerShell cerrado (A9, n.º 90) y comprobado con llamadas reales (B3, n.º 91) |
| 1. `sqcli -h`, build | SÍ | 145.3191, firma válida (n.º 9–10) |
| 2. Límites de la prueba | NO en lo probado | WFO y What If funcionan (n.º 57–71); optimización secuencial INCONCLUSA |
| 3a–3d. Generar, backtest, exportar | SÍ | n.º 16–33, 34–48 |
| 3e–3f. Código MT4/MT5 | Exporta SÍ · compila INCONCLUSO | n.º 27–31; no hay MetaTrader |
| 4. Reproducir backtest | SÍ | 1.353 operaciones idénticas, control negativo (n.º 43–56) |
| 5. Datos de Darwinex | Metadatos SÍ; descarga bloqueada por protocolo | n.º 87–88 |
| 6. Pasos manuales | Uno: cerrar la interfaz de SQX | Tareas 3–7 |
| 7. Experimento completo | SÍ: 54,7 s | n.º 72–86 |
| B1. Exportar/importar por fechas | **NO por criterios; causas corregidas (B1-bis SÍ)** | n.º 93–148, `h0/b1_resultados.md`: precios idénticos; volumen > 2³¹−1 recortado al importar; sin margen de calentamiento se pierden las primeras operaciones (con un mes, 1.277 idénticas); zona horaria = solo etiqueta |
| B11. Piloto de transcripción | SÍ | n.º 92: *medium* + fotogramas; ≈ 50 h de CPU para el curso entero |
| B17. Control negativo de la búsqueda | **D1: el embudo de filtros no distingue el real del ruido** | n.º 149–222, `h0/b17_resultados.md`: sin costes, el embudo aprueba el 0,8 % de estrategias en datos sin ventaja y el real no lo supera (p = 0,99); con costes, 0,1 %. "Pasa los filtros" es compatible con el azar |

**No demostrado (y no es objetivo de H0):** ninguna ventaja de mercado; reconstrucción independiente de SQX; costes
reales de Darwinex Zero; reloj real y volumen de los datos de Darwinex; aislamiento real del bloque sellado; corrección
por selección sobre el universo completo; **que SQX distinga ventaja de ruido** (B17 dice que, con generación aleatoria y
un embudo típico en el USDCHF quemado, no; falta probarlo con el motor y los filtros del piloto).

## 3. Estado exacto del PC de SQX (no está en git; comprobar al reiniciar)

- **SQX:** `C:\StrategyQuantX145`, *StrategyQuant X **Pro** Build 145 (Trial license)*, build **145.3191 de
  desarrollo**, **la prueba caduca el 2026-11-02** (Diego: se usa la prueba y se decide después con evidencia, A12).
  `sqcli.exe` SHA-256 `afa68ccb…a4f`. Interfaz y CLI no pueden funcionar a la vez: **cerrar la interfaz** antes de cada
  tanda.
- **Carpeta de intercambio:** `C:\StrategyQuantX145\user\lab_h0\` (plantillas, órdenes `-run`, salidas; B1 en
  `lab_h0\b1\`). Las rutas relativas de `sqcli` se resuelven **desde `C:\StrategyQuantX145`**.
- **Proyectos:** Builder (último: n.º 219–220, tras B17) y Retester (último: n.º 146–147, tras B1-bis) **restaurados y
  comprobados** a su configuración original (0 diferencias en todos los bloques).
  Originales en `h0/configs/*_original_145.3191.cfx`.
- **Bancos** (todo lo nuestro es familia `H0-proceso`, datos quemados): **`Builder/Results` = 7.003** (23 de las 40 de
  H0 + 28 de la calibración + 949 de la v1 de B17 + 3.001 de la v2 + 3.002 de la v3; contado el 2026-10-21); **ojo (B21): la capacidad restaurada es 1.000 y la próxima
  generación desalojará sin avisar** → guardar el banco antes de volver a usar el Builder. `Builder/H0_T7` y
  `Builder/H0_archivo` vacíos; `Retester/H0_USDCHF` = 10; `Retester/H0_T7` = 10; `Retester/H0_B1` = 10;
  `Retester/Results` = 7 ejemplos de SQX (**no tocar**). **Pérdida registrada:** SQX desalojó 17 de las 40
  estrategias de prueba de H0 durante la v1 de B17 (8 sin copia en otra carpeta; n.º 181).
- **Símbolos de prueba** (datos quemados, ventana 2023.01.02–2024.10.30): `USDCHF_B1` (importado, EETUS),
  `USDCHF_B1_TZ` (etiqueta UTC, control C2), `USDCHF_SINT1` y `USDCHF_SINT2` (sintéticos sin ventaja de B17, semillas
  1 y 2). No se han borrado. Archivos de B1 y B17 en `lab_h0\b1\` y `lab_h0\b17\`.
- **Datos quemados** (decisión 0002): `USDCHF_M1_dukas`, 2023-01-01 → 2024-10-30, zona "(EST+07) New York, US DST"
  (`EETUS`). Solo para pruebas de proceso; **USDCHF no será el primer mercado de investigación**.
- **Python 3.14.6** del laboratorio; `pdfplumber` sí; **numpy, pandas y scipy NO** (A18). `pip install -e .` no hecho:
  usar `PYTHONPATH=src python -m lab …`. El transcriptor vive en **otro** entorno (abajo).
- **Git:** sin identidad configurada; commits con `git -c user.name=Claude -c user.email=noreply@anthropic.com commit
  -F <archivo>` (A13). `core.autocrlf=true` (por eso `.gitattributes`: evidencias byte a byte, registro y `.sh` en LF,
  `.cmd` en CRLF). Las líneas 1–2 del registro tienen CRLF solo en la copia de trabajo (sin efecto).
- **`ANTHROPIC_API_KEY`**: es de Diego y se queda (A10), pero **el laboratorio no la usa**: abrir siempre con
  **`claude_lab.cmd`**. La aplicación de escritorio no la lee.
- **Carpetas privadas fuera del repositorio** (solo en este PC; **copia de seguridad: A14**): `h0/evidencias_privadas/`
  (dentro del proyecto, ignorada por git); `C:\Users\SERVILAB\Documents\LAB_PRIVADO_CURSO\` (auditoría del curso,
  inventario, transcripciones, fotogramas, tabla de fechas de B18, herramientas, `.venv_transcripcion` con faster-whisper
  1.2.1 y PyAV 18.1.0, modelos small y medium) y `C:\Users\SERVILAB\Documents\LAB_BIBLIOTECA\papers\`.
- **Curso de Imox** (comprado por Diego, A8): `C:\Users\SERVILAB\Desktop\curso de trading algoritmico\IMOX
  TRADING.zip.001…008` (14,8 GB, 85 vídeos sin comprimir, **28,7 h**; empaquetado el **2026-01-12**). La carpeta
  `IMOX TRADING.zip` del escritorio es una extracción parcial (8 vídeos). El guardián bloquea comandos que nombren esa
  ruta (`zip`, B9): se usan los scripts de `LAB_PRIVADO_CURSO/herramientas/`, que llevan la ruta dentro. Nada del curso
  va a GitHub (tampoco las cifras de sus filtros).
- **Repositorio de GitHub público** (`LaRuinaDeMago/TradingAlgoritmico`, rama `claude/proyecto-2026-fps66g`); A4.

## 4. Cómo se trabaja aquí (procedimiento probado)

1. **Todo comando de SQX por el ejecutor:** `PYTHONPATH=src python -m lab ejecutar --nombre <n> --version-sqx
   "145.3191-dev" [--datos …] [--costes …] --descripcion "…" -- "C:/StrategyQuantX145/sqcli.exe" <orden>`. Las
   comparaciones y análisis en Python también pasan por el ejecutor (`--version-sqx N/A`) para quedar registrados.
   Funciones listas para tandas: `h0/configs/b1_funciones.sh` (commit antes y después de cada orden).
2. **Commit antes de cada ejecución** (si no, sale `"sucio": true`) y **no tocar el repositorio mientras corre** una tanda.
3. **Criterios antes de ejecutar:** plan con criterios de aceptación y controles negativos, en git, **antes** de la
   primera orden (B1). Si un criterio falla, no se redefine: se diagnostica aparte y, si hace falta, se fija un criterio
   nuevo como cambio de proceso, escrito antes de volver a probar (B1-bis).
4. **No fiarse del "OK" ni del código 0**: leer la evidencia entera y comprobar el efecto real (recuentos, archivos,
   reexportar la configuración y compararla con `h0/configs/comparar_bloque.py`).
5. **Antes de cada subida:** tests, `lab verificar`, `comprobar_evidencias.py`,
   `python -I h0/scripts_sesion_2026-10-21/barrido_privacidad.py` (datos privados y contenido del curso en lo que va a
   salir), nada privado ni PDF ni código MT en git, `git fetch` antes de `push`.
6. **Trampas de SQX ya vistas:** órdenes asíncronas (`-databank action=load` suelta no espera; usar `-run` con
   `synctofiles`); **el Builder escribe siempre en `Results`**; **`-databank action=move` corta y no pega: no usarlo**;
   SQX reutiliza nombres de estrategia (identificar por hash); ~22 s por arranque; la consola va 2 h adelantada; las
   plantillas de fábrica no son homogéneas (al Retester le falta `<Swap>`); `engine=MetaTrader4`, no `mt4`;
   `-sourcecode` existe aunque `-h` no lo liste. **De B1:** la importación **exige** `format`; `-symbol action=list
   csv=true` no imprime nada (sin `csv`, sí); el volumen importado se recorta a 2³¹−1; la zona horaria al importar es una
   etiqueta; SQX ajusta el inicio del backtest al primer dato del símbolo; los CSV de operaciones llevan ticket, símbolo
   y saldo (comparar con `b1_diagnostico_operaciones.py`). **De B17:** el banco tiene capacidad
   (`<Rankings><MaxStrategies>`, 1.000 de fábrica) y, lleno, **desaloja por fitness sin avisar** (fijarla en la plantilla
   y comprobar recuentos antes y después); genera alguna más de las pedidas (7 hilos); descarta las estrategias "con
   problemas" antes de contarlas; las exportaciones del banco tardan más cuanto más grande es (de 22 a 74 s); posible
   recorte de métricas (Ret/DD 10, factor de beneficio 5: B20); un tramo fuera de muestra se añade con
   `<OutOfSample><Range dateFrom= dateTo= type="oos"/>`.
7. **Falsos positivos del guardián** (no rodearlo: usar la vía sancionada): en un comando que nombra `registry` o
   `.claude`, evitar "del", `>`, `>=`, `2>&1`, `->`, `<…>`; los textos que contienen órdenes peligrosas literales
   también saltan; "zip" en rutas, `find` y `.find(` saltan. Vía sancionada: **commit con `-F archivo`**, código en un
   archivo escrito con Write, resultados largos con `--resultado archivo.json`, separar comandos.
8. **Nunca:** leer `data/sealed/`, operar en real, comprar, borrar estrategias o datos de Diego, modificar el guardián,
   decidir por Diego (si delega, se escribe como decisión suya con la recomendación y el motivo de Claude).

## 5. Mapa de documentos

| Qué | Dónde |
|---|---|
| Reglas duras, objetivo y estilo | `CLAUDE.md` |
| Hoja de ruta (PDF de Diego y transcripción, con nota de desfase) | `docs/hoja_de_ruta*.{md,pdf}` |
| Decisiones: 0001 (IA y herramientas), 0002 (datos quemados), **0003 (ACEPTADA v6)**, **0004 (ACEPTADA v3: rumbo, principios P1–P13, fases 0–6)** | `docs/decisiones/` |
| **Índice único de asuntos abiertos** (A: Diego · B: técnico · C: requisitos futuros · D: no construir) | `docs/decisiones/PENDIENTES.md` |
| Protocolo de sellado de Darwinex (BORRADOR; manda la 0003 v6; con los requisitos de B1) | `protocols/2026-10-20_sellado_darwinex.md` |
| Revisiones externas 01–12 con la respuesta de Claude | `docs/revisiones/` |
| Prompt de auditoría maestra (para una sesión independiente) | `docs/auditoria/prompt_auditoria_maestra.md` |
| Mantenimiento del guardián (aplicado A9; procedimiento para el siguiente) | `docs/mantenimiento/` |
| Ficha H0 | `h0/ficha.md` |
| B1: plan con criterios previos y resultados | `h0/b1_plan_integridad.md`, `h0/b1_resultados.md` |
| B16: licencia frente al calendario (precios, inconclusos, texto para el soporte) | `h0/b16_licencia_calendario.md` |
| B17: control negativo (plan con enmiendas v2, v2.1 y v3, y resultados) | `h0/b17_plan_control_negativo.md`, `h0/b17_resultados.md` |
| Fase 1 (calibración del embudo, B17 mejorado): diseño BORRADOR v0 | `protocols/2026-10-22_fase1_calibracion_BORRADOR.md` |
| Plantillas, scripts de preparación, tandas y comparadores | `h0/configs/` |
| Guiones exactos de las tandas del 2026-10-20 | `h0/scripts_sesion_2026-10-20/` |
| Guiones auxiliares del 2026-10-21 (pruebas del lanzador, lector del registro) | `h0/scripts_sesion_2026-10-21/` |
| Evidencias públicas (redactadas) | `h0/evidencias/` |
| Base de conocimiento (3 fichas de papers con verificaciones) | `conocimiento/` |
| Diario de lecciones, glosario, lección 01 | `aprendizaje/` |
| Núcleo Python y tests | `src/lab/`, `tests/` |
| Lanzador de Claude Code sin la clave API | `claude_lab.cmd` |

## 6. Decisiones de Diego (detalle en `PENDIENTES.md`, sección A)

**Cerradas el 2026-10-21** (varias por delegación explícita en el criterio de Claude): A1 (0003 v6), A2 (0 € reales
hasta superar la demo), A3 (horas variables, se registran), A5 (objetivo), A8 (curso comprado), A9 (guardián), A10
(clave API: se queda, el laboratorio no la usa), A17 (transcriptor), A19 (EURUSD), A20 (rigor con presupuesto de tiempo
por fase), A21 (pausa de revisiones externas hasta el piloto). **Por la tarde:** 0004 aceptada en v3; varios mercados
como dirección; la caducidad de SQX deja de ser fecha límite (se puede renovar la prueba; no verificado).
**Abiertas:** **A23 ampliar USDCHF quemado para calibrar** · **A22 vehículo y datos desde España** (Diego pregunta por escrito a Darwinex; no bloquea la fase 1) · A12
licencia (se decide con la evidencia de la fase 1) · A1b cifras del piloto
(propuestas en la 0003) · A4 repositorio público/privado · A6 regla de proporcionalidad · A7 cifras del criterio
económico · A11 MetaTrader · A13 identidad git · A14 copias de seguridad · A15 protección de rama · A18 numpy/pandas/scipy.

## 7. Siguiente paso (fases de la 0004; poco a poco, una puerta cada vez)

**Regla de trabajo acordada con Diego (2026-10-21): medir, no escribir.** La 0004 es un mapa y un conjunto de
prohibiciones, no una obra que construir antes de empezar.
1. **Ni documentos de diseño nuevos ni revisiones externas** hasta tener el resultado de la fase 1 (solo se corrige un
   defecto demostrado, por la vía de P7). El diseño de la fase 1 está cerrado (revisiones 13–17).
2. **Cada paso, en su versión mínima que responde la pregunta**, reutilizando lo que hay (`b17_sintetico.py`,
   `b17_analizar.py`, plantillas de H0, los `.cfx` del curso).
3. **Plazo cerrado para la fase 1**, fijado en su protocolo; si se supera, se para y se revisa por qué.
4. **Antes de hacer algo nuevo:** ¿qué error evita y qué decisión cambia? Si no hay respuesta, no se hace (P10, A6).
5. **Antes de dar un plazo o una cifra:** buscar en el registro lo ya medido y decir qué falta por medir.

Lo que no está en nuestra mano: que exista una ventaja, el acceso a Darwinex (A22) y la calidad real de datos y
ejecución. **Lo medido** (B17, n.º 204–222): 1.000 estrategias aleatorias en 74–87 s; un brazo completo en 5–6 min.
**Sin medir:** genética, walk-forward, Monte Carlo, retest de mayor precisión y 22 años de datos (A23). La VPS para
calcular entra cuando una medición diga que el cálculo frena (C23 c); la VPS como incubadora, en la fase 5.

### Lo que depende de Diego (cuanto antes)

1. **A14, copias de seguridad:** `Documents/LAB_PRIVADO_CURSO/` y `h0/evidencias_privadas/` solo existen en este PC;
   copiarlas a un sitio suyo y comprobar que se abren.
2. **A12, renovar la prueba de SQX** (caduca el **2026-11-02**): pedirla ya, sin suponer que se renueva sola. Claude
   prepara el texto (B16).
3. **A22, Darwinex:** enviar la consulta (Claude prepara el texto).
4. **A23:** ¿ampliar USDCHF quemado a 2003–2024 para la calibración? (más operaciones y regímenes; ~10× más tiempo de
   cálculo; no gasta datos de investigación).
5. **B13, auditoría independiente:** la tarjeta `task_fe8910bc` caduca hacia el **2026-10-27**; empezarla o, si
   caduca, volver a proponerla con `docs/auditoria/prompt_auditoria_maestra.md`.
6. Cerrar la interfaz de SQX antes de cada tanda por línea de comandos.

### Lo que hace Claude, en orden

**Fase 0 – condiciones previas:**
1. **B21:** plan corto con criterios en git antes de la primera orden (como B1); copiar las 7.003 estrategias de
   `Builder/Results` con hash y metadatos; leer o restaurar la copia en otro lugar y verificar recuento e integridad;
   ajustar la capacidad en una **copia de trabajo** de la plantilla y **probar** que una generación nueva no desaloja
   lo conservado.
2. **B20:** ¿recorta SQX Ret/DD y factor de beneficio? Documentación y una estrategia de métricas conocidas; ¿afecta a
   la ordenación o la selección?
3. Textos para Diego: renovación o ampliación de SQX (B16) y consulta a Darwinex (A22).
4. **B22, curso a fondo:** primera tanda de transcripción (*medium* + fotogramas) en los huecos de CPU (hasta el 02-11,
   SQX tiene prioridad); historiales públicos del autor.

**Fase 1 – calibración** (diseño cerrado en `protocols/2026-10-22_fase1_calibracion_BORRADOR.md`):
5. **Construir lo mínimo:** nulos N2 y N3 y siembra S1/S2 en `b17_sintetico.py` con tests; embudo C desde los `.cfx`
   del curso (cambiando solo símbolo, fechas, costes y capacidad); embudo L; análisis en el tramo de reserva.
6. **Medir un brazo completo** (genética + embudo C) y dimensionar N y R con ese dato.
7. **Escribir la v1** rellenando los huecos (B20, B21, B5, A23, B22 para lo que no esté en los `.cfx`, niveles,
   presupuesto, plazo) y subirla **antes** de ejecutar. B14 y B19 en su versión mínima antes de la primera tanda que
   cuente; probable A18 (numpy/scipy).
8. **Núcleo mínimo antes del 02-11** (C y L sobre N3 y S2 tamaño 1, R = 3), etiquetado **EXPLORATORIO**: con 0 carteras
   de ruido aceptadas en 3 réplicas, el límite superior de falsos positivos sigue siendo 63 %. Interpretación con la
   tabla fijada en el borrador §8.
9. **Calibración completa** si hay SQX y la medición lo permite (R según la precisión; ~30 réplicas por familia de
   aceptación para acotar en torno al 10 %), con el brazo con IA. Puerta: los dos exámenes de aceptación.
10. Decidir la siguiente inversión con esa evidencia: si hay diferencias informativas, ampliar; si no, investigar el
    motivo antes de añadir filtros, activos, API o infraestructura.

**En paralelo, sin chocar con mediciones de SQX:** B18 ampliada (B22 y las demás fuentes de contaminación); B15 + B9
(mantenimiento del guardián, lo abre Diego).

**Fase 2 en adelante:** protocolo de sellado → datos (vía verificada, A22) → fichas C12 → reconstrucción en Python (H1,
P12) → piloto con cartera (fase 3) → examen → MetaTrader y prospectivo (fase 5) → capital (fase 6). Detalle y puertas en
la 0004 §4; escalado de la máquina en C23.

## 8. Revisiones externas recibidas (vía Diego)

01 auditoría del curso y 0003 · 02 organización y fichas · 03 viabilidad para un particular · 04 ¿camino razonable? ·
05 laboratorio integrado · 06 enmiendas a 0003 · 07 base de conocimiento · 08 auditoría de diseño y prompt maestro ·
09 auditoría estática de un ZIP (cifras verificadas) · **2026-10-21:** 10 evaluación sincera (amplía A7, sugiere A21) ·
11 cambio de enfoque (referencias previas C20; Claude añade B17) · 12 diagnóstico con la v6 (B19; coste de B18; misión →
A5). Desde la 10, en formato corto por la pausa A21. **13–17** (2026-10-21 y 22): sobre el rumbo → 0004 v3 y el borrador de la fase 1, que queda cerrado
(`docs/revisiones/2026-10-21_13-16_revisiones_0004.md`); dos citas suyas no se encontraron y no se usan. Si vienen del mismo modelo, que coincidan no es evidencia
independiente.

## 9. Lo esencial aprendido (detalle en `aprendizaje/diario.md`)

El código 0 y los mensajes de éxito mienten; un resultado idéntico necesita control negativo, y un control negativo
puede estar mal diseñado (C2); un indicador mal elegido casi da una conclusión falsa; una cifra plausible no es una cifra
comprobada; registrar sin límite no controla el sobreajuste; con 7 años caben ~139 configuraciones independientes antes
de Sharpe 1 por azar; hay que guardar los resultados de **todas** las estrategias probadas; un periodo sellado dentro de
SQX no está sellado; lo que se ha visto (el curso, el conocimiento de Claude) no se puede sellar; "ignorado por git" no
es "privado"; la memoria y los resúmenes también se equivocan; los criterios se fijan antes y no se tocan después.
**De B17:** "pasa los filtros" es compatible con el azar (el embudo aprueba ruido al mismo ritmo que datos reales); la
referencia es una distribución nula simulada con los mismos costes, no el cero; una herramienta puede borrar datos en
silencio (el banco desaloja al llenarse): contar antes y después de cada paso.
