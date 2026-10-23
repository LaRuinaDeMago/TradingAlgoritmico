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

---

## Resultado de la primera tanda y enmienda B21-bis (escrita el 2026-10-23, ANTES de cualquier orden nueva)

### Qué pasó (registro n.º 224–238)

| Criterio | Resultado | Registro |
|---|---|---|
| A0 7.003 `.sqx` | **SÍ** (224.406.772 bytes) | 224 |
| A1 SQX cuenta 7.003 | **SÍ** | 225 |
| A2 CSV igual al último de B17 | **SÍ** (7.003 filas idénticas: métricas sin cambios desde el 21-10) | 226–227 |
| A3 copia byte a byte | **SÍ** (0 faltan, 0 sobran, 0 distintos; origen estable) | 228 |
| A4 7.003 en `H0_archivo` | **SÍ** al cargar (SQX cuenta 7.003 y hay 7.003 `.sqx`) | 230–231 |
| A5 CSV de `H0_archivo` igual al de `Results` | **NO**: 6.406 filas frente a 7.003 (las 6.406 idénticas) | 232–233 |
| A5b–A9 | **No ejecutados** (la tanda se paró en A5, antes de tocar la configuración del Builder) | — |

**Causa de A5 (demostrada):** al arrancar para exportar, SQX cargó `Results` (7.003) y después `H0_archivo`; al llegar
a 6.406 se quedó sin memoria ("Memory usage is too high (92%)", n.º 232) y, **al salir, sincronizó la carpeta con lo
que tenía en memoria y borró 597 archivos de `H0_archivo` sin avisar** ("removed 597"). La línea de comandos tiene
**4 GiB** de memoria de Java (`sqcli.config`: `-Xms4g`, sin `-Xmx`) y la interfaz **8 GiB** (`-Xmx8g`) (n.º 238).
No es un defecto de la copia: las 6.406 cargadas tienen el mismo contenido que la copia (n.º 237) y nuestra copia está
intacta (n.º 235).

**Defecto de este plan (demostrado):** A5b, A7 y A8 comparaban archivos byte a byte, pero **SQX reescribe todos los
`.sqx` en cada arranque** (son zip y cada archivo interno lleva la fecha del guardado): 7.003 "distintos" tras un
simple recuento (n.º 234). En cambio, el **contenido** (nombre y SHA-256 de cada archivo interno) de `Results` coincide
con la copia en las 7.003, tras cuatro reescrituras (n.º 236). → Los criterios pasan a ser **por contenido**
(`b21_archivo.py contenido`, con tests que detectan una operación cambiada o un archivo interno de más).

**Hallazgo útil para C13:** cada `.sqx` guarda dentro `dailyEquity.bin` y `orders.bin` (curva diaria y operaciones).
Hipótesis por comprobar: que de ahí se puedan leer las series de todas las estrategias probadas.

### Riesgo nuevo (el más grave visto con SQX)

Si SQX no puede cargar un banco por memoria, **al salir borra de la carpeta lo que no cargó**. Le ha pasado a una copia
de prueba; podría pasarle a `Results` (los originales) si un proyecto acumula más estrategias de las que caben en 4 GiB.
Hoy el Builder tiene 7.003 + 6.406 = 13.409: **ninguna orden más al Builder** hasta sacar `H0_archivo` de SQX.

### Pasos de B21-bis y criterios (fijados ahora)

