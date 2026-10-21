# Estado del proyecto y punto de continuación

**Actualizado: 2026-10-20 (cierre de la primera sesión local en el PC de SQX).** Último registro: n.º 89.
**Comprobado al reiniciar el 2026-10-21:** tests 20/20, guardián 28/28, registro 89, evidencias 0 fallos, git limpio y
0/0 con origin, `sqcli.exe` con el mismo SHA-256, bancos como en §3 (40 · 0 · 0 · 10 · 10 · 7). A9 sin hacer.
Este documento es el **punto de entrada al reiniciar una sesión**. Si algo aquí contradice a un archivo más específico,
manda el más específico (estado de H0: `h0/ficha.md`; asuntos abiertos: `docs/decisiones/PENDIENTES.md`; hechos:
`registry/experimentos.jsonl`), y se corrige este documento.

## 0. Al empezar una sesión nueva (en este orden)

1. Leer `CLAUDE.md` (reglas duras), **este documento**, `aprendizaje/diario.md` (errores ya vistos) y
   `docs/decisiones/PENDIENTES.md` (todo lo abierto).
2. Comprobar el banco de trabajo:
   `python -m unittest discover -s tests` (20/20) · `python .claude/hooks/guardian.py --autotest` ·
   `PYTHONPATH=src python -m lab verificar` (89 entradas o más) · `python -I h0/configs/comprobar_evidencias.py`
   (0 fallos) · `git status` limpio · `git fetch` y sin divergencias con `origin/claude/proyecto-2026-fps66g`.
3. Mirar si Diego ha resuelto algo de la sección 6 (decisiones) o la sesión de mantenimiento del guardián (A9).
4. Seguir por la sección 7 (siguiente paso).

## 1. Objetivo y fase

- **Objetivo** (CLAUDE.md; propuesta de enunciado nuevo pendiente, asunto A5): averiguar con evidencia si una estrategia
  tiene ventaja real o es ruido. **Concluir "no hay edge" es un resultado válido.**
- **Fase: H0 (viabilidad técnica), casi cerrada.** Siguiente hito: H1 (puente SQX completo con MetaTrader y
  reconstrucción independiente), **no antes** de cerrar las condiciones previas de la sección 7.

## 2. Qué está demostrado (H0) y qué no

| Tarea H0 | Estado | Evidencia clave |
|---|---|---|
| 0. Banco de trabajo | SÍ, con un agujero | Registros 5–8. PowerShell no pasa por el guardián (arreglo listo, A9) |
| 1. `sqcli -h`, build | SÍ | 145.3191, firma válida (n.º 9–10) |
| 2. Límites de la prueba | NO en lo probado | WFO y What If funcionan (n.º 57–71); optimización secuencial INCONCLUSA |
| 3a–3d. Generar, backtest, exportar | SÍ | n.º 16–33, 34–48 |
| 3e–3f. Código MT4/MT5 | Exporta SÍ · compila INCONCLUSO | n.º 27–31; no hay MetaTrader |
| 4. Reproducir backtest | SÍ | 1.353 operaciones idénticas, control negativo (n.º 43–56) |
| 5. Datos de Darwinex | Metadatos SÍ; descarga bloqueada por protocolo | n.º 87–88 |
| 6. Pasos manuales | Uno: cerrar la interfaz de SQX | Tareas 3–7 |
| 7. Experimento completo | SÍ: 54,7 s | n.º 72–86 (dos intentos fallidos registrados) |

**No demostrado (y no es objetivo de H0):** ninguna ventaja de mercado; reconstrucción independiente de SQX; costes
reales de Darwinex Zero; aislamiento real del bloque sellado; corrección por selección sobre el universo completo.

## 3. Estado exacto del PC de SQX (no está en git; comprobar al reiniciar)

- **SQX:** `C:\StrategyQuantX145`, *StrategyQuant X **Pro** Build 145 (Trial license)*, build **145.3191 de
  desarrollo**, **la prueba caduca el 2026-11-02**. `sqcli.exe` SHA-256 `afa68ccb…a4f`. Interfaz y CLI no pueden
  funcionar a la vez: **cerrar la interfaz** antes de cada tanda.
