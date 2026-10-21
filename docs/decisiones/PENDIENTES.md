# Asuntos abiertos – índice único

Actualizado: 2026-10-20 · Lo mantiene Claude. Cuando un asunto se cierra, se tacha aquí y se enlaza la decisión o el
registro que lo cierra. **Nada abierto vive solo en el chat.** Estado general y siguiente paso:
`docs/ESTADO_Y_CONTINUACION.md`.

## A. Decisiones de Diego (Claude no puede tomarlas, aunque se le delegue)

| # | Asunto | Propuesta de Claude | Origen |
|---|---|---|---|
| A1 | Aprobar, cambiar o rechazar la **decisión 0003** (reparto 24 meses sellados, cómo sellar, primer mercado provisional, presupuesto de búsqueda escalonado con piloto, muestra mínima, fechas como hitos, causas de abandono) | PROPUESTA v5 en `0003-reparto-mercado-presupuesto.md` (con historial de cambios) | Revisiones 01, 03, 06 |
| A1b | **Cifras del piloto** de búsqueda (1 familia, ≤ 2.000 estrategias, ≤ 8 h de cómputo) | Las propone Claude; Diego puede cambiarlas antes de empezar | Revisión 06 |
| A2 | **Dinero adicional que está dispuesto a perder** en el proyecto | — (solo Diego lo sabe) | Revisión 03 |
| A3 | **Horas semanales** que puede dedicar sin perjudicar otras prioridades | — | Revisión 03 |
| A4 | Repositorio de GitHub **público o privado** | Privado reduce exposición futura (no borra copias) | Revisión 03 |
| A5 | **Enunciado del objetivo** del proyecto (CLAUDE.md) | El de la revisión 05: "laboratorio cuantitativo integrado, reproducible, auditable y progresivamente automatizado, para encontrar —o descartar con evidencia— ventajas explotables por un particular" | Revisión 05 |
| A6 | **Regla de proporcionalidad** como decisión: ningún control nuevo sin amenaza concreta, prueba que demuestre el fallo y criterio de aceptación | Adoptarla | Primera revisión externa (diario) |
| A7 | **Éxito medido por rentabilidad neta conservadora frente al coste total** del proyecto (no por estrategias que pasan filtros) | Añadirlo a los criterios de abandono de 0003 | Revisión 04 |
| A8 | **Procedencia y autorización** del material del curso (aparece "CURSOSDIGITALEX.COM") | Aclararla antes de usarlo más | Revisiones 01, 03 |
| A9 | **Sesión de mantenimiento del guardián** (cerrar el agujero de PowerShell). Solo puede abrirla Diego | Borrador probado (44/44) e instrucciones en `docs/mantenimiento/` | Ficha H0, Paso 0 |
| A10 | Variable de usuario **`ANTHROPIC_API_KEY`**: ¿la reconoce, la revoca, la borra? | Revocarla si no la reconoce | Sesión 2026-10-20 |
| A11 | **Instalar MetaTrader** para compilar el código exportado (tareas 3e/3f) | Necesario antes de la demo | Ficha H0 |
| A12 | **Edición y compra de la licencia de SQX**. La caducidad (02-11-2026) no es motivo para comprar | Decidir con la ficha H0 cerrada | Revisión 03, ficha H0 |
| A13 | **Identidad de los commits** (hoy `Claude <noreply@anthropic.com>`) | Mantenerla o poner la suya | Sesión 2026-10-20 |
| A14 | **Copias de seguridad** de `h0/evidencias_privadas/` y `Documents/LAB_PRIVADO_CURSO/` (solo existen en este PC) | Copiarlas a un sitio suyo de vez en cuando | Diario |
| A15 | **Proteger la rama en GitHub** contra `push --force` (refuerza el registro como referencia externa) | Activarlo | Primera revisión externa |
| ~~A16~~ | ~~Permiso para descargar los 3 papers~~ **Cerrado:** permiso dado y papers descargados (registro n.º 89) | — | Revisión 07 |
| A17 | **Piloto de vídeos del curso:** instalar FFmpeg y un transcriptor (Whisper o similar, gratuitos) y descargar su modelo (1–3 GB); depende de A8 | Darlo cuando A8 esté aclarado | Revisión 07 |
| A19 | **Primer mercado de investigación:** EURUSD (simplicidad, costes por verificar), oro (seguir el curso) o no decidir hasta contrastar costes y calidad de datos | EURUSD como candidato provisional (0003) | Revisión 09 |
| A20 | **Prioridad principal:** máximo rigor aunque tarde más; rigor con límite temporal estricto; o aprender SQX y cuantitativa mientras se valida. Diego añadió en el chat: "además de utilizar Claude Code y Opus para optimizar el proceso en todos los sentidos" | Pendiente de que Diego elija una (pegó las tres opciones sin marcar) | Revisión 09 |
| A18 | **Instalar numpy, pandas y scipy** con versiones fijadas (gratuitos; necesarios para H2, decisión 0001) | Darlo antes de H2 | Revisión 07 (hallazgo) |

