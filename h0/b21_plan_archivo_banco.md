# B21 – Archivo del banco `Builder/Results` y prueba de no desalojo (plan escrito ANTES de ejecutar)

Fecha: 2026-10-23 · Autor: Claude · Asunto B21 de `PENDIENTES.md`; puerta de la fase 0 de la 0004 (§4). Mismo
procedimiento que B1 y B17: criterios y controles negativos en git antes de la primera orden; si un criterio falla, no
se redefine: se diagnostica aparte.

## Pregunta

¿Podemos (1) sacar de SQX una copia íntegra de las estrategias de `Builder/Results`, (2) comprobar que SQX la lee y da
las mismas métricas, y (3) volver a usar el Builder **sin que desaloje** lo que hay?

Prueba de proceso con datos quemados (familia `H0-proceso`, regla 7). No mira métricas para decidir nada.

## Estado de partida (comprobado el 2026-10-23, antes de escribir este plan)

- `user/projects/Builder/databanks/Results/` tiene **7.003** archivos `.sqx` (y nada más). Los demás bancos del Builder
  (`H0_T7`, `H0_archivo`, `Initial population`, `Last generation`, `Strategies to improve`, `Existing portfolio`): 0.
- Capacidad actual del Builder: `<MaxStrategies>1000</MaxStrategies>` en `Build-Task1.xml` de `project.cfx` (la de
  fábrica, restaurada tras B17). Con 7.003 > 1.000, la próxima generación con esta configuración desalojaría.
- Última exportación conocida del banco: `lab_h0/b17/Results_despues_v3_nulo2.csv` (2026-10-21, tras el último brazo
  de B17).
- SQX cerrado (ningún proceso `java` ni de StrategyQuant en `tasklist`).
- **La exportación es determinista** (registro n.º 223, comprobado antes de fijar A2): las dos exportaciones de B17 del
  mismo estado del banco (`Results_despues_v3_real.csv` y `Results_antes_v3_nulo1.csv`, 5.001 filas) son idénticas
  fila a fila. Sin esto, comparar CSV no probaría nada. (El n.º 223 quedó marcado "sucio" porque este plan aún no
  estaba confirmado; el comparador usado sí lo estaba, commit anterior.)

## Pasos y criterios (fijados ahora)

