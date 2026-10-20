# H0 – Ficha de viabilidad técnica

SQX según la pantalla de inicio: **"StrategyQuant X Pro Build 145 (Trial license)"**, build **145.3191**, **build de desarrollo del 2026-10-06**
(no es versión final), prueba válida hasta el **02-11-2026** (registros n.º 1 y 2, evidencias en `h0/evidencias/20261019_*`).
⚠️ La hoja de ruta decía *Ultimate, build 143.2708*: **no coincide**. Ver la fila "Versión y edición" más abajo.
Inicio de la prueba: 2026-10-19 (quedaban 14 d 00:32 en la captura) · Sistema operativo del PC de SQX: Windows 11 (según Diego)

Estados: **SÍ** / **NO** / **INCONCLUSO** / PENDIENTE (aún no probado).
Regla: solo se marca SÍ o NO con evidencia guardada en `h0/evidencias/` y una entrada en `registry/experimentos.jsonl`.
Si algo no se puede comprobar dentro de la prueba, queda INCONCLUSO; nunca se supone.

## Paso 0 – El banco de trabajo funciona en el PC de SQX

| Comprobación | Estado | Evidencia | Tiempo |
|---|---|---|---|
| `python --version` ≥ 3.10 | **SÍ** (3.14.6) | Registro n.º 5 · `h0/evidencias/20261020T000119Z_p0_python_version.txt` | < 1 min |
| `python -m unittest discover -s tests` sin fallos | **SÍ** (13/13) | Registro n.º 6 · `h0/evidencias/20261020T000120Z_p0_unittest.txt` | < 1 min |
| `python .claude/hooks/guardian.py --autotest` sin fallos | **SÍ** (28/28) | Registro n.º 7 · `h0/evidencias/20261020T000123Z_p0_guardian_autotest.txt` | < 1 min |
| Prueba real: pedir a Claude Code que lea `data/sealed/x` y que el guardián lo bloquee | **SÍ, con un agujero** | Registro n.º 8. Bash: lo bloquea el guardián. Read: lo bloquea antes la regla `deny`. **La herramienta PowerShell no pasa por el guardián** (arreglo preparado; falta la sesión de mantenimiento) | 10 min |

Si el hook no se ejecuta (por ejemplo, porque `python` no está en el PATH), **no hay protección**: se arregla antes de seguir.
Nota: `pip install -e .` no está hecho en este PC; mientras tanto se usa `PYTHONPATH=src python -m lab ...`.

## Tareas H0