## B. Trabajo técnico pendiente (Claude)

| # | Asunto | Estado / siguiente paso | Origen |
|---|---|---|---|
| B1 | **Prueba de integridad exportar/importar por fechas** con USDCHF (datos quemados), con los criterios de la revisión 01 (intervalo exacto, importación sin errores, velas idénticas tras normalizar, sin ausentes/duplicadas/desplazadas, repetible, zona horaria) | Siguiente paso técnico | Decisión 0003, revisión 01 |
| B2 | **API del puerto 5050**: ¿pide autenticación? ¿se alcanza desde otro equipo? Reglas por puerto (requiere administrador) | Necesita un segundo dispositivo de la red y permisos de Diego | Ficha H0, revisión 03 |
| B3 | Comprobar el guardián con una llamada **real** de PowerShell tras A9 | Tras A9 | Paso 0 |
| B4 | Darwinex sin precios: fecha final, granularidad, zona horaria; **procedencia de los datos del curso desde 2015** frente a EURUSD de Darwinex desde 2017-10 | Abierto | Tarea 5, revisión 01 |
| B5 | Comisión y swap reales de **Darwinex Zero** (condiciones oficiales) | Abierto | Tarea 5 |
| B6 | Optimización secuencial | INCONCLUSO por proporcionalidad | Tarea 2 |
| B7 | Hipótesis por verificar: **P/L con tipo de cambio fijo** en pares no USD; **efecto no uniforme del spread**; **consola de SQX 2 h adelantada**; aviso de **cambio de convención horaria** en los datos | Verificar en H1 (reconstrucción en Python) | Tareas 3d, 4, 2 |
| B8 | `pip install -e .` en este PC | Menor | Paso 0 |
| B9 | Falsos positivos del guardián ("del", `>`, `2>&1`, "zip", `.find(`) | Afinar en mantenimiento, con permiso de Diego | Diario |
| B10 | El ejecutor no detecta errores de SQX que salen con código 0 | Añadir detección de mensajes conocidos | Diario |
| B11 | **Piloto de 3 vídeos** (Builder, Retester, Optimizer): transcripción con marcas de tiempo + fotogramas leídos por Claude + contraste con los `.cfx`; medir calidad, tiempo y coste | Tras A8 y A17; todo en `LAB_PRIVADO_CURSO` | Revisión 07 |
| ~~B12~~ | ~~Fichas de los 3 papers~~ **Cerrado:** tres fichas con verificaciones propias en `conocimiento/fundamentos/` | — | Revisión 07 |
| B14 | **Esquema de eventos tipados en el registro** (GENERACION, BACKTEST, VALIDACION, CAMBIO_PROCESO, OPERACION_TECNICA, REVISION), con **campo de familia** y campos obligatorios por tipo. Aceptación: reconstruir automáticamente el universo de pruebas de una tanda. Sin tocar las entradas ya escritas (solo se añade) | Antes de H1; con tests | Revisión 09 (H4) |
| B15 | **Permiso de acceso al sellado demasiado amplio:** hoy cualquier protocolo "aprobado" en `LAB_PROTOCOLO_SELLADO` abre todo `data/sealed/`. Ligarlo a recurso, finalidad y salida | En la sesión de mantenimiento (A9) | Revisión 09 (H1) |
| B16 | **Licencia frente a calendario:** documentar qué tareas de H1 se pueden hacer con la licencia de prueba (caduca 02-11-2026) y cuáles exigen licencia, con el coste de cada alternativa | Antes de comprometer H1 | Revisión 09 (H7) |
| B13 | **Auditoría maestra** con `docs/auditoria/prompt_auditoria_maestra.md`, en una **sesión independiente** de solo lectura (sin el contexto de quien construyó el laboratorio) | Propuesta como tarjeta de sesión `task_fe8910bc` el 2026-10-20 (caduca hacia el 2026-10-27; si caduca, se vuelve a proponer); el resultado se separa en bloqueantes, alto valor y futuro | Revisión 08 |

## C. Requisitos fijados para fases futuras (no se olvidan al llegar)

