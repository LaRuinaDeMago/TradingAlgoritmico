# Estado del proyecto y punto de continuación

**Actualizado: 2026-10-21, tarde (segunda sesión local en el PC de SQX).** Último registro: **n.º 148**.
Este documento es el **punto de entrada al reiniciar una sesión**. Si algo aquí contradice a un archivo más específico,
manda el más específico (estado de H0: `h0/ficha.md`; asuntos abiertos: `docs/decisiones/PENDIENTES.md`; hechos:
`registry/experimentos.jsonl`), y se corrige este documento.

## 0. Al empezar una sesión nueva (en este orden)

1. Leer `CLAUDE.md` (reglas duras y objetivo), **este documento**, `aprendizaje/diario.md` (errores ya vistos) y
   `docs/decisiones/PENDIENTES.md` (todo lo abierto).
2. Comprobar el banco de trabajo:
   `python -m unittest discover -s tests` (29/29) · `python .claude/hooks/guardian.py --autotest` (44/44) ·
   `PYTHONPATH=src python -m lab verificar` (148 entradas o más) · `python -I h0/configs/comprobar_evidencias.py`
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
- **Fase: H0 (viabilidad técnica), casi cerrada.** Siguiente hito: H1 (puente SQX → MetaTrader y reconstrucción
  independiente), **no antes** de cerrar las condiciones previas de la sección 7.

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

**No demostrado (y no es objetivo de H0):** ninguna ventaja de mercado; reconstrucción independiente de SQX; costes
reales de Darwinex Zero; reloj real y volumen de los datos de Darwinex; aislamiento real del bloque sellado; corrección
por selección sobre el universo completo; que SQX distinga ventaja de ruido (B17).

## 3. Estado exacto del PC de SQX (no está en git; comprobar al reiniciar)

- **SQX:** `C:\StrategyQuantX145`, *StrategyQuant X **Pro** Build 145 (Trial license)*, build **145.3191 de
  desarrollo**, **la prueba caduca el 2026-11-02** (Diego: se usa la prueba y se decide después con evidencia, A12).
  `sqcli.exe` SHA-256 `afa68ccb…a4f`. Interfaz y CLI no pueden funcionar a la vez: **cerrar la interfaz** antes de cada
  tanda.
