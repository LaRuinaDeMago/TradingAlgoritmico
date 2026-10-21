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
- **Variable de usuario `ANTHROPIC_API_KEY`** definida en Windows (no se ha mirado su valor; A10). **Ojo:** hace que
  `claude` lanzado desde PowerShell se cobre por consumo ("API Usage Billing"). Mientras A10 siga abierto, en cada
  ventana: `Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue` antes de `claude`.
- **Carpetas privadas fuera del repositorio** (solo en este PC; **copia de seguridad: A14**):
  `h0/evidencias_privadas/` (dentro del proyecto pero ignorada por git: originales con ID de hardware y licencia),
  `C:\Users\SERVILAB\Documents\LAB_PRIVADO_CURSO\` (auditoría del curso, herramientas para leer el zip, configs
  extraídas) y `C:\Users\SERVILAB\Documents\LAB_BIBLIOTECA\papers\` (3 PDF, su texto e imágenes de fórmulas).
- **Curso de Imox:** `C:\Users\SERVILAB\Desktop\curso de trading algoritmico\IMOX TRADING.zip.001…008` (14,8 GB,
  85 vídeos + configuraciones). Procedencia por aclarar (A8: el zip trae 3 imágenes "WWW.CURSOSDIGITALEX.COM"). Nada
  del curso va a GitHub. **Inventario del 2026-10-21** (privado, en `LAB_PRIVADO_CURSO`): los 85 vídeos están sin
  comprimir dentro del zip; 78 MP4 = 26,3 h; 7 MKV (2,8 GB) sin duración legible. Junto a las partes hay una
  **carpeta** `IMOX TRADING.zip` (2026-10-20 13:30) con una extracción **parcial**: 8 vídeos (3,3 h) de "Bonus 2025",
  idénticos en tamaño al índice. El guardián bloquea cualquier comando que nombre esa ruta (`zip`, falso positivo B9):
  se lee con scripts de `LAB_PRIVADO_CURSO/herramientas/` que llevan la ruta dentro. Con los 7 MKV (2,4 h): **28,7 h**.
  El zip se empaquetó el **2026-01-12**. Transcriptor en `LAB_PRIVADO_CURSO/.venv_transcripcion` (Python aparte;
  faster-whisper 1.2.1, PyAV 18.1.0, modelos small y medium); herramientas: `extraer_videos.py`, `transcribir.py`,
  `fotogramas.py`, `duraciones_zip.py`, `duracion_mkv_av.py`.
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
| Decisiones: 0001 (IA y herramientas), 0002 (datos quemados), **0003 (ACEPTADA v6 el 2026-10-21: reparto por regla, EURUSD, presupuesto, abandono, con historial)** | `docs/decisiones/` |
| **Índice único de asuntos abiertos** (A: Diego · B: técnico · C: requisitos futuros · D: no construir) | `docs/decisiones/PENDIENTES.md` |
| Protocolo de sellado de Darwinex (BORRADOR) | `protocols/2026-10-20_sellado_darwinex.md` |
| Revisiones externas 01–11 con la respuesta de Claude | `docs/revisiones/` |
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

**Cerradas el 2026-10-21** (Diego, en el chat; varias por delegación explícita en el criterio de Claude): A1 (0003
aceptada v6), A2 (0 € reales hasta superar la demo), A3 (horas variables, se registran), A8 (curso comprado), A17
(transcriptor instalado), A19 (EURUSD), A20 (rigor con presupuesto de tiempo por fase), A21 (pausa de revisiones).
Las más urgentes que quedan: **A9** sesión de mantenimiento del guardián · **A10** la clave API (urgente: hizo que
`claude` en PowerShell se cobrara por consumo) · **A12** licencia (la caducidad del 2026-11-02 no es motivo para
comprar; antes, B16) · **A1b** cifras del piloto (propuestas en la 0003). Después: A4 repositorio
público/privado, A5 enunciado del objetivo, A6 regla de proporcionalidad, A7 éxito por rentabilidad neta frente al coste
total, A8 procedencia del curso, A10 clave API, A11 MetaTrader, A13 identidad git, A14 copias de seguridad, A15
protección de rama, A17 piloto de vídeos, A18 numpy/pandas/scipy.

## 7. Siguiente paso (orden propuesto)

1. **Diego: sesión de mantenimiento del guardián** (`docs/mantenimiento/README.md`): **solo el borrador de PowerShell**,
   que es lo que está escrito y probado (44/44). B15 (permiso del sellado ligado a recurso y finalidad) y B9 (falsos
   positivos) no tienen borrador todavía: Claude los prepara y probará, y van en una **segunda** sesión de
   mantenimiento antes de descargar Darwinex (hasta entonces no hay nada sellado que proteger). Mientras Diego hace A9,
   **Claude no hace commits ni lanza SQX** en esta carpeta (para no mezclar cambios ni dejar registros "sucios").
   Después, **Claude comprueba con una llamada real de PowerShell** (B3).
2. **Claude: prueba de integridad exportar/importar por fechas (B1)** con USDCHF quemado: intervalo exacto (límites
   inclusivos/exclusivos), importación sin errores, velas idénticas tras normalizar, sin ausentes/duplicadas/desplazadas,
   zona horaria, repetible, y **mismo backtest antes y después**. Es la última pieza técnica antes de Darwinex.
3. **Claude: esquema de eventos tipados del registro (B14)**, con tests, antes de H1.
4. **Claude: licencia frente a calendario (B16)** antes del 2026-11-02: qué de H1 se puede hacer sin licencia.
5. **Auditoría maestra independiente (B13):** tarjeta de sesión propuesta el 2026-10-20 (`task_fe8910bc`, solo
   lectura; caduca hacia el 2026-10-27). Si caduca, volver a proponerla con el prompt guardado.
6. **Curso completo (B11 → B18):** transcripción con *medium* (≈ 55 h de CPU, por tandas, nunca a la vez que una
   medición de tiempo de SQX) + fotogramas → **fecha de mercado más tardía vista en el curso = inicio del sellado**
   (0003 v6 §1). Plan: `LAB_PRIVADO_CURSO/plan_revision_curso.md`.
7. 0003 ya aceptada (v6) → reescribir y aprobar el protocolo de sellado con la fecha de B18 y lo aprendido en B1 →
   descargar Darwinex según el protocolo → ficha de datos y costes de EURUSD (C12) → **referencias preregistradas
   (C20)** → piloto de búsqueda **con su control negativo sobre datos sintéticos (B17)**.

## 8. Revisiones externas recibidas (vía Diego)

01 auditoría del curso y 0003 · 02 organización y fichas · 03 viabilidad para un particular y enmiendas a 0003 ·
04 ¿camino razonable? · 05 laboratorio integrado y ciclo de aprendizaje · 06 enmiendas concretas a 0003 ·
07 base de conocimiento · 08 auditoría de diseño y prompt maestro · 09 auditoría estática de un ZIP antiguo (cifras
del registro verificadas: exactas). **2026-10-21:** 10 evaluación sincera (casi nada nuevo: amplía A7 y sugiere A21) ·
11 cambio de enfoque (idea clave: referencias definidas antes, C20; competición de métodos aplazada a D; Claude añade el
control negativo B17). Varias leían versiones antiguas de la 0003: por eso lleva historial de versiones.
Si vienen del mismo modelo, que coincidan no es evidencia independiente.

## 9. Lo esencial aprendido (detalle en `aprendizaje/diario.md`)

El código 0 y los mensajes de éxito mienten; un resultado idéntico necesita control negativo; un indicador mal elegido
casi da una conclusión falsa (WF "vacío"); una cifra plausible no es una cifra comprobada ("cientos de operaciones");
registrar sin límite no controla el sobreajuste; con 7 años caben ~139 configuraciones independientes antes de Sharpe 1
por azar y con 24 meses sellados ~7; hay que guardar los resultados de **todas** las estrategias probadas; un periodo
sellado dentro de SQX no está sellado; "ignorado por git" no es "privado".
