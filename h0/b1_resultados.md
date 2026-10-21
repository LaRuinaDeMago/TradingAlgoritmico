# B1 – Resultados de la prueba de integridad exportar/importar (plan: `h0/b1_plan_integridad.md`)

Fecha: 2026-10-21 · Registros n.º 93–135 · SQX 145.3191-dev · Datos quemados `USDCHF_M1_dukas` (decisión 0002),
ventana W = 2023.01.01–2024.10.30. Archivos grandes en `C:/StrategyQuantX145/user/lab_h0/b1/`; aquí, evidencias y hashes.

## Veredicto: **B1 = NO** según sus criterios. Las causas están identificadas y son corregibles por procedimiento.

| # | Criterio | Resultado | Evidencia |
|---|---|---|---|
| A1 | Dos exportaciones idénticas | **SÍ**: byte a byte, SHA-256 `38da49f1…71d8`, 678.024 velas | n.º 96–97 |
| A2 | Límites documentados; E_B = tramo de E_A | **SÍ**: `datefrom` y `dateto` **inclusivos por días completos** (00:00–23:59 en la hora del símbolo); 31.408 velas idénticas | n.º 98–99 |
| A3 | Importación sin errores | **SÍ**: 678.024 filas importadas = filas del archivo. Salvedad: SQX dice "Invalid csv rows will be ignored" aunque se pida `errorhandling=stop` → podría descartar filas en silencio | n.º 101–102 |
| A4 | E_R = E_A vela a vela | **NO**: precios idénticos en las 678.024 velas; **111 volúmenes distintos** = exactamente las 111 velas con volumen > 2.147.483.647 (2³¹−1), **recortadas a ese máximo al importar** (el archivo intermedio lo tiene completo; máximo original 6,73·10⁹) | n.º 103–105 |
| A5 | Operaciones idénticas con el símbolo original y el importado | **NO**: 0 de 10 idénticas byte a byte (el CSV lleva el nombre del símbolo y el número de orden: esa comparación no podía pasar, defecto del plan). Diagnóstico (n.º 122, posterior a ver los datos): sin ticket, símbolo ni saldo, **18 operaciones solo en el original, todas abiertas entre el 2023-01-02 y el 2023-01-06**; 0 solo en el importado; **las 1.335 siguientes, idénticas**. Causa: calentamiento de indicadores (el original tiene historia anterior a 2023; el importado empieza en seco). El recorte de volumen no cambió ninguna operación | n.º 106–122 |
| A6 | C1 detecta los cinco errores; C2 detecta el desplazamiento | **C1 SÍ** (copia sin tocar idéntica; los cinco errores detectados en el archivo real, n.º 123). **C2 NO tal como se diseñó**: `timezone` en la importación **es solo una etiqueta** (no convierte las horas); la reexportación sale igual; se detecta en la zona declarada (`-symbol action=list`: EETUS frente a UTC, n.º 127). Además, la etiqueta distinta **no cambia el backtest**: 1.335 operaciones idénticas (n.º 128–135) | n.º 124–135 |

Otras observaciones registradas: la importación **exige** `format` aunque la ayuda lo da por opcional (n.º 101,
FALLIDO); `-symbol action=list csv=true` dice "Data listed" sin imprimir nada (n.º 93), y sin `csv` funciona (n.º 94);
SQX ajusta la fecha de inicio del backtest al primer dato del símbolo (2023.01.01 → 2023.01.02). El Retester quedó
restaurado y comprobado (0 diferencias, n.º 120 y 134). Se crearon en SQX los símbolos `USDCHF_B1` y `USDCHF_B1_TZ` y el
banco `Retester/H0_B1` (familia `H0-proceso`); no se borró nada.

## Consecuencias para el método de sellado (0003 §1) — a escribir en el protocolo antes de Darwinex

1. **Calentamiento:** ningún backtest empieza en el primer dato importado. Todo archivo importado lleva un **margen
   previo** y los backtests empiezan después de él. En la instalación de examen se importan investigación + sellado
   (los datos de investigación no son secretos), de modo que el bloque sellado nunca empieza en seco.
2. **Volumen:** antes de importar, comprobar el volumen máximo del archivo; si supera 2³¹−1, registrarlo y decidir
   antes de seguir (ninguna estrategia que use volumen puede evaluarse con esos datos sin corregirlo).
3. **Recuento tras cada importación:** filas del archivo = filas importadas = velas reexportadas (SQX podría descartar
   filas en silencio).
4. **Zona horaria:** la etiqueta no convierte ni avisa. Comprobar (a) la zona declarada tras importar y (b) **el reloj
   real de los datos con una referencia externa** (apertura y cierre semanal del mercado, cambios de horario de EE. UU.
   y Europa) antes de usar reglas por hora. Esto pasa a ser parte obligatoria de B4 y de la ficha C12.
5. **Comparación de operaciones:** sin ticket, símbolo ni saldo (`b1_diagnostico_operaciones.py`).

## B1-bis (cambio de proceso, regla 8): escrito ANTES de ejecutarlo

Motivo: el punto 1 se apoya en un análisis hecho después de ver los datos. Se convierte en prueba: mismas 10
estrategias, mismas plantillas, **inicio del backtest 2023.02.01** (un mes de margen dentro de la ventana quemada; no
se usan datos nuevos) con `USDCHF_M1_dukas` y con `USDCHF_B1`.
**Criterio A5-bis:** con `b1_diagnostico_operaciones.py`, 0 operaciones solo en un lado y todas las comunes idénticas
en las 10 estrategias. Si no, el punto 1 no basta y se investiga antes de Darwinex.

### Resultado de B1-bis (registros n.º 136–148): **A5-bis = SÍ**

Las 10 estrategias dan **1.277 operaciones idénticas** con el símbolo original y con el importado (0 solo en un lado);
las plantillas se cargaron sin diferencias (sin ajuste de fecha) y el Retester quedó restaurado (0 diferencias). Con un
margen de calentamiento de un mes, exportar e importar **no cambia el backtest**. El mes basta para estas estrategias
(todas sus diferencias acababan el 2023-01-06); para indicadores más largos el margen se fija con su periodo máximo.
Nota de procedimiento: Diego cortó en el chat la orden que lanzó esta tanda, pero el proceso ya había arrancado y
terminó solo; se dejó acabar para no dejar el Retester sin restaurar, y se verificó entero.

## Estado final de B1

Los puntos que fallaron (A4 volumen, A5 calentamiento, C2 diseño) tienen causa demostrada y remedio de procedimiento,
y el del calentamiento ya está **probado** (B1-bis). El método de sellado de la 0003 §1 sigue siendo válido **con los
cinco requisitos de arriba**, que pasan al protocolo de sellado. Queda abierto: el volumen y el reloj real de los datos
de Darwinex (ficha C12 y B4).
