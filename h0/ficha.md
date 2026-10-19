# H0 – Ficha de viabilidad técnica

SQX según la pantalla de inicio: **"StrategyQuant X Pro Build 145 (Trial license)"**, build **145.3191**, prueba válida hasta el **02-11-2026**
(registro n.º 1, evidencia `h0/evidencias/20261019_sqx_pantalla_inicio.png`).
⚠️ La hoja de ruta decía *Ultimate, build 143.2708*: **no coincide**. Ver la fila "Versión y edición" más abajo.
Inicio de la prueba: 2026-10-19 (quedaban 14 d 00:32 en la captura) · Sistema operativo del PC de SQX: Windows 11 (según Diego)

Estados: **SÍ** / **NO** / **INCONCLUSO** / PENDIENTE (aún no probado).
Regla: solo se marca SÍ o NO con evidencia guardada en `h0/evidencias/` y una entrada en `registry/experimentos.jsonl`.
Si algo no se puede comprobar dentro de la prueba, queda INCONCLUSO; nunca se supone.

## Paso 0 – El banco de trabajo funciona en el PC de SQX

| Comprobación | Estado | Evidencia | Tiempo |
|---|---|---|---|
| `python --version` ≥ 3.10 | PENDIENTE | | |
| `python -m unittest discover -s tests` sin fallos | PENDIENTE | | |
| `python .claude/hooks/guardian.py --autotest` sin fallos | PENDIENTE | | |
| Prueba real: pedir a Claude Code que lea `data/sealed/x` y que el guardián lo bloquee | PENDIENTE | | |

Si el hook no se ejecuta (por ejemplo, porque `python` no está en el PATH), **no hay protección**: se arregla antes de seguir.

## Tareas H0

| # | Tarea | Estado | Evidencia | Tiempo |
|---|---|---|---|---|
| 1 | Localizar `sqcli.exe`, confirmar la build y guardar la salida completa de `sqcli.exe -h` | PENDIENTE | | |
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

## Comprobaciones y decisiones pendientes (hoja de ruta)

No se compra ninguna licencia antes de cerrar esta lista.

| Punto | Estado | Evidencia / decisión |
|---|---|---|
| Versión y edición de SQX | INCONCLUSO | Registro n.º 1. El título dice **Pro**, build 145.3191, pero se ven módulos que la web atribuye a Ultimate (Portfolio Master, SQ 4 Business). Hay un texto parcial "This is Dev build of…" tapado por un diálogo: ¿build de desarrollo? Falta: captura de *About* y del texto completo de la pantalla de inicio, y saber si la licencia que se compraría es Pro o Ultimate (puede cambiar qué hace la CLI) |
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
