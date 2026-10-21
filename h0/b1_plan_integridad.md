# B1 – Prueba de integridad exportar/importar por fechas (plan escrito ANTES de ejecutar)

Fecha: 2026-10-21 · Autor: Claude · Asunto B1 de `docs/decisiones/PENDIENTES.md` · Decisión 0003 v6 §1 ("A comprobar en
H0 antes…") y revisión 01.

## Para qué

La 0003 sella exportando por fechas desde una instalación e importando en otra. Si ese camino pierde, duplica, desplaza
o redondea velas, o cambia la hora, el bloque de investigación no sería el que creemos y el examen sellado tampoco.
Esta prueba lo comprueba con los **datos quemados** (decisión 0002), sin tocar Darwinex.

## Datos y herramientas

- Símbolo `USDCHF_M1_dukas` (Dukascopy, M1), ventana **W = 2023.01.01 → 2024.10.30** (la misma de los backtests de H0).
- Órdenes de `sqcli -data` tal como las da su ayuda real (`h0/evidencias/20261020T000832Z_t1_sqcli_ayuda.redactada.txt`):
  `action=export` (`symbols`, `timeframe`, `datefrom`, `dateto`, `outputdir`, `prefix`, `format`, `cFormat`…) y
  `action=import` (`symbol`, `filepath`, `format`, `instrument`, `timeframe`, `timezone`, `errorhandling`).
  Si una opción no funciona como dice la ayuda, se registra y se para: no se prueban nombres a ciegas.
- Formato de comparación (lo fijamos nosotros): `format=Custom`, cabecera `Date,Time,Open,High,Low,Close,Volume`,
  `cFormat=[Date:yyyy.MM.dd],[Time:HH:mm:ss],[Open],[High],[Low],[Close],[Volume]`.
- Comparador propio `h0/configs/b1_comparar_velas.py`, con tests de errores sembrados (`tests/test_b1_comparar_velas.py`).
- Archivos grandes en `C:/StrategyQuantX145/user/lab_h0/b1/` (fuera del repositorio); en el repositorio, sus hashes y
  los resúmenes. Todo por el ejecutor con registro; commit antes de cada ejecución; ninguna otra carga de CPU a la vez.

## Pasos

1. **Inventario** del símbolo (`-symbol action=list`): zona horaria e instrumento declarados.
2. **Exportación de referencia** E_A de W, **dos veces** (repetibilidad).
3. **Límites:** exportación E_B de 2023.06.01 → 2023.06.30. Se anota si `datefrom` y `dateto` son inclusivos y a qué
   hora empieza y acaba; E_B debe ser exactamente el tramo correspondiente de E_A.
4. **Exportación para importar** E_I de W en un formato que `import` acepte (primero el de por defecto de la ayuda).
5. **Importación** de E_I en un símbolo nuevo `USDCHF_B1` (instrumento USDCHF, misma zona horaria que el original,
   `errorhandling=stop`). Se lee el log entero.
6. **Reexportación** E_R de `USDCHF_B1` con los parámetros de E_A y comparación vela a vela.
7. **Mismo backtest antes y después:** las 10 estrategias de H0 (registro n.º 24) en el Retester, una vez con
   `USDCHF_M1_dukas` y otra con `USDCHF_B1`, mismos costes y plantilla (solo cambia el símbolo); operaciones a CSV y
   `comparar_operaciones.py`. Al terminar, el Retester se restaura a su configuración original y se comprueba.

## Controles negativos (sin ellos un "sale igual" no prueba nada)

- **C1 (comparador):** con copias de E_A con un error sembrado cada una — vela eliminada, vela duplicada, precio alterado
  en 1 punto, una vela desplazada 1 minuto, todo desplazado 1 hora — el comparador debe detectar **cada** error, y
  E_A frente a sí misma debe dar 0 diferencias. Primero en tests con datos sintéticos; después con el archivo real.
- **C2 (zona horaria):** importar el mismo E_I en `USDCHF_B1_TZ` con otra zona horaria; la reexportación debe salir
  desplazada y el comparador debe detectarlo. Demuestra que la prueba vería un error de zona horaria.

## Criterios de aceptación (todos, para marcar B1 = SÍ)

| # | Criterio |
|---|---|
| A1 | Las dos exportaciones E_A son idénticas byte a byte |
| A2 | Límites de `datefrom`/`dateto` documentados, y E_B = tramo exacto de E_A |
| A3 | Importación sin errores ni avisos de datos en el log |
| A4 | E_R = E_A vela a vela: 0 ausentes, 0 sobrantes, 0 duplicadas, 0 desplazadas, 0 diferencias de precio o volumen (tras normalizar solo el formato numérico) |
| A5 | Las 10 estrategias dan operaciones **idénticas** con el símbolo original y con el importado |
| A6 | C1 detecta los cinco errores sembrados y C2 detecta el desplazamiento |

Si falla alguno: B1 = NO o INCONCLUSO, se registra, y el método de sellado de la 0003 §1 se replantea por escrito
**antes** de descargar Darwinex. No se cambian estos criterios después de ver los resultados (regla 8); si hubiera que
cambiarlos, se registra como cambio de proceso.

## Lo que esta prueba NO demuestra

Que Darwinex funcione igual (otra fuente; se verá en la ficha C12), que la zona horaria de Darwinex sea la que se espera,
ni que las velas de Dukascopy sean correctas: solo que **exportar e importar** no altera lo que ya hay.
