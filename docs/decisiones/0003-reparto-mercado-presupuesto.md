# Decisión 0003 – Reparto de los datos, primer mercado, presupuesto y abandono

Fecha: 2026-10-20 · Estado: **ACEPTADA (versión 6)** el 2026-10-21 por Diego, por delegación explícita en el chat
("A1 Si crees que es lo mejor aprobar 0003 vamos con ello"; también delegó A19, A20 y A21 y respondió A2 y A3), con la
recomendación de Claude, que la redactó · Sustituye a: — · Cambiarla exige una decisión nueva que cite a esta.

> Todo lo de aquí se fija **antes de ver ningún precio de Darwinex ni ningún backtest** del mercado elegido.
> Claude no ha visto precios ni resultados de ninguno de los candidatos con datos de Darwinex.
> Al aprobarla, Diego cambia el estado a ACEPTADA y el protocolo `protocols/2026-10-20_sellado_darwinex.md` se
> completa con ella.

## 1. Reparto de los datos (protocolo de sellado, secciones 3 y 4)

La **regla** queda fijada; la fecha exacta de corte se calcula con ella antes de descargar (revisión 06: cobertura y
muestra por verificar).

| Bloque | Periodo | Uso |
|---|---|---|
| Investigación | 2017-10-01 → día anterior al **inicio del sellado** | Generar, seleccionar y validar (walk-forward dentro del bloque) |
| **Sellado** | **inicio del sellado** → fecha de descarga | Examen final, una sola vez |
| Prospectivo | después de la descarga | Demo (H4) |

**Inicio del sellado (v6).** El primer día del mes siguiente a la **fecha de mercado más tardía que aparezca en el
material del curso de Imox** (configuraciones, vídeos y capturas), para **cualquier** instrumento (mismo corte para
todos: protocolo §3), y **nunca antes del 2024-10-01**. Motivo: Diego tiene el curso y Claude lo está transcribiendo; lo
que ya se ha visto no se puede sellar. El zip del curso se empaquetó el **2026-01-12** y sus configuraciones usan datos de
Darwinex hasta al menos **2025-03**, que caen dentro del corte anterior (2024-10-01). La fecha se obtiene de la revisión
completa del curso (B11), se registra con sus evidencias (solo fechas y hashes) y se fija **antes de descargar**.
Si a la fecha de descarga el bloque sellado tiene **menos de 18 meses**, el examen se completa con el periodo
**prospectivo** en demo, con una duración mínima fijada antes de empezarlo. No se recorta el bloque de investigación
para compensar.

**Conocimiento previo que no se puede sellar (v6).** Claude, entrenado con datos hasta 2026-06, y Diego conocen a grandes
rasgos lo que hicieron los mercados en 2024–2026. Por eso: (a) las candidatas salen de **procedimientos mecánicos
preregistrados** sobre el bloque de investigación, no de ideas elegidas sabiendo lo que pasó después; (b) toda hipótesis
propuesta por una persona o una IA se registra con la marca "posible conocimiento posterior"; (c) el único examen
totalmente limpio es el **prospectivo** (datos que no existían al congelar la candidata).

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

Por qué 24 meses (v1–v5; desde la v6 la longitud la da la regla de arriba y puede ser menor): deja 7 años para
investigar y un examen razonable. **Corrección (revisión 03):** la primera versión
decía que daría "cientos de operaciones por estrategia"; era una suposición y es falsa para la mitad de los casos. Con
las 20 estrategias de prueba del propio laboratorio (22 meses H1, registros n.º 43 y 82): mediana 75–90 operaciones,
solo la mitad llega a 100 y varias tienen menos de 30. Por eso:

- **Muestra mínima fijada antes del examen:** una candidata con **menos de 100 operaciones en el bloque sellado** recibe
  INCONCLUSO, nunca FAVORABLE. La frecuencia mínima se exige ya en la investigación, como criterio preregistrado.
  **Necesaria, no suficiente** (revisión 09): 100 operaciones no son 100 observaciones independientes (dependencia
  temporal, rachas, un mismo régimen). La muestra útil se justifica antes del examen con la frecuencia, la variabilidad y
  la dependencia de las candidatas y con la ventaja mínima económicamente relevante.
- Alternativas: 18 meses (más investigación, examen más débil) o 36 meses (examen más fuerte). No se elige mirando datos.

## 2. Primer mercado, puntuado solo con los criterios del protocolo (sección 5)