Todo por el ejecutor con registro (`lab ejecutar`, commit antes y después de cada orden). Guion:
`h0/configs/b21_tanda.sh`. Herramienta: `h0/configs/b21_archivo.py` (12 tests en `tests/test_b21_archivo.py`, con
controles negativos: un byte cambiado, un archivo de menos o de más y una fila duplicada **tienen** que detectarse).
Carpeta de trabajo: `C:\StrategyQuantX145\user\lab_h0\b21\`.

| Paso | Qué | Criterio de aceptación |
|---|---|---|
| 0 | Comprobar que SQX no está abierto; manifiesto **M0** de `Results` (nombre, bytes, SHA-256 de cada `.sqx`) | **A0:** 7.003 archivos. Si SQX está abierto, la tanda no empieza |
| 1 | `-databank action=count` y `action=export` de `Results` | **A1:** SQX cuenta 7.003. **A2:** el CSV tiene 7.003 filas y es **idéntico** (mismas filas, cualquier orden) a `Results_despues_v3_nulo2.csv` de B17: nada ha cambiado el banco desde el 21-10. Si no, **parada** y diagnóstico antes de seguir |
| 2 | Copia byte a byte con Python a `lab_h0\b21\archivo_Results\` (sin pasar por SQX), con su manifiesto | **A3:** 7.003 copiados; 0 que falten, 0 de más, 0 distintos; el origen no cambia durante la copia |
| 3 | Lectura por SQX: `-run` que carga la copia en `Builder/H0_archivo` (vacío, creado en H0 para archivar), sincroniza y cuenta en el mismo proceso; después exportar `H0_archivo` a CSV | **A4:** SQX cuenta 7.003 en `H0_archivo` y hay 7.003 `.sqx` en su carpeta. **A5:** el CSV de `H0_archivo` es idéntico al CSV de `Results` del paso 1. **Control negativo de A5:** el mismo comparador frente a `Results_despues_v3_real.csv` (estado anterior, con menos estrategias) **tiene** que dar DISTINTOS. **A5b:** `Results` sigue idéntico a M0 |
| 4 | Plantilla **de trabajo** con capacidad 100.000 (`b17_preparar_builder.py` sobre el original de fábrica: `USDCHF_B1`, generación aleatoria, N = 50, spread 2, deslizamiento 1, como la calibración de B17); cargarla, comprobar los bloques, generar, exportar `Results` | **A6:** entre 50 y 57 estrategias nuevas (7 hilos, B17) y **ninguna** de antes falta (`b17_analizar.nuevas`). **A7:** las 7.003 de M0 siguen en `Results` **byte a byte** (`b21_archivo.py conservadas`). **A8:** la copia del paso 2 sigue idéntica a M0 |
| 5 | Restaurar la configuración original del Builder y comprobarla | **A9:** 0 diferencias en los bloques `Data`, `WhatToBuild`, `Rankings`, `CrossChecks`, `Options` y `RiskMoneyManagement` frente a `Builder_original_145.3191.cfx`; manifiesto final **M3** de `Results` guardado |

**Control negativo del no desalojo (A6–A7):** ya existe y no se repite (destruiría estrategias): con capacidad 1.000,
SQX desalojó sin avisar en la v1 de B17 (registro n.º 159–181; 17 de las 40 de H0 perdidas). Aquí solo se prueba la
rama que debe conservar.

**Diagnósticos, sin criterio:** si los `.sqx` que SQX escribe en `H0_archivo` son byte a byte iguales a la copia (SQX
puede volver a serializarlos); tiempos de cada paso (exportar, cargar 7.003, generar 50).

## Reglas de decisión

- **A0–A9 se cumplen → B21 cerrado (SÍ):** copia con hash y metadatos, leída en un lugar separado con recuento e
  integridad, y probado que una generación con la plantilla de trabajo no desaloja (0004, fase 0).
- **Falla A2** → parada antes de copiar: algo cambió el banco desde el 21-10; se diagnostica.
- **Falla A3 o A8** → la copia no vale; se rehace en una carpeta nueva (nunca sobrescribir) tras diagnosticar.
- **Falla A4 o A5** → la copia no se lee igual. Si el recuento es exactamente 1.000, la causa probable es la capacidad
  también al cargar: se registra como hallazgo y se diseña otra prueba de lectura con su criterio escrito antes.
- **Falla A6 o A7** → **no** se vuelve a generar con el Builder hasta entenderlo; la fase 1 no empieza.
- Si A7 falla solo por "distintos" (mismos nombres, bytes cambiados), puede ser que SQX reescriba los archivos al
  sincronizar: se diagnostica comparando métricas, sin dar el criterio por cumplido.

## Qué queda para Diego

- **Orden con A14:** B21 escribe en `lab_h0\b21\` y en `h0/evidencias_privadas/`. Esas dos carpetas se copian
  **después** de la tanda (así la copia de A14 incluye el archivo del banco); `LAB_PRIVADO_CURSO` y `LAB_BIBLIOTECA`
  pueden copiarse ya, porque B21 no las toca.
- **Qué hacer con `Results` después:** con el archivo verificado, vaciarlo dejaría cada brazo de la fase 1 en un banco
  limpio. Es borrar estrategias (aunque haya copia): **lo decide Diego**, y no se hace en esta tanda.

## Lo que no demuestra

Que la copia sobreviva fuera de este disco (eso es A14 y la prueba de restauración de B25); que la capacidad funcione
igual con la generación genética o con bancos de cientos de miles (se comprobará con recuentos en cada brazo).
