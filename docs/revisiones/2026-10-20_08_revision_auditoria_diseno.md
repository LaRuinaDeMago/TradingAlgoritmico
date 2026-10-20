# Revisión externa 08 – Auditoría de diseño y prompt de auditoría maestra

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego (dice haber revisado un ZIP del repositorio de forma estática) ·
Tipo: auditoría de diseño (no propone estrategias). El prompt se guarda literal en `docs/auditoria/prompt_auditoria_maestra.md`.

## Resumen de lo que propone (redactado por Claude)

- Pregunta rectora: qué cambios aumentan de verdad la capacidad de descubrir una ventaja y distinguirla del azar **por
  unidad de dinero, tiempo y complejidad**. Separar lo que aporta evidencia, lo que ahorra trabajo y lo que solo parece
  sofisticado.
- Del repositorio: base mejor que la media (registro encadenado, separación de datos, IA sin poder de aprobar,
  reconstrucción independiente prevista, EDGE frente a VIABILIDAD, aprendizaje). 88 registros y reproducción 10/10.
- **Cinco problemas prioritarios:** seguridad del bloque sellado (PowerShell, puerto 5050); integridad temporal de los
  datos (exportar/importar); presupuesto estadístico (dice que las ejecuciones no tienen límite); validación
  independiente de SQX que **detecte** errores de anticipación, costes, desfases; criterios de éxito y abandono
  cuantificables.
- **Mejoras por impacto en la evidencia:** A) **banco de pruebas adversarias** (errores sembrados: fuga de futuro, costes
  omitidos, desfase temporal, selección por azar, supervivencia), prioridad muy alta; B) contabilidad de todos los grados
  de libertad; C) **ficha de datos y costes por instrumento** contrastada con el vehículo; D) biblioteca científica y del
  curso; E) IA frente a sin IA en tareas controladas; F) registro de ejecución prospectiva en demo.
- **Qué no construir todavía:** más agentes en paralelo; modelo propio; VPS permanente; base de datos compleja o
  infraestructura distribuida; optimización automática continua; muchos mercados a la vez; cientos de papers de golpe.
- **Prompt de auditoría maestra** de solo lectura, para una sesión aparte; usar su resultado separando bloqueantes,
  mejoras de alto valor y mejoras futuras, y aplicar cambios pequeños y revisables.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| "Ejecuciones sin límite" | **Otra vez sobre una versión anterior de la 0003** (desde la v3 hay techos; la v4 tiene piloto + confirmatoria). El argumento de fondo ya está incorporado | Nota en el prompt guardado |
| Banco de pruebas adversarias | **De acuerdo: lo más valioso de la revisión.** La decisión 0001 ya preveía errores sembrados para evaluar a la IA; aquí se amplía a evaluar **el propio validador** | Requisito C11 para H1–H2 |
| Contabilidad de grados de libertad | Ya en 0003 v4 y reglas 7–8 | — |
| Ficha de datos y costes por instrumento | De acuerdo; concreta la tarea 5 y el asunto B5 | Requisito C12 |
| Lista de "no construir todavía" | **De acuerdo con toda ella** | Nueva sección D en `PENDIENTES.md` |
| Auditoría maestra en sesión aparte | **De acuerdo, y debe ser una sesión sin mi contexto**: yo construí casi todo y no soy un auditor independiente | B13: propuesta como sesión independiente de solo lectura |
| Aplicar el resultado por grupos y con cambios pequeños | De acuerdo | — |