| Paso | Qué | Criterio |
|---|---|---|
| 0 | Sin arrancar SQX: copiar las 6.406 de `H0_archivo` a `lab_h0\b21\H0_archivo_parcial\` (verificada), y **solo si la copia es idéntica**, quitar los `.sqx` de la carpeta del banco | **B0:** copia de 6.406 idéntica; carpeta del banco con 0 `.sqx` |
| 1 | **Si Diego aprueba A24** (memoria de `sqcli` a 8 GiB, como la interfaz): guardar `sqcli.config` original en `lab_h0\b21\`, añadir `option -Xmx8g` y medir | **B1:** `b21_heap.py` da 8,00 GiB para `sqcli.config`; el resto del archivo, idéntico al original |
| 2 | Lectura: `-run` que carga `archivo_Results` en `H0_archivo`, sincroniza y cuenta; después exportar `H0_archivo` | **B2:** 7.003 contadas y 7.003 `.sqx`; **ninguna línea "failed" ni "Memory usage" en ninguna evidencia del paso**; CSV idéntico a `Results_B21.csv`; contenido de `H0_archivo` = contenido de la copia (7.003). Control negativo: el CSV frente a `Results_despues_v3_real.csv` da DISTINTOS |
| 3 | Sin arrancar SQX: sacar otra vez las 7.003 de `H0_archivo` como en el paso 0 (la copia ya existe; se comprueba por contenido antes de quitar) | **B3:** carpeta del banco con 0 `.sqx`; contenido de `Results` = copia |
| 4 | Plantilla de trabajo con capacidad 100.000, generar 50 (como A6) | **B4 = A6:** 50–57 nuevas, ninguna de antes falta. **B5 (sustituye a A7):** contenido de las 7.003 de la copia presente en `Results`. **B6 (sustituye a A8):** la copia, byte a byte, igual a su manifiesto (SQX no la toca). Ninguna línea "failed" ni "Memory usage" |
| 5 | Restaurar la configuración del Builder | **A9** sin cambios |

**Si Diego no aprueba A24:** los pasos 2–3 no se hacen con el Builder (cargar dos bancos de 7.003 no cabe en 4 GiB).
B21 se cierra con lo demostrado (copia íntegra con hash y contenido verificado; SQX contó las 7.003 al cargarlas) y
la lectura completa por SQX pasa a la prueba de restauración de B25, en un banco vacío.

**Regla nueva para todas las tandas** (también la fase 1): antes de cada orden de SQX, contar lo que tiene cargado el
proyecto; después, buscar "failed" y "Memory usage" en la evidencia y volver a contar archivos. Ningún proyecto con más
estrategias de las que se hayan cargado sin error con la memoria vigente.

### Antes de lanzar B21-bis (2026-10-23)

- **A24 aprobado por Diego** ("vamos a aprobarlo si a ti también te parece lo correcto"; Claude lo recomendó).
- Guion: `h0/configs/b21bis_tanda.sh`; cambio de memoria: `h0/configs/b21_memoria.py` (7 tests: copia del original,
  una sola línea, respeta el salto de línea del archivo, no sobrescribe, restaura exacto). Para deshacerlo:
  `python -I h0/configs/b21_memoria.py restaurar C:/StrategyQuantX145/sqcli.config <lab_h0>/b21/sqcli.config.original`.
- **Cómo se sabe que el cambio surte efecto:** `sqcli.exe` arranca Java dentro de su propio proceso (el registro del
  lanzador solo dice "Invoking main class"), así que no se puede leer `-Xmx` en su línea de comandos. La prueba es de
  comportamiento: el paso 2 repite **la misma carga y exportación** que falló con 4 GiB (n.º 232), que hace de control.
- El guion **se para** si una evidencia de SQX contiene "failed" o "Memory usage" (comprobado antes: de 30 evidencias
  de B17 v3 y B21, solo la del fallo de memoria las contiene), y si B1 no da 8,00 GiB con el archivo original intacto.
- Medición para C23 (sin criterio): memoria de `sqcli.exe` cada 2 s en `lab_h0\b21\memoria_sqcli.csv`.
- **Primer intento (n.º 244–245): parada correcta en B1.** `sqcli.config` mezcla saltos CRLF (6 líneas) y LF (las 2
  últimas); el script añadió una línea en blanco de más y la comprobación "una sola línea añadida" paró la tanda antes
  de arrancar SQX. Se restauró el original (hash `cc75c454…`, n.º 245), se corrigió el script con dos tests nuevos
  (saltos mezclados; repetible si la copia guardada es el archivo vigente) y se ensayó sobre una copia del archivo real:
  una sola línea. Los criterios no cambian.

### Resultado de B21-bis (n.º 246–265) y criterio B2c (escrito ANTES de probarlo)

B1, B3, B4, B5, B6 y A9: **SÍ**. B2: **SÍ** en archivos (7.003), CSV (7.003 filas idénticas; control negativo
DISTINTOS: 7.003 frente a 5.001), contenido (7.003 en `H0_archivo` y en `Results`) y memoria (la exportación con
14.006 estrategias, que con 4 GiB falló en el n.º 232, con 8 GiB carga 7.003 + 7.003 y no quita ninguna, n.º 250);
**NO en el recuento**: la orden `count` dio **6.747** porque se ejecutó en el mismo proceso que la carga, que es
asíncrona ("Records: 6747" antes de "Strategies loaded", n.º 248). Carrera ya vista el 2026-10-20; el `-run` no la
evitaba. No se redefine: se prueba un criterio nuevo.

**B2c (restauración y recuento sin carrera):** con SQX cerrado, se reponen los 7.003 `.sqx` de la copia en la carpeta
vacía de `Builder/H0_archivo` (`b21_archivo.py reponer`, que se niega si la carpeta tiene algún `.sqx` y comprueba la
copia byte a byte); después, **una orden `count` sola** (sin `load` en el mismo proceso). Criterios: la evidencia
contiene "Loaded 7003 strategies to databank H0_archivo" y "Records: 7003", y no contiene "failed" ni "Memory usage";
el contenido de la copia está en `H0_archivo` (7.003); al final se retira otra vez (`retirar`, carpeta en 0). Es el
camino de una restauración real (B25). Control: el mismo recuento con la carga en el mismo proceso dio 6.747 (n.º 248).

### Resultado de B2c (n.º 266–273) y siguiente paso (escrito ANTES de ejecutarlo)

- **Reposición: SÍ** (7.003 copiadas a la carpeta vacía, idénticas byte a byte, n.º 266).
- **Recuento sin carrera: SÍ** ("Loaded 7003 strategies to databank H0_archivo", "Records: 7003", sin "failed" ni
  "Memory usage", 0 quitadas; 14.056 estrategias en el proyecto con 8 GiB, n.º 267).
- **Contenido: NO** (7.003 distintas, n.º 268). Diagnóstico (n.º 269–273): solo cambia `settings.xml`; las reglas
  (`strategy_Portfolio.xml`), operaciones (`orders.bin`) y curvas (`dailyEquity.bin`) son idénticas. Dentro de
  `settings.xml` cambian los **15 bloques `SQStats`** (estadísticas serializadas en binario y en base64); los archivos
  miden lo mismo (34.643 bytes en el ejemplo) y los nombres de las estadísticas aparecen en otro orden. **Lo mismo le
  ha pasado a `Results`** frente a la copia (7.003, n.º 270), que en el n.º 261 era igual: entre medias solo se
  restauró la configuración de fábrica del Builder (n.º 263) y SQX arrancó con ella. Lo retirado en B2 sigue igual
  que la copia (n.º 271) y la copia, intacta (n.º 272). Hipótesis: SQX vuelve a serializar las estadísticas al
  arrancar con otra configuración del proyecto. **No demostrado** que los valores sean los mismos.
- **Siguiente (diagnóstico, sin criterio nuevo para B2c):** exportar `H0_archivo` a CSV y compararlo con
  `Results_B21.csv` (las métricas tal como las da SQX, que es lo que se usa para filtrar); después retirar
  `H0_archivo` a `lab_h0\b21\H0_archivo_ter`, como prevé B2c. B2c queda **NO en el contenido**; el cierre de B21 se
  decide con lo demostrado en B2 (contenido idéntico tras `load`), B2c (recuento) y B4–B6, y se dice así.
