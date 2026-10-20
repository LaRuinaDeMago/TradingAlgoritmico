# Decisión 0003 – Reparto de los datos, primer mercado, presupuesto y abandono

Fecha: 2026-10-20 · Estado: **PROPUESTA** (redactada por Claude; la decide y aprueba Diego) · Sustituye a: —

> Todo lo de aquí se fija **antes de ver ningún precio de Darwinex ni ningún backtest** del mercado elegido.
> Claude no ha visto precios ni resultados de ninguno de los candidatos con datos de Darwinex.
> Al aprobarla, Diego cambia el estado a ACEPTADA y el protocolo `protocols/2026-10-20_sellado_darwinex.md` se
> completa con ella.

## 1. Reparto de los datos (protocolo de sellado, secciones 3 y 4)

| Bloque | Periodo | Uso |
|---|---|---|
| Investigación | 2017-10-01 → 2024-09-30 (7 años) | Generar, seleccionar y validar (walk-forward dentro del bloque) |
| **Sellado** | 2024-10-01 → fecha de descarga (~24 meses) | Examen final, una sola vez |
| Prospectivo | después de la descarga | Demo (H4) |

**Cómo se sella.** La documentación indica que Darwinex no admite descargar hasta una fecha (registro n.º 88): cualquier
instalación que descargue tendrá dentro el bloque sellado. Propuesta, con dos instalaciones de SQX:

1. **Instalación de examen** (nueva, solo para esto): descarga toda la historia de Darwinex del mercado elegido.
2. Desde ella, `-data action=export … datefrom=2017.10.01 dateto=2024.09.30` → archivo de **investigación**;
   y `datefrom=2024.10.01` → archivo **sellado**, que se cifra (7-Zip AES-256, contraseña solo de Diego), se registra
   su SHA-256 y se elimina la copia en claro. Nadie mira su contenido.
3. **Instalación de investigación** (la actual): `-data action=import` del archivo de investigación. Nunca tiene el
   bloque sellado.

**A comprobar en H0 antes (con los datos quemados de USDCHF, sin Darwinex):** que la exportación con fechas respeta
exactamente los límites, que la importación reproduce los mismos datos (mismo backtest antes y después) y el formato
de archivo que conserva la zona horaria. Si algo falla, se replantea por escrito antes de descargar.

Por qué 24 meses: con estrategias H1 da del orden de cientos de operaciones por estrategia (intervalo útil) y deja 7
años para investigar. Alternativas: 18 o 36 meses.

## 2. Primer mercado, puntuado solo con los criterios del protocolo (sección 5)

| Criterio | EURUSD | GBPUSD | XAUUSD (oro) | NDX / DAX |
|---|---|---|---|---|
| Historia en Darwinex desde 2017-10 | Sí | Sí | Sí | NDX y DAX desde 2018-06 |
| Spread por defecto en SQX (n.º 88) | **0,6 pips (el menor)** | 0,8 pips | 28 (puntos) | sin registrar aún |
| Liquidez / horario | Máxima, 24 h | Alta | Alta | Horario de índice |
| Muy minado por usuarios de SQX (hoja de ruta) | No | No | **Sí** | **Sí** |
| Es mercado del curso de Imox | Divisas, fase posterior | Ídem | **Sí** | **Sí** |

**Propuesta: EURUSD.** Cumple todos los criterios, tiene el coste por defecto más bajo y no está entre los mercados
que la hoja de ruta marca como muy minados. **La contrapartida** es que el curso empieza por oro, Nasdaq y DAX: si Diego
da más peso a seguir el curso, la alternativa sería XAUUSD, con un coste por defecto mucho mayor. Esa ponderación es de
Diego. (Los costes son valores por defecto de SQX: se contrastan con Darwinex Zero antes de usarlos.)

## 3. Presupuesto y criterios de abandono (hoja de ruta: "se fijan en H0, antes de ver ningún resultado")

- **Dinero:** 0 € de gasto adicional hasta cerrar H0. Comprar la licencia de SQX es una decisión aparte de Diego, con
  la ficha H0 delante (edición, precio y límites comprobados).
- **Tiempo:** H1 (puente SQX completo con MetaTrader) antes del **2026-12-31**; H2 (motor de validación) antes del
  **2027-03-31**. Si se pasa más de un mes de cualquiera de las dos fechas, se replantea el proyecto por escrito.
- **Hipótesis:** antes de abrir el bloque sellado, como máximo **20 familias de hipótesis preregistradas**; todas las
  estrategias generadas se cuentan (regla 7) y entran en la corrección por selección.
- **Ejecuciones de SQX:** sin límite numérico mientras cada una quede registrada; se revisa al cerrar H1.
- **Abandono o replanteamiento** si: (a) el flujo exige más de un paso manual por experimento (hoy: uno, cerrar la
  interfaz); (b) a 2027-06-30 ninguna estrategia tiene EDGE favorable en datos no sellados; (c) en el examen sellado las
  aprobadas no baten con claridad a las referencias comparables; (d) se superan las fechas de arriba.

## 4. Condición previa que no depende de esta decisión

Antes de descargar un solo precio: **guardián sin el agujero de PowerShell**, comprobado con una llamada real.