- **Carpeta de intercambio:** `C:\StrategyQuantX145\user\lab_h0\` (plantillas, órdenes `-run`, salidas). Se usa para
  que las rutas no lleven el usuario de Windows. Las rutas relativas de `sqcli` se resuelven **desde `C:\StrategyQuantX145`**.
- **Proyectos:** Builder y Retester **restaurados y comprobados** a su configuración original (n.º 32–33, 54–55,
  66–67, 84–85). Originales en `h0/configs/*_original_145.3191.cfx`.
- **Bancos** (todo lo nuestro es familia `H0-proceso`, datos quemados): `Builder/Results` = **40** estrategias de
  prueba (n.º 23, 72, 74, 80; antes de H0 tenía 0); `Builder/H0_T7` y `Builder/H0_archivo` vacíos (creados en H0);
  `Retester/H0_USDCHF` = 10; `Retester/H0_T7` = 10; `Retester/Results` = 7 ejemplos de SQX (**no tocar**).
  Nada se ha borrado.
- **Datos quemados** (decisión 0002): `USDCHF_M1_dukas`, 2023-01-01 → 2024-10-30, hash del directorio `4ee152b0…`.
  Solo para pruebas de proceso; **USDCHF no será el primer mercado de investigación**.
- **Python 3.14.6**; `pdfplumber` sí; **numpy, pandas y scipy NO** (A18); FFmpeg y Whisper NO (A17).
  `pip install -e .` no hecho: usar `PYTHONPATH=src python -m lab …`.
- **Git:** sin identidad configurada; los commits se hacen con
  `git -c user.name=Claude -c user.email=noreply@anthropic.com commit -F <archivo>` (A13). `core.autocrlf=true`
  (por eso `.gitattributes`: evidencias byte a byte, registro y `.sh` en LF).
- **Variable de usuario `ANTHROPIC_API_KEY`** definida en Windows (no se ha mirado su valor; A10).
- **Carpetas privadas fuera del repositorio** (solo en este PC; **copia de seguridad: A14**):
  `h0/evidencias_privadas/` (dentro del proyecto pero ignorada por git: originales con ID de hardware y licencia),
  `C:\Users\SERVILAB\Documents\LAB_PRIVADO_CURSO\` (auditoría del curso, herramientas para leer el zip, configs
  extraídas) y `C:\Users\SERVILAB\Documents\LAB_BIBLIOTECA\papers\` (3 PDF, su texto e imágenes de fórmulas).
- **Curso de Imox:** `C:\Users\SERVILAB\Desktop\curso de trading algoritmico\IMOX TRADING.zip.001…008` (14,8 GB,
  85 vídeos + configuraciones). Procedencia por aclarar (A8). Nada del curso va a GitHub. Junto a las partes hay
  además una **carpeta** llamada `IMOX TRADING.zip` (creada el 2026-10-20 13:30, probablemente lo extraído); no se
  ha podido mirar dentro porque el guardián bloquea `ls` en esa ruta (falso positivo, B9).
- **Repositorio de GitHub público** (`LaRuinaDeMago/TradingAlgoritmico`, rama `claude/proyecto-2026-fps66g`); A4.
  El historial ya contiene el ID de hardware, el de la licencia de prueba y el usuario de Windows (decisiones de
  Diego del 2026-10-20 de no reescribir historial).

## 4. Cómo se trabaja aquí (procedimiento probado)

1. **Todo comando de SQX por el ejecutor:** `PYTHONPATH=src python -m lab ejecutar --nombre <n> --version-sqx
   "145.3191-dev" [--datos …] [--costes …] --descripcion "…" -- "C:/StrategyQuantX145/sqcli.exe" <orden>`.
   Redacta solo los datos privados conocidos y guarda el original en `h0/evidencias_privadas/`.
2. **Commit antes de cada ejecución** (si no, sale `"sucio": true`) y **no tocar el repositorio mientras corre** una tanda.
3. **No fiarse del "OK" ni del código 0**: leer la evidencia entera (el original privado si hay redacción) y comprobar el
   efecto real (recuentos, archivos, volver a exportar la configuración y compararla con
   `h0/configs/comparar_bloque.py`).
4. **Antes de cada subida:** tests, `lab verificar`, `h0/configs/comprobar_evidencias.py`, buscar valores reales
   conocidos en archivos y mensajes, ninguna evidencia privada ni PDF ni código MT en git, `git fetch` antes de `push`.
5. **Trampas de SQX ya vistas:** órdenes asíncronas (`-databank action=load` suelta no espera; usar `-run` con
   `synctofiles` y comprobar); los bancos se cargan del disco en diferido; **el Builder escribe siempre en `Results`**
   (ignora el banco de salida de la plantilla); **`-databank action=move` corta y no pega: no usarlo**; SQX reutiliza
   nombres ("Strategy 0.11(2)"): identificar por hash; cada arranque reescribe los archivos del banco; ~22 s por arranque;
   la consola va 2 h adelantada; las plantillas de fábrica no son homogéneas (al Retester le falta `<Swap>`); el motor de
   código es `engine=MetaTrader4`, no `mt4`; `-sourcecode` existe aunque `-h` no lo liste.
6. **Falsos positivos del guardián** (no rodearlo: usar la vía sancionada): en un comando que nombra `registry` o
   `.claude`, evitar "del" (palabra española), `>`, `>=`, `2>&1`, `->`; los nombres con "zip" y `.find(`/`glob.glob`
   sobre rutas fuera de `src|tests|h0…` también saltan. Vía sancionada: **commit con `-F archivo`**, código en un archivo
   escrito con Write, resultados largos con `--resultado archivo.json`, separar comandos.
7. **Nunca:** leer `data/sealed/`, operar en real, comprar, borrar estrategias o datos de Diego, modificar el guardián,
   aprobar decisiones que son de Diego (aunque las delegue).

## 5. Mapa de documentos

| Qué | Dónde |
|---|---|
| Reglas duras y estilo | `CLAUDE.md` |
| Hoja de ruta (PDF de Diego y transcripción, con nota de desfase) | `docs/hoja_de_ruta*.{md,pdf}` |
| Decisiones: 0001 (IA y herramientas), 0002 (datos quemados), **0003 (PROPUESTA v5: reparto, mercado, presupuesto, abandono, con historial)** | `docs/decisiones/` |
| **Índice único de asuntos abiertos** (A: Diego · B: técnico · C: requisitos futuros · D: no construir) | `docs/decisiones/PENDIENTES.md` |
| Protocolo de sellado de Darwinex (BORRADOR) | `protocols/2026-10-20_sellado_darwinex.md` |
| Revisiones externas 01–09 con la respuesta de Claude | `docs/revisiones/` |
| Prompt de auditoría maestra (para una sesión independiente) | `docs/auditoria/prompt_auditoria_maestra.md` |
| Arreglo del guardián listo e instrucciones de mantenimiento | `docs/mantenimiento/` |
| Ficha H0 (estado por tarea, con evidencias) | `h0/ficha.md` |
| Plantillas, scripts de preparación y comprobación | `h0/configs/` |
| Guiones exactos de las tandas del 2026-10-20 | `h0/scripts_sesion_2026-10-20/` |
| Evidencias públicas (redactadas) y salidas de H0 | `h0/evidencias/` |
| Base de conocimiento (4 bloques, plantilla, 3 fichas de papers con verificaciones) | `conocimiento/` |
| Diario de lecciones, glosario, lección 01 | `aprendizaje/` |
| Núcleo Python (registro, ejecutor, redacción, hashes) y tests | `src/lab/`, `tests/` |

## 6. Decisiones de Diego pendientes (resumen; detalle en `PENDIENTES.md`, sección A)

Las más urgentes: **A9** sesión de mantenimiento del guardián · **A1** aprobar la 0003 (v5) y **A1b** cifras del piloto ·
**A2** dinero que está dispuesto a perder · **A3** horas semanales · **A20** prioridad principal (pegó las tres
opciones sin elegir; añadió "usar Claude Code y Opus para optimizar el proceso en todos los sentidos") · **A19** primer
mercado · **A12** licencia (la caducidad del 2026-11-02 no es motivo para comprar). Después: A4 repositorio
público/privado, A5 enunciado del objetivo, A6 regla de proporcionalidad, A7 éxito por rentabilidad neta frente al coste
total, A8 procedencia del curso, A10 clave API, A11 MetaTrader, A13 identidad git, A14 copias de seguridad, A15
protección de rama, A17 piloto de vídeos, A18 numpy/pandas/scipy.

## 7. Siguiente paso (orden propuesto)

1. **Diego: sesión de mantenimiento del guardián** (`docs/mantenimiento/README.md`), incluyendo B15 (permiso de acceso
   ligado a recurso y finalidad). Después, **Claude comprueba con una llamada real de PowerShell** (B3).
2. **Claude: prueba de integridad exportar/importar por fechas (B1)** con USDCHF quemado: intervalo exacto (límites
   inclusivos/exclusivos), importación sin errores, velas idénticas tras normalizar, sin ausentes/duplicadas/desplazadas,
   zona horaria, repetible, y **mismo backtest antes y después**. Es la última pieza técnica antes de Darwinex.
3. **Claude: esquema de eventos tipados del registro (B14)**, con tests, antes de H1.
4. **Claude: licencia frente a calendario (B16)** antes del 2026-11-02: qué de H1 se puede hacer sin licencia.
5. **Auditoría maestra independiente (B13):** tarjeta de sesión propuesta el 2026-10-20 (`task_fe8910bc`, solo
   lectura; caduca hacia el 2026-10-27). Si caduca, volver a proponerla con el prompt guardado.
6. Con las decisiones de Diego: aprobar la 0003 → aprobar el protocolo de sellado → descargar Darwinex según el
   protocolo → ficha de datos y costes del instrumento (C12) → piloto de búsqueda (0003 v5).

## 8. Revisiones externas recibidas (todas el 2026-10-20, vía Diego)

01 auditoría del curso y 0003 · 02 organización y fichas · 03 viabilidad para un particular y enmiendas a 0003 ·
04 ¿camino razonable? · 05 laboratorio integrado y ciclo de aprendizaje · 06 enmiendas concretas a 0003 ·
07 base de conocimiento · 08 auditoría de diseño y prompt maestro · 09 auditoría estática de un ZIP antiguo (cifras
del registro verificadas: exactas). Varias leían versiones antiguas de la 0003: por eso lleva historial de versiones.
Si vienen del mismo modelo, que coincidan no es evidencia independiente.

## 9. Lo esencial aprendido (detalle en `aprendizaje/diario.md`)

El código 0 y los mensajes de éxito mienten; un resultado idéntico necesita control negativo; un indicador mal elegido
casi da una conclusión falsa (WF "vacío"); una cifra plausible no es una cifra comprobada ("cientos de operaciones");
registrar sin límite no controla el sobreajuste; con 7 años caben ~139 configuraciones independientes antes de Sharpe 1
por azar y con 24 meses sellados ~7; hay que guardar los resultados de **todas** las estrategias probadas; un periodo
sellado dentro de SQX no está sellado; "ignorado por git" no es "privado".