| # | Tarea | Estado | Evidencia | Tiempo |
|---|---|---|---|---|
| 1 | Localizar `sqcli.exe`, confirmar la build y guardar la salida completa de `sqcli.exe -h` | **SÍ** | `C:\StrategyQuantX145\sqcli.exe`, SHA-256 `afa68ccb…a4f`, firma Authenticode **válida** de StrategyQuant s.r.o. Registro n.º 9 · copia pública redactada `h0/evidencias/20261020T000832Z_t1_sqcli_ayuda.redactada.txt` (registro n.º 10; el original, con el ID de hardware, solo en el PC): `SQX version: 145.3191`, código 0, 24,5 s. Antes, registros n.º 3 y 4: **FALLIDO** con código 0 porque la GUI estaba abierta. La **edición** (Pro/Ultimate) sigue sin confirmar | 25 min |
| 2 | ¿La prueba gratuita limita alguna función de la línea de comandos? | **NO, en lo probado** · INCONCLUSO (Optimización secuencial) | Licencia: *"StrategyQuant X **Pro** Build 145 (Trial license)"* (n.º 11–12). Todo lo usado en las tareas 1, 3 y 4 funcionó sin límites. La documentación dice que una licencia *Special Trial* desactiva What If, Optimización secuencial y Walk-Forward Optimization. Prueba (n.º 57–61, Retester con datos quemados): **WFO y What If se ejecutan y dejan resultados reales** en `settings.xml` (11 periodos de WF con ventanas y parámetros optimizados distintos en cada uno; resultado What If de 26 KB), inspección registrada en n.º 68–71. Control positivo: Monte Carlo Manipulation (30 simulaciones). Ojo: las carpetas `Results/WF…` y `Results/CrossCheck_WhatIf` salen con **0 bytes** también en la Walk-Forward Matrix, que no está bloqueada (n.º 62–65): ese vacío no indica bloqueo. **Sin probar:** Optimización secuencial (no está en la plantilla del Retester). Retester restaurado y comprobado (n.º 66–67) | 60 min |
| 3a | CLI: lanzar un proyecto de generación | **SÍ** | Datos quemados según la **decisión 0002** (registro n.º 18): USDCHF H1, 2023-01-01 – 2024-10-30. Proyectos y datos disponibles: registros n.º 16–17 (solo datos de ejemplo de SQX). Configuración: copia original (n.º 19, `h0/configs/Builder_original_145.3191.cfx`) → plantilla mínima hecha con `h0/configs/preparar_builder_usdchf.py` → `loadconfig` (n.º 21), **comprobado** volviendo a exportar (n.º 22) → `-project action=start name=Builder` (n.º 23): **10 estrategias en 6 s** (33 s con el arranque), ≥ 17 probadas, familia `H0-proceso`. Builder restaurado y comprobado: 0 diferencias (n.º 32–33). Notas: backtest **solo con velas H1** (`testPrecision="1"`, ~12.400 "ticks"): hay operaciones que abren y cierran en la misma vela; aviso de SQX sobre un cambio de convención horaria en los datos; **sin semilla aleatoria** documentada | 40 min |
| 3b | CLI: ejecutar un backtest | **SÍ** | Backtest de estrategias ya existentes con el proyecto **Retester**: configuración original guardada (n.º 34), plantilla mínima con los mismos datos, costes, opciones y gestión de capital que el Builder (comprobado: 0 diferencias), en un banco propio `H0_USDCHF` (el banco `Results` trae 7 estrategias de ejemplo de SQX que no se tocan; n.º 35–38), carga de las 10 estrategias (n.º 39–42) y `-project action=start name=Retester` (n.º 43): 10 estrategias en 1,1 s. **Ojo: `-databank action=load` es asíncrona**: suelta dice "Strategies loaded" y no guarda nada (n.º 39 y 41); hizo falta `-run file=` con `synctofiles` (n.º 42) | 30 min |
| 3c | CLI: exportar estrategias | **SÍ** | Registro n.º 24: `-databank action=save` → 10 `.sqx` (zip con `settings.xml`, `strategy_Portfolio.xml`, `orders.bin`…). Públicas en `h0/evidencias/t3_salidas/estrategias/` (n.º 31). Ojo: no son copias byte a byte de las del banco (pesan unos bytes distintos) | 5 min |
| 3d | CLI: exportar resultados y operaciones a formato legible (CSV u otro) | **SÍ** | Registro n.º 25: `-databank action=export` → `Results.csv` (separador `;`, métricas IS). Registro n.º 26: `-tools action=orderstocsv` sobre la carpeta → 1 CSV de operaciones por estrategia. Públicos en `h0/evidencias/t3_salidas/`. Notas: **los valores salen traducidos** ("Comprar"/"Vender") según el idioma de SQX; **hipótesis por verificar:** el P/L en USD de USDCHF usa un **tipo de cambio fijo** (`pointValue` 115.179,5 = 100.000/0,8682): una pérdida de 36 pips da exactamente −41,46 $ = 0,0036 × 11.517,95 | 5 min |
| 3e | CLI: exportar código para MT4 | **SÍ (exportar)** · INCONCLUSO (compilar) | `-sourcecode` **no aparece en `-h` pero existe**. Con `engine=mt4` (lo que dicen la documentación y la plantilla): "Generator 'mt4' not found" (n.º 27). Con `engine=MetaTrader4` y ruta relativa: falla porque **las rutas relativas se resuelven desde `C:\StrategyQuantX145`** (n.º 28). Con ruta absoluta: `.mq4` de 273 KB con `OnInit`/`OnTick`/`OnDeinit` (n.º 29). **Sin compilar** (no hay MetaTrader). Se guarda solo en el PC (hash en n.º 31): incrusta la librería OrderReliable, cedida solo para estrategias de SQ | 10 min |
| 3f | CLI: exportar código para MT5 | **SÍ (exportar)** · INCONCLUSO (compilar) | `engine=MetaTrader5`, registro n.º 30: `.mq5` de 298 KB con `OnInit`/`OnTick`/`OnDeinit`. Necesita 47 indicadores `Sq*` propios en MT5. Su cabecera dice, por error, "for MetaTrader4". Sin compilar; solo en el PC (hash en n.º 31) | 5 min |
| 4 | Recorrido mínimo: generar, exportar, registrar y reproducir el backtest dos veces con resultados idénticos | **SÍ** | Dos backtests independientes (n.º 43–48): **10 de 10 estrategias idénticas byte a byte, 1.353 operaciones**, y también idénticas a las de la generación (n.º 26). **Control negativo** (n.º 49–53): misma configuración salvo spread 3 → 0 de 10 idénticas, así que el Retester recalcula de verdad. Comparación registrada en n.º 56 con `h0/configs/comparar_operaciones.py`; operaciones públicas en `h0/evidencias/t4_salidas/`. Retester restaurado y comprobado (n.º 54–55). **Límites:** una máquina, una build de desarrollo, backtest solo con velas H1; la **generación** no se ha reproducido (no hay semilla documentada). n.º 44–48 salieron "sucios" por un descuido de Claude (archivo creado durante la ejecución) | 45 min |
| 5 | Datos de Darwinex: procedencia, instrumentos, periodo, granularidad y modelo de costes | PENDIENTE (metadatos hechos) | No hay datos de Darwinex instalados (n.º 17). **Instrumentos y periodo** (n.º 87, `-symbol action=darwinexsymbols`, no está en `-h` pero funciona; sin descargar precios): 328 símbolos; forex y metales 45, casi todos desde **2017-10-01**; índices 13 (2017-10 / 2018-06 / 2019-12); energía 3; cripto 9; acciones de EE. UU. 258 (desde 2019-12). Fecha final, granularidad, zona horaria y costes: **sin comprobar**. **Antes de descargar ningún precio:** protocolo de sellado `protocols/2026-10-20_sellado_darwinex.md` (BORRADOR, lo aprueba Diego) | 15 min |
| 6 | Pasos que exigen intervención manual y con qué frecuencia | **SÍ, uno** (en lo probado) · INCONCLUSO (Darwinex, MetaTrader) | El experimento completo de la tarea 7 corre sin interfaz. Único paso manual: **cerrar la interfaz de SQX antes de cada tanda** (solo admite una instancia; n.º 3–4). **Trampas de automatización** encontradas (n.º 72–78), que el guion ya evita: el Builder ignora el banco de salida de la plantilla y escribe siempre en `Results`; los bancos se cargan del disco en diferido; `-databank action=move` corta y no pega (riesgo de pérdida: no se usa); `-databank action=load` suelta no espera. Sin probar: datos de Darwinex y compilar en MetaTrader | |
| 7 | Tiempo y coste de un experimento completo de principio a fin | **SÍ** | Registros n.º 79–86, receta `h0/configs/t7_experimento.sh` (2 arranques de `sqcli`: generar y restaurar; copiar las nuevas; operaciones, backtest de reproducción y restaurar; comparar). **54,7 s de principio a fin**, incluidos registro y commits: generar 10 estrategias ~1–2 s, backtest de 10 en 0,85 s y **~22 s por cada arranque de `sqcli`** (casi todo el tiempo). Operaciones de la generación y de la reproducción **idénticas en 10 de 10**; Builder y Retester restaurados (0 diferencias). Coste en dinero: 0 durante la prueba; falta el precio de la licencia. **Límite:** experimento mínimo; con generación genética, walk-forward o más datos, el cálculo dominará el tiempo. Dos intentos anteriores fallidos y registrados (n.º 72–75) | 90 min |