- **Carpeta de intercambio:** `C:\StrategyQuantX145\user\lab_h0\` (plantillas, órdenes `-run`, salidas; B1 en
  `lab_h0\b1\`). Las rutas relativas de `sqcli` se resuelven **desde `C:\StrategyQuantX145`**.
- **Proyectos:** Builder (sin tocar desde la tarea 7, n.º 84–85) y Retester (último: n.º 146–147) **restaurados y
  comprobados** a su configuración original.
  Originales en `h0/configs/*_original_145.3191.cfx`.
- **Bancos** (todo lo nuestro es familia `H0-proceso`, datos quemados): `Builder/Results` = **40**; `Builder/H0_T7` y
  `Builder/H0_archivo` vacíos; `Retester/H0_USDCHF` = 10; `Retester/H0_T7` = 10; **`Retester/H0_B1` = 10** (B1);
  `Retester/Results` = 7 ejemplos de SQX (**no tocar**). Nada se ha borrado.
- **Símbolos creados por B1** (datos quemados, ventana 2023.01.02–2024.10.30): `USDCHF_B1` (zona EETUS) y
  `USDCHF_B1_TZ` (etiqueta UTC, para el control C2). No se han borrado.
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
5. **Antes de cada subida:** tests, `lab verificar`, `comprobar_evidencias.py`, buscar datos privados en archivos y
   mensajes, nada privado ni PDF ni código MT ni contenido del curso en git, `git fetch` antes de `push`.
6. **Trampas de SQX ya vistas:** órdenes asíncronas (`-databank action=load` suelta no espera; usar `-run` con
   `synctofiles`); **el Builder escribe siempre en `Results`**; **`-databank action=move` corta y no pega: no usarlo**;
   SQX reutiliza nombres de estrategia (identificar por hash); ~22 s por arranque; la consola va 2 h adelantada; las
   plantillas de fábrica no son homogéneas (al Retester le falta `<Swap>`); `engine=MetaTrader4`, no `mt4`;
   `-sourcecode` existe aunque `-h` no lo liste. **De B1:** la importación **exige** `format`; `-symbol action=list
   csv=true` no imprime nada (sin `csv`, sí); el volumen importado se recorta a 2³¹−1; la zona horaria al importar es una
   etiqueta; SQX ajusta el inicio del backtest al primer dato del símbolo; los CSV de operaciones llevan ticket, símbolo
   y saldo (comparar con `b1_diagnostico_operaciones.py`).
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
| Decisiones: 0001 (IA y herramientas), 0002 (datos quemados), **0003 (ACEPTADA v6)** | `docs/decisiones/` |
| **Índice único de asuntos abiertos** (A: Diego · B: técnico · C: requisitos futuros · D: no construir) | `docs/decisiones/PENDIENTES.md` |
| Protocolo de sellado de Darwinex (BORRADOR; manda la 0003 v6; con los requisitos de B1) | `protocols/2026-10-20_sellado_darwinex.md` |
| Revisiones externas 01–12 con la respuesta de Claude | `docs/revisiones/` |
| Prompt de auditoría maestra (para una sesión independiente) | `docs/auditoria/prompt_auditoria_maestra.md` |
| Mantenimiento del guardián (aplicado A9; procedimiento para el siguiente) | `docs/mantenimiento/` |
| Ficha H0 | `h0/ficha.md` |
| B1: plan con criterios previos y resultados | `h0/b1_plan_integridad.md`, `h0/b1_resultados.md` |
| B16: licencia frente al calendario (precios, inconclusos, texto para el soporte) | `h0/b16_licencia_calendario.md` |
| Plantillas, scripts de preparación, tandas y comparadores | `h0/configs/` |
| Guiones exactos de las tandas del 2026-10-20 | `h0/scripts_sesion_2026-10-20/` |
| Evidencias públicas (redactadas) | `h0/evidencias/` |
| Base de conocimiento (3 fichas de papers con verificaciones) | `conocimiento/` |
| Diario de lecciones, glosario, lección 01 | `aprendizaje/` |
| Núcleo Python y tests | `src/lab/`, `tests/` |
| Lanzador de Claude Code sin la clave API | `claude_lab.cmd` |

## 6. Decisiones de Diego (detalle en `PENDIENTES.md`, sección A)

**Cerradas el 2026-10-21** (varias por delegación explícita en el criterio de Claude): A1 (0003 v6), A2 (0 € reales
hasta superar la demo), A3 (horas variables, se registran), A5 (objetivo), A8 (curso comprado), A9 (guardián), A10
(clave API: se queda, el laboratorio no la usa), A17 (transcriptor), A19 (EURUSD), A20 (rigor con presupuesto de tiempo
por fase), A21 (pausa de revisiones externas hasta el piloto).
**Abiertas:** A12 licencia (se usa la prueba; se decide con evidencia después del 02-11) · A1b cifras del piloto
(propuestas en la 0003) · A4 repositorio público/privado · A6 regla de proporcionalidad · A7 cifras del criterio
económico · A11 MetaTrader · A13 identidad git · A14 copias de seguridad · A15 protección de rama · A18 numpy/pandas/scipy.

## 7. Siguiente paso (orden propuesto)

1. **Antes del 02-11 (con SQX):** exportar todo lo que H1 necesite sin SQX (velas de la ventana quemada: ya en
   `lab_h0/b1/EA1`; operaciones y código de H0 ya exportados) y comprobarlo; decidir qué más conviene medir mientras
   dure la prueba (p. ej. el coste de un lote del piloto con datos quemados).
2. **B14: registro con eventos tipados** (tipo, familia, origen de la hipótesis, motivo de descarte) y **registro de
   hipótesis**, con tests, antes de H1.
3. **B15 + B9: segunda sesión de mantenimiento del guardián** (Claude prepara y prueba el borrador; Diego la abre).
4. **B18: revisión del curso** con *medium* + fotogramas, por tandas de noche y nunca a la vez que una medición de SQX →
   fecha máxima vista (provisional: 2025-03) → inicio del sellado.
5. **B19: protocolo estadístico del piloto implementado y probado** (referencias C20, criterio de superación,
   incertidumbre con dependencia, control negativo B17).
6. Reescribir y aprobar el protocolo de sellado (con B18 y los requisitos de B1) → descargar Darwinex → ficha C12 de
   EURUSD (costes de Darwinex Zero, reloj real, volumen, huecos) → piloto.
7. **Auditoría maestra independiente (B13):** tarjeta `task_fe8910bc` propuesta el 2026-10-20 (caduca hacia el
   2026-10-27); si caduca, volver a proponerla con el prompt guardado.

## 8. Revisiones externas recibidas (vía Diego)

01 auditoría del curso y 0003 · 02 organización y fichas · 03 viabilidad para un particular · 04 ¿camino razonable? ·
05 laboratorio integrado · 06 enmiendas a 0003 · 07 base de conocimiento · 08 auditoría de diseño y prompt maestro ·
09 auditoría estática de un ZIP (cifras verificadas) · **2026-10-21:** 10 evaluación sincera (amplía A7, sugiere A21) ·
11 cambio de enfoque (referencias previas C20; Claude añade B17) · 12 diagnóstico con la v6 (B19; coste de B18; misión →
A5). Desde la 10, en formato corto por la pausa A21. Si vienen del mismo modelo, que coincidan no es evidencia
independiente.

## 9. Lo esencial aprendido (detalle en `aprendizaje/diario.md`)

El código 0 y los mensajes de éxito mienten; un resultado idéntico necesita control negativo, y un control negativo
puede estar mal diseñado (C2); un indicador mal elegido casi da una conclusión falsa; una cifra plausible no es una cifra
comprobada; registrar sin límite no controla el sobreajuste; con 7 años caben ~139 configuraciones independientes antes
de Sharpe 1 por azar; hay que guardar los resultados de **todas** las estrategias probadas; un periodo sellado dentro de
SQX no está sellado; lo que se ha visto (el curso, el conocimiento de Claude) no se puede sellar; "ignorado por git" no
es "privado"; la memoria y los resúmenes también se equivocan; los criterios se fijan antes y no se tocan después.
