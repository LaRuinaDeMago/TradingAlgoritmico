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
| 1 | Localizar `sqcli.exe`, confirmar la build y guardar la salida completa de `sqcli.exe -h` | PENDIENTE (en curso) | Localizado: `C:\StrategyQuantX145\sqcli.exe`, SHA-256 `afa68ccb…a4f`, firma Authenticode **válida** de StrategyQuant s.r.o. (sin número de versión en el ejecutable). 1.er intento, registros n.º 3 y 4: **FALLIDO** aunque devolvió código 0, porque la GUI estaba abierta y SQX solo admite una instancia por instalación. Falta repetir con la GUI cerrada | 15 min |
| 2 | ¿La prueba gratuita limita alguna función de la línea de comandos? | PENDIENTE | | |
| 3a | CLI: lanzar un proyecto de generación | PENDIENTE | | |
| 3b | CLI: ejecutar un backtest | PENDIENTE | | |
| 3c | CLI: exportar estrategias | PENDIENTE | | |
| 3d | CLI: exportar resultados y operaciones a formato legible (CSV u otro) | PENDIENTE | | |
| 3e | CLI: exportar código para MT4 | PENDIENTE | | |
| 3f | CLI: exportar código para MT5 | PENDIENTE | | |
| 4 | Recorrido mínimo: generar, exportar, registrar y reproducir el backtest dos veces con resultados idénticos | PENDIENTE | | |
| 5 | Datos de Darwinex: procedencia, instrumentos, periodo, granularidad y modelo de costes | PENDIENTE | | |
| 6 | Pasos que exigen intervención manual y con qué frecuencia | PENDIENTE | | |
| 7 | Tiempo y coste de un experimento completo de principio a fin | PENDIENTE | | |

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

## Comprobaciones y decisiones pendientes (hoja de ruta)

No se compra ninguna licencia antes de cerrar esta lista.

| Punto | Estado | Evidencia / decisión |
|---|---|---|
| Versión y edición de SQX | INCONCLUSO | Registros n.º 1 y 2. **Build de desarrollo confirmada**: "This is Dev build of new Build 145, it is not a final release. Build from 2026.10.06." El título dice **Pro**, build 145.3191, pero se ven módulos que la web atribuye a Ultimate (Portfolio Master, SQ 4 Business). Falta: captura de *Acerca de* y saber si la licencia que se compraría es Pro o Ultimate. Riesgo: lo que se compruebe en H0 con una build de desarrollo puede no valer para la versión final |
| Asistente IA integrado (SQ Pilot) | PENDIENTE | Registro n.º 2: funciona con créditos (166) y modelo elegible (se veía `openai/gpt-5.6-sol`). Afirma que hay plugins `runtime: claude-code`: **sin verificar**. Por la decisión 0001, es una herramienta candidata más: entra solo si demuestra valor, y sus propuestas cuentan como hipótesis. Lo que se escribe allí sale a un modelo externo |
| La prueba gratuita limita `sqcli.exe` o alguna exportación | PENDIENTE | |
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
