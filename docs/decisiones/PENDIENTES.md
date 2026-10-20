# Asuntos abiertos – índice único

Actualizado: 2026-10-20 · Lo mantiene Claude. Cuando un asunto se cierra, se tacha aquí y se enlaza la decisión o el
registro que lo cierra. **Nada abierto vive solo en el chat.**

## A. Decisiones de Diego (Claude no puede tomarlas, aunque se le delegue)

| # | Asunto | Propuesta de Claude | Origen |
|---|---|---|---|
| A1 | Aprobar, cambiar o rechazar la **decisión 0003** (reparto 24 meses sellados, cómo sellar, primer mercado, topes de búsqueda, muestra mínima, fechas) | PROPUESTA en `0003-reparto-mercado-presupuesto.md` | Revisiones 01, 03 |
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