| Criterio | EURUSD | GBPUSD | XAUUSD (oro) | NDX / DAX |
|---|---|---|---|---|
| Historia en Darwinex desde 2017-10 | Sí | Sí | Sí | NDX y DAX desde 2018-06 |
| Spread por defecto en SQX (n.º 88) | **0,6 pips (el menor)** | 0,8 pips | 28 (puntos) | sin registrar aún |
| Liquidez / horario | Máxima, 24 h | Alta | Alta | Horario de índice |
| Muy minado por usuarios de SQX (hoja de ruta) | No | No | **Sí** | **Sí** |
| Es mercado del curso de Imox | Divisas, fase posterior | Ídem | **Sí** | **Sí** |

**Decisión (v6, A19): EURUSD.** Queda confirmada salvo que la ficha de datos y costes del instrumento (C12) muestre un
problema de costes reales en Darwinex Zero, de cobertura o de calidad de datos; en ese caso se pasa a GBPUSD con los
mismos criterios. Nunca se cambia por rentabilidad histórica ni por seguir el curso. Razón añadida en v6: cotiza en USD,
así que en un backtest en USD el resultado no depende del tipo de cambio fijo que SQX parece usar en los pares que no
cotizan en USD (hipótesis B7). Cumple todos los criterios, tiene el coste por defecto más bajo y no está entre los mercados
que la hoja de ruta marca como muy minados. **La contrapartida** es que el curso empieza por oro, Nasdaq y DAX: si Diego
da más peso a seguir el curso, la alternativa sería XAUUSD, con un coste por defecto mucho mayor. Esa ponderación es de
Diego. (Los costes son valores por defecto de SQX: se contrastan con Darwinex Zero antes de usarlos.)

## 3. Presupuesto y criterios de abandono (hoja de ruta: "se fijan en H0, antes de ver ningún resultado")

- **Dinero:** 0 € de gasto adicional hasta cerrar H0. Comprar la licencia de SQX es una decisión aparte de Diego, con
  la ficha H0 delante (edición, precio y límites comprobados). **Que caduque la prueba el 02-11-2026 no es un motivo
  para comprar.** Precios según la revisión 03 (web oficial, sin verificar por Claude, en USD y sin IVA): Professional
  1.490; Ultimate 2.900 en promoción (4.900 de lista). Se trata como un gasto que quizá no se recupere nunca.
- **Capital real (A2, v6): 0 €** hasta superar la demo (H4) con criterios preregistrados. Diego: "primero usaremos
  cuentas demo". El tope de pérdida con dinero real se fija por escrito **antes** de H5. Gasto del proyecto: 0 €
  adicional; cualquier compra (licencia, A12; datos; VPS) es una decisión aparte de Diego.
- **Horas (A3, v6):** variables; no hay compromiso semanal. Se **registran** las horas humanas por fase, porque son
  coste del proyecto (objetivo C) y del piloto. Las fechas de H1 y H2 siguen siendo hitos de revisión.
- **Prioridad (A20, v6): rigor con presupuesto de tiempo por fase.** El rigor no se negocia en lo que decide (datos,
  selección, examen y registro); cuando falta tiempo se **recorta el alcance**, nunca el rigor. Aprender es un
  subproducto que se registra (`aprendizaje/`), no un motivo para gastar más. Usar Claude Code y Opus para optimizar
  el proceso entra igual que cualquier herramienta: se queda donde demuestre que mejora el resultado (decisión 0001).
- Agotado el presupuesto sin evidencia suficiente, se detiene o se replantea: **no se amplía por llevar meses
  trabajando**.
- **Tiempo:** H1 (puente SQX completo con MetaTrader) antes del **2026-12-31**; H2 (motor de validación) antes del
  **2027-03-31**. Si se pasa más de un mes de cualquiera de las dos fechas, se replantea el proyecto por escrito.
