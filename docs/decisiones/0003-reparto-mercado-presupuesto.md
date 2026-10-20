# Decisión 0003 – Reparto de los datos, primer mercado, presupuesto y abandono

Fecha: 2026-10-20 · Estado: **PROPUESTA** (redactada por Claude; la decide y aprueba Diego) · Sustituye a: —

> Todo lo de aquí se fija **antes de ver ningún precio de Darwinex ni ningún backtest** del mercado elegido.
> Claude no ha visto precios ni resultados de ninguno de los candidatos con datos de Darwinex.
> Al aprobarla, Diego cambia el estado a ACEPTADA y el protocolo `protocols/2026-10-20_sellado_darwinex.md` se
> completa con ella.

## 1. Reparto de los datos (protocolo de sellado, secciones 3 y 4) – provisional

Provisional hasta verificar la cobertura real de los datos de Darwinex y el tamaño de muestra (revisión 06).

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

Por qué 24 meses: deja 7 años para investigar y un examen razonable. **Corrección (revisión 03):** la primera versión
decía que daría "cientos de operaciones por estrategia"; era una suposición y es falsa para la mitad de los casos. Con
las 20 estrategias de prueba del propio laboratorio (22 meses H1, registros n.º 43 y 82): mediana 75–90 operaciones,
solo la mitad llega a 100 y varias tienen menos de 30. Por eso:

- **Muestra mínima fijada antes del examen:** una candidata con **menos de 100 operaciones en el bloque sellado** recibe
  INCONCLUSO, nunca FAVORABLE. La frecuencia mínima se exige ya en la investigación, como criterio preregistrado.
- Alternativas: 18 meses (más investigación, examen más débil) o 36 meses (examen más fuerte). No se elige mirando datos.

## 2. Primer mercado, puntuado solo con los criterios del protocolo (sección 5)

| Criterio | EURUSD | GBPUSD | XAUUSD (oro) | NDX / DAX |
|---|---|---|---|---|
| Historia en Darwinex desde 2017-10 | Sí | Sí | Sí | NDX y DAX desde 2018-06 |
| Spread por defecto en SQX (n.º 88) | **0,6 pips (el menor)** | 0,8 pips | 28 (puntos) | sin registrar aún |
| Liquidez / horario | Máxima, 24 h | Alta | Alta | Horario de índice |
| Muy minado por usuarios de SQX (hoja de ruta) | No | No | **Sí** | **Sí** |
| Es mercado del curso de Imox | Divisas, fase posterior | Ídem | **Sí** | **Sí** |

**Propuesta: EURUSD, como candidato provisional** (revisión 06): se confirma o se cambia cuando se verifiquen costes
reales de Darwinex Zero, calidad y cobertura de datos y viabilidad técnica; nunca por rentabilidad histórica ni por
seguir el curso. Cumple todos los criterios, tiene el coste por defecto más bajo y no está entre los mercados
que la hoja de ruta marca como muy minados. **La contrapartida** es que el curso empieza por oro, Nasdaq y DAX: si Diego
da más peso a seguir el curso, la alternativa sería XAUUSD, con un coste por defecto mucho mayor. Esa ponderación es de
Diego. (Los costes son valores por defecto de SQX: se contrastan con Darwinex Zero antes de usarlos.)

## 3. Presupuesto y criterios de abandono (hoja de ruta: "se fijan en H0, antes de ver ningún resultado")

- **Dinero:** 0 € de gasto adicional hasta cerrar H0. Comprar la licencia de SQX es una decisión aparte de Diego, con
  la ficha H0 delante (edición, precio y límites comprobados). **Que caduque la prueba el 02-11-2026 no es un motivo
  para comprar.** Precios según la revisión 03 (web oficial, sin verificar por Claude, en USD y sin IVA): Professional
  1.490; Ultimate 2.900 en promoción (4.900 de lista). Se trata como un gasto que quizá no se recupere nunca.