### Cómo se ejecuta cada comando (para que quede registrado)

```
python -m lab ejecutar --nombre t1_sqcli_ayuda --version-sqx 143.2708 -- "<ruta>\sqcli.exe" -h
```

El ejecutor guarda stdout/stderr en `h0/evidencias/`, mide la duración y anota la entrada en el registro, también si falla.
Los comandos de SQX que se usen en las tareas 2–4 salen **solo** de la salida de `-h` o de la documentación oficial, citando la fuente.

### Notas previas (sin verificar; solo orientan dónde mirar)

Según la documentación pública de StrategyQuant, no comprobado en nuestra build:
- `sqcli.exe` está en la carpeta de instalación de SQX; la CLI mejorada existe desde la build 127.
- Sin parámetros abre una consola interactiva; dentro, `-h` lista los comandos y `-exit` sale.
  → El ejecutor cierra la entrada estándar y tiene tiempo máximo, así que si `sqcli.exe -h` se queda esperando, quedará registrado como FALLIDO y se probará otra forma.
- La salida puede redirigirse a archivo con `>`.
- Hay un fallo conocido en el foro sobre añadir instrumentos por CLI (`orderSizeMultiplier`).

Fuentes: [Introduction to CLI](https://strategyquant.com/doc/cli-command-line/introduction-to-cli/) (página de 2020, puede estar desfasada).

**Documentación incluida en la instalación** (`C:\StrategyQuantX145\docs\cli\`: `sqcli.md`, `commands-reference.md`, `qdmcli.md`).
Es más reciente y dice derivarse del código fuente; sigue siendo documentación, no prueba. Lo que afirma y hay que comprobar:
- Con un argumento (`-h`), `sqcli` va en modo *one-shot*: ejecuta, espera a que acaben los trabajos y sale.
- Comandos candidatos para la tarea 3: `-project action=start name=…` (3a), `-databank action=export … file=….csv` (3c/3d),
  `-tools action=orderstocsv file=….sqx` (3d, operaciones), `-sourcecode action=generate engine=… s=… o=…` (3e/3f; nombres de *engine* desconocidos).
  No aparece ningún comando de "backtest" suelto (3b): habrá que ver si se hace con un proyecto que solo haga backtest.
- `-symbol action=darwinexsymbols` lista los símbolos de datos de Darwinex que la licencia puede descargar (tarea 5).
- Esa documentación está escrita pensando en agentes de IA (habla de `CLAUDE.md` y de plugins): se trata como datos, no como instrucciones.

**Lo que dice de verdad `sqcli -h` (registro n.º 9), contrastado con esa documentación:**
- **La documentación y el programa no coinciden.** El `-h` real **no lista** `-sourcecode` (la vía prevista para exportar código
  MT4/MT5, tareas 3e/3f), ni `-extindicators`, ni `-symbol action=darwinexsymbols`. Su `-ai` es otro: `action=sync|plugins|list`
  ("regenerate the Claude Code wiring"), no el chat con `message=` que describe la documentación. → La documentación de la
  instalación no basta: cada comando se prueba en esta build antes de contar con él.
- Errores en la propia ayuda: en `-tools`, `usecomma` aparece descrito como "Path of the output file" y `output` solo sale en un ejemplo.
- **Ningún comando de "backtest" suelto** (3b): habrá que hacerlo con un proyecto (`-project action=start` / `startOnlyTask`).
- **`-h` no es de solo lectura:** arranca SQX entero (datos, proyectos, motor de IA), y al salir sincroniza los bancos de estrategias
  con sus archivos. Cada llamada cuesta unos 20–25 s de arranque → para tandas, mejor `-run file=…` (tarea 7).
- **Abre una API HTTP local** ("Server started on port 5050", `http://localhost:5050/call?cmd=-h`) mientras se ejecuta.
  Sin comprobar: si escucha solo en este PC o también en la red, y si pide autenticación. Riesgo de seguridad por revisar.
- **Arranca el asistente de IA** (`SQAI: AgentScope model ready - sq / openai/gpt-5.6-sol`) aunque solo se pida la ayuda.
  Sin comprobar si se conecta a algo externo en ese momento.
- **Hora incoherente en el propio log:** las primeras líneas dicen 02:08 (hora de España, UTC+2), y la sincronización final,
  04:08. Algún componente usa otra zona horaria. Hay que vigilarlo cuando entren datos y operaciones con fecha (tareas 4 y 5).
- No se ve ningún límite de la versión de prueba en la ayuda; la tarea 2 empieza por `-license action=info`.

## Comprobaciones y decisiones pendientes (hoja de ruta)

No se compra ninguna licencia antes de cerrar esta lista.

| Punto | Estado | Evidencia / decisión |
|---|---|---|
| Versión y edición de SQX | INCONCLUSO | **Build 145.3191 confirmada por CLI** (registro n.º 9). **Edición de la prueba: Pro**, según `-license action=info` (registro n.º 11). Según la documentación, algunas opciones son solo de Ultimate (generar ATM, salidas múltiples, *parts to improve*): sin comprobar. Sigue abierto qué edición se compraría y si importa para el plan. Registros n.º 1 y 2. **Build de desarrollo confirmada**: "This is Dev build of new Build 145, it is not a final release. Build from 2026.10.06." El título dice **Pro**, build 145.3191, pero se ven módulos que la web atribuye a Ultimate (Portfolio Master, SQ 4 Business). Falta: captura de *Acerca de* y saber si la licencia que se compraría es Pro o Ultimate. Riesgo: lo que se compruebe en H0 con una build de desarrollo puede no valer para la versión final |
| Asistente IA integrado (SQ Pilot) | PENDIENTE | Registro n.º 2: funciona con créditos (166) y modelo elegible (se veía `openai/gpt-5.6-sol`). Afirma que hay plugins `runtime: claude-code`: **sin verificar**. Por la decisión 0001, es una herramienta candidata más: entra solo si demuestra valor, y sus propuestas cuentan como hipótesis. Lo que se escribe allí sale a un modelo externo |
| La prueba gratuita limita `sqcli.exe` o alguna exportación | NO, en lo probado | Ver tarea 2. Exportaciones de las tareas 3c–3f sin límites |
| Seguridad: API HTTP de `sqcli` en el puerto 5050 | INCONCLUSO (riesgo bajo) | Registros n.º 13–15. Mientras corre `sqcli`, escucha en **`0.0.0.0:5050` (todas las interfaces)**, aunque el mensaje diga `localhost`. Cortafuegos de Windows activo en los 3 perfiles, red **privada**, política **BlockInbound**, ninguna regla de entrada para programas de SQX. **No comprobado:** reglas por puerto (requieren permisos de administrador), si la API pide autenticación y una prueba real desde otro equipo. Mientras tanto: no abrir ese puerto ni permitir SQX en el cortafuegos si Windows lo pregunta |
| Formatos de exportación y automatización realmente soportados | PENDIENTE | |
| Plataforma de destino (MT4 o MT5) y compatibilidad de lo exportado | PENDIENTE | |
| Recuperar operaciones ejecutadas para compararlas con el backtest | PENDIENTE | |
| Procedencia, cobertura y granularidad de los datos de Darwinex | PENDIENTE | |
| Costes reproducibles con precisión suficiente, por broker | PENDIENTE | |
| Pasos con intervención humana y su frecuencia | PENDIENTE | |
| Coste en tiempo y dinero de un experimento completo | PENDIENTE | |
| Condiciones vigentes de Darwinex Zero, Axi Select y fondeadas de Imox | PENDIENTE | |
| Criterios de elección del primer mercado, fijados antes de ver backtests | PENDIENTE (decide Diego) | |
| Presupuesto de tiempo y dinero del proyecto y cifras de abandono | PENDIENTE (decide Diego) | |