- **Presupuesto de búsqueda escalonado** (revisión 03: registrar sin límite no controla el sobreajuste; revisión 06:
  no fijar la cifra definitiva sin conocer el coste de cada lote):
  1. **Piloto** (cifras fijadas ya): 1 familia preregistrada, como máximo **2.000 estrategias generadas** y
     **8 horas de cómputo**, sobre el bloque de investigación. Sirve para medir el coste por lote, la tasa de
     supervivencia a los filtros y los motivos de descarte. **Del piloto no sale ninguna candidata al examen sellado.**
     Método de medición (revisión 09): **tres tamaños de lote**; tiempos separados de arranque, generación, validación,
     optimización y exportación; **coste por estrategia válida para el análisis** (no por estrategia generada); y el
     **tiempo humano** de revisión. También mide si SQX permite conservar todas las estrategias probadas (C13).
     **Antes del piloto (v6):** se preregistran las **referencias comparables** (C20): no operar, una regla de
     tendencia con parámetros fijados sin optimizar y entradas al azar con la misma exposición y costes. Cada una cuenta
     como hipótesis. **Dentro del piloto (v6):** el **control negativo** (B17), la misma búsqueda sobre datos
     sintéticos sin ventaja; si encuentra en el ruido estrategias tan buenas como en los datos reales, los filtros no
     discriminan y no se pasa a la fase confirmatoria sin cambiarlos (cambio registrado, regla 8).
  2. **Fase confirmatoria**: su límite acumulado (estrategias, horas de cómputo y gasto) se fija **por escrito con los
     números del piloto y antes de empezar la búsqueda confirmatoria**; después no se toca. **Techos provisionales**
     que esa cifra no podrá superar sin una nueva decisión: 20 familias, 10.000 estrategias por familia, 100.000 en total.
  3. Como máximo **3 candidatas** llegan al examen sellado. **Preferible una candidata principal** (o una cartera definida
     por reglas previas). Si son varias, el examen **es una prueba múltiple** y se corrige como tal; nunca se examinan
     varias para quedarse con la mejor y llamarla "fuera de muestra" (revisión 09). Las candidatas, su código, costes y
     métricas se congelan con hashes antes de abrir el bloque.
  4. Límites de **cómputo, evaluaciones y tiempo humano** con **parada automática** al alcanzar cualquiera.
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
    **preregistradas** (C20); (c) se agota el presupuesto aprobado sin evidencia suficiente; (d) **v6, A7:** aun con
    ventaja estadística, lo esperable no compensa el coste total del proyecto (licencias, datos, horas, capital
    inmovilizado y coste de oportunidad frente a una alternativa sencilla). Se juzgan por separado tres objetivos:
    A ventaja estadística, B rentabilidad neta explotable, C que el proyecto compense. **El presupuesto no se amplía por llevar
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
1. **Guardián sin el agujero de PowerShell**, comprobado con una llamada real. **Cumplida el 2026-10-21** (registros
   n.º 90 y 91).
2. **API de SQX en el puerto 5050** (escucha en todas las interfaces): comprobar si pide autenticación y si se alcanza
   desde otro equipo de la red; si se alcanza, bloquearla en el cortafuegos antes de seguir.
3. **Visibilidad del repositorio** (decide Diego): la revisión 03 recomienda hacerlo privado para reducir exposición
   futura (el historial público ya contiene el ID de hardware y el de la licencia de prueba; hacerlo privado no borra
   copias existentes). El ID de licencia de prueba caduca el 02-11-2026; el de hardware no se puede "revocar".

## Historial de esta decisión (aceptada en la versión 6)

| Versión | Cambio | Origen |
|---|---|---|
| 1 | Reparto 7 años / 24 meses, sellado por exportación e instalación aparte, EURUSD, presupuesto y abandono | Claude, tras metadatos de Darwinex (n.º 87–88) |
| 2 | Sellado con dos instalaciones (la opción B sola no bastaba) | Claude, autocorrección |
| 3 | "Cientos de operaciones" corregido con datos propios; muestra mínima de 100; topes de búsqueda; precios de SQX; no comprar por la caducidad; exigencias de realismo; condiciones previas (puerto 5050, repositorio) | Revisión 03 |
| 4 | Presupuesto escalonado (piloto con cifras ya fijadas → confirmatoria con límite fijado con datos del piloto; los topes de la v3 pasan a techos); variantes, filtros y selecciones cuentan como pruebas; fechas como hitos de revisión; causas de abandono distinguidas; el bloque sellado nunca selecciona, modifica ni rescata; reparto y EURUSD provisionales | Revisión 06 |
| 5 | Muestra mínima necesaria pero no suficiente (dependencia); método de medición del piloto (tres lotes, coste por estrategia válida, tiempo humano); preferible una candidata principal y, si hay varias, el examen como prueba múltiple; congelación con hashes; parada automática por cualquier límite | Revisión 09 |
| 6 | **Aceptada.** Inicio del sellado por regla (fecha más tardía vista en el curso, nunca antes de 2024-10-01; si quedan menos de 18 meses, se completa con prospectivo); conocimiento previo de Claude y Diego declarado; EURUSD decidido con salida a GBPUSD si falla C12; capital real 0 € hasta superar la demo; horas registradas sin compromiso semanal; prioridad "rigor con presupuesto de tiempo por fase"; referencias preregistradas y control negativo en el piloto; tres objetivos (A7) en el abandono | Diego (A1, A2, A3, A19, A20 delegadas en el chat del 2026-10-21); Claude: la regla del sellado, al ver que el curso usa datos hasta 2025-03 y se empaquetó el 2026-01-12; revisiones 10 y 11 |