| # | Requisito | Fase | Origen |
|---|---|---|---|
| C1 | Cada estrategia descartada registra **su motivo** (costes, sensibilidad a parámetros, concentración temporal, pocas operaciones, régimen…); los fallos agrupados alimentan las **siguientes** hipótesis, con presupuesto nuevo y sin tocar el bloque sellado | H2 | Revisión 05 |
| C2 | **MC, WF y optimización no son pruebas independientes** si comparten datos y selección: su acuerdo no suma evidencia | H2 | Revisión 04 |
| C3 | Costes del vehículo real, **deslizamiento adverso**, retest **intradía** y código **compilado** antes de atribuir ventaja | H1–H2 | Revisión 03 (0003 §4) |
| C4 | Estrategia seleccionada con datos hasta una fecha: solo se evalúa con datos **posteriores** | Siempre | Auditoría del curso |
| C5 | **Una sola arquitectura** escrita (hoy hay tres: hoja de ruta, revisión 02, revisión 05), consolidada al cerrar H0, sin reescribir lo que funciona | Cierre de H0 | Revisiones 02, 05 |
| C6 | **Fichas de investigación** del curso, una por concepto que vaya a entrar en una decisión (empezar por OOS usado para seleccionar, filtros de robustez y costes) | H1–H2 | Revisión 02 |
| C7 | Comparar **IA frente a sin IA** con métrica y tamaño fijados antes (poca potencia con pocas estrategias) | H3 | Revisión 02, decisión 0001 |
| C8 | **VPS** solo para ejecución continua de una estrategia ya validada | H4–H5 | Revisión 05 |
| C9 | Las fechas de 0003 son **puntos de control de gasto**, no plazos para declarar evidencia: sin muestra suficiente, INCONCLUSO | Siempre | Revisión 04 |
| C10 | La **base de conocimiento** (`conocimiento/`) no entra en el motor crítico hasta estar validada y decidida; el bloque sellado queda fuera del ciclo de aprendizaje | Siempre | Revisión 07 |
| C11 | **Banco de pruebas adversarias** del validador: casos con errores sembrados (fuga de información futura, costes omitidos, desfase de vela, selección por azar, sesgo de supervivencia) que el validador **tiene que detectar**; si no los detecta, no se fía de él | H1–H2 | Revisión 08, decisión 0001 |
| C12 | **Ficha de datos y costes por instrumento**: procedencia, cobertura, huecos, zona horaria, sesiones, spread, comisión, swap y deslizamiento, contrastada con el vehículo (Darwinex Zero) | Antes de investigar un mercado | Revisión 08, tarea 5 |
| C13 | **Conservar la serie diaria de resultados de TODAS las estrategias probadas**, también las descartadas por los filtros: sin ella no se pueden calcular DSR, PBO ni el N efectivo. Comprobar en el piloto si SQX permite conservarlas (hoy solo guarda las que pasan) | Piloto de la 0003 | Fichas DSR, PBO y MinBTL |
| C14 | **No usar la PBO ni el DSR como objetivo de la búsqueda**: miden el proceso, no lo guían | H2 | Ficha PBO |
| C16 | **Examen sellado:** preferible una candidata principal; con varias, se corrige como prueba múltiple; todo congelado con hashes antes de abrir | Examen | Revisión 09 |
| C17 | Registrar las horas en **UTC** y normalizar aparte la hora de mercado (la consola de SQX va 2 h adelantada) | H1 | Revisión 09 |
| C18 | **Semillas:** si SQX no permite fijarla, declarar en el registro que la generación no es reproducible; nunca inventar una semilla a posteriori | Siempre | Revisión 09 |
| C19 | Toda ejecución **confirmatoria** con código limpio (sin cambios sin confirmar) | Fase confirmatoria | Revisión 09 |
| C15 | Comparar el **N efectivo** de cada búsqueda con el límite de ~139 configuraciones independientes que admite el bloque de investigación de 7 años (para no pasar de Sharpe 1 por azar) | Piloto y confirmatoria | Ficha MinBTL |

## D. Lo que NO se construye todavía (y cuándo reconsiderarlo)

| Idea | Cuándo reconsiderarla | Origen |
|---|---|---|
| Más agentes de IA en paralelo | Cuando un experimento controlado demuestre mejora frente al proceso actual | Revisiones 05, 08 |
| Entrenar un modelo propio | Con datos etiquetados suficientes y una tarea concreta que lo justifique | Revisión 08 |
| VPS permanente | Cuando la ejecución prospectiva exija disponibilidad continua | Revisiones 05, 08 |
| Base de datos compleja o infraestructura distribuida | Cuando el registro actual sea un cuello de botella **medido** | Revisión 08 |
| Optimización automática continua | Tras validar la búsqueda controlada y sus límites contra el sobreajuste | Revisión 08 |
| Muchos mercados a la vez | Cuando el primero tenga validación fiable y presupuesto definido | Revisión 08 |
| Cientos de papers de golpe | Tras validar el método de extracción con las primeras fichas | Revisiones 07, 08 |
| Otra arquitectura teórica | Solo la consolidación única de C5, al cerrar H0 | Revisiones 06, 08 |