- **Tope de pérdida total y horas semanales: los fija Diego** (pendiente: "¿cuánto dinero adicional estoy dispuesto a
  perder en el proyecto?" y "¿cuántas horas a la semana sin perjudicar otras prioridades?"). Agotado el presupuesto
  sin evidencia suficiente, se detiene o se replantea: **no se amplía por llevar meses trabajando**.
- **Tiempo:** H1 (puente SQX completo con MetaTrader) antes del **2026-12-31**; H2 (motor de validación) antes del
  **2027-03-31**. Si se pasa más de un mes de cualquiera de las dos fechas, se replantea el proyecto por escrito.
- **Presupuesto de búsqueda escalonado** (revisión 03: registrar sin límite no controla el sobreajuste; revisión 06:
  no fijar la cifra definitiva sin conocer el coste de cada lote):
  1. **Piloto** (cifras fijadas ya): 1 familia preregistrada, como máximo **2.000 estrategias generadas** y
     **8 horas de cómputo**, sobre el bloque de investigación. Sirve para medir el coste por lote, la tasa de
     supervivencia a los filtros y los motivos de descarte. **Del piloto no sale ninguna candidata al examen sellado.**
  2. **Fase confirmatoria**: su límite acumulado (estrategias, horas de cómputo y gasto) se fija **por escrito con los
     números del piloto y antes de empezar la búsqueda confirmatoria**; después no se toca. **Techos provisionales**
     que esa cifra no podrá superar sin una nueva decisión: 20 familias, 10.000 estrategias por familia, 100.000 en total.
  3. Como máximo **3 candidatas** llegan al examen sellado.
- **Qué cuenta como prueba:** no solo las estrategias generadas. También cada **variante, filtro y decisión de
  selección** se registra y entra en la corrección por selección (regla 7 y regla 8 de CLAUDE.md).
- **Las fechas son hitos de revisión, no obligación de avanzar** (revisiones 04 y 06): si llega una fecha y faltan
  pruebas, no se pasa de fase; se revisa por escrito la causa y el calendario.
- **Abandono o replanteamiento**, distinguiendo la causa (revisión 06):
  - **Retraso justificable** (p. ej. la muestra crece más despacio de lo previsto): se ajusta el calendario por escrito,
    sin tocar criterios ni presupuesto de búsqueda.
  - **Fallo técnico corregible** (p. ej. el flujo exige más de un paso manual por experimento; hoy: uno): se corrige y se
    repite lo afectado, registrado.
  - **Evidencia de que no hay ventaja** → se detiene o se replantea el enfoque: (a) a 2027-06-30 ninguna estrategia con
    EDGE favorable en datos no sellados; (b) en el examen sellado las candidatas no baten con claridad a las referencias
    comparables; (c) se agota el presupuesto aprobado sin evidencia suficiente. **El presupuesto no se amplía por llevar
    meses trabajando.**
- **El bloque sellado no se usa nunca para seleccionar, modificar ni rescatar estrategias** (revisión 06). Se abre una
  vez para evaluar un procedimiento congelado; si después se cambia algo, ese bloque deja de servir de examen y hay que
  reservar datos nuevos.

## 4. Exigencias de realismo antes de atribuir ventaja (enmienda de la revisión 03)

- Costes efectivos del instrumento **en el vehículo previsto** (Darwinex Zero), no los valores por defecto de SQX.
- **Escenarios de deslizamiento adverso** además del caso base; una ventaja que desaparece con un deslizamiento
  razonable no cuenta.
- No depender de lo que ocurre dentro de una vela H1: toda candidata pasa un retest de **mayor precisión** (datos
  intradía) con resultados coherentes.
- El código exportado (MT4/MT5) **compila y se ejecuta** en la plataforma antes de la demo (pendiente en H0).

## 5. Condiciones previas que no dependen de esta decisión

Antes de descargar un solo precio:
1. **Guardián sin el agujero de PowerShell**, comprobado con una llamada real.
2. **API de SQX en el puerto 5050** (escucha en todas las interfaces): comprobar si pide autenticación y si se alcanza
   desde otro equipo de la red; si se alcanza, bloquearla en el cortafuegos antes de seguir.
3. **Visibilidad del repositorio** (decide Diego): la revisión 03 recomienda hacerlo privado para reducir exposición
   futura (el historial público ya contiene el ID de hardware y el de la licencia de prueba; hacerlo privado no borra
   copias existentes). El ID de licencia de prueba caduca el 02-11-2026; el de hardware no se puede "revocar".

## Historial de esta propuesta (sigue sin aprobar)

| Versión | Cambio | Origen |
|---|---|---|
| 1 | Reparto 7 años / 24 meses, sellado por exportación e instalación aparte, EURUSD, presupuesto y abandono | Claude, tras metadatos de Darwinex (n.º 87–88) |
| 2 | Sellado con dos instalaciones (la opción B sola no bastaba) | Claude, autocorrección |
| 3 | "Cientos de operaciones" corregido con datos propios; muestra mínima de 100; topes de búsqueda; precios de SQX; no comprar por la caducidad; exigencias de realismo; condiciones previas (puerto 5050, repositorio) | Revisión 03 |
| 4 | Presupuesto escalonado (piloto con cifras ya fijadas → confirmatoria con límite fijado con datos del piloto; los topes de la v3 pasan a techos); variantes, filtros y selecciones cuentan como pruebas; fechas como hitos de revisión; causas de abandono distinguidas; el bloque sellado nunca selecciona, modifica ni rescata; reparto y EURUSD provisionales | Revisión 06 |
