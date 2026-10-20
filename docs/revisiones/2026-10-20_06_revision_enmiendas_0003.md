# Revisión externa 06 – Enmiendas concretas a la decisión 0003

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego en el chat · Tipo: enmiendas a una decisión (no propone estrategias)

## Resumen de lo que propone (redactado por Claude)

- No aprobar la 0003 tal como está, pero no reescribirla entera ni frenar el proyecto: modificar pocos puntos, aprobar
  el plan por etapas y seguir con H0. **No hace falta otra arquitectura teórica**: alinear decisiones, controles y
  trabajo técnico.
- Mantener: reparto 2017–2024 / sellado desde 2024-10 (provisional, sujeto a verificar datos y muestra); EURUSD como
  candidato provisional (por costes, calidad de datos y viabilidad, no por rentabilidad ni por el curso); 0 € hasta
  cerrar H0; fechas de H1 y H2 como hitos de revisión, no como obligación de avanzar; 20 familias como límite inicial
  **contando también variantes, filtros y decisiones de selección**; seguridad antes de descargar datos.
- **Cambio crítico: las ejecuciones de SQX no pueden ser ilimitadas.** Presupuesto **escalonado**: piloto pequeño;
  ampliación solo si el piloto aporta información útil; límite acumulado (búsquedas, cómputo, gasto) fijado antes de la
  búsqueda confirmatoria. **No poner ahora una cifra arbitraria** sin conocer el coste de cada lote y la capacidad del PC.
- Abandono distinguiendo **retrasos justificables, fallos técnicos corregibles y evidencia de que no hay ventaja**.
- El bloque sellado **no se usa para seleccionar, modificar ni rescatar** estrategias.
- Seguir: cerrar H0 (exportar/importar con USDCHF, PowerShell, API local); ficha con SÍ / NO / INCONCLUSO sin dar por
  hecha una prueba porque un comando devuelva algo; H1 y H2 por sus criterios de salida; el curso como fuente de
  hipótesis. VPS, más API y agentes solo con necesidad demostrada. Invertir tiempo, no dinero, por ahora.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| "Ejecuciones ilimitadas" | **Se basa en una versión anterior**: desde la revisión 03 la 0003 ya tenía topes. Pero su argumento añade algo nuevo | — |
| Presupuesto escalonado frente a cifras ya (choca con la revisión 03) | **Se concilian**: el **piloto** sí necesita cifras ya (pequeñas, solo para medir): 1 familia, ≤ 2.000 estrategias, ≤ 8 h de cómputo, y no produce candidatas. La **confirmatoria** fija su límite con los números del piloto, antes de empezar. Los topes de la revisión 03 quedan como **techos** | 0003, versión 4. Las cifras del piloto son un juicio de Claude; Diego puede cambiarlas antes de empezar |
| Variantes, filtros y decisiones de selección cuentan | De acuerdo (reglas 7 y 8) | 0003 v4 |
| Fechas como hitos de revisión | De acuerdo (ya en `PENDIENTES.md`, C9) | 0003 v4 |
| Tres causas de abandono distintas | **De acuerdo; mejora la decisión** | 0003 v4 |
| El sellado no selecciona, modifica ni rescata | De acuerdo; ya estaba implícito, ahora es explícito | 0003 v4 |
| Reparto y EURUSD provisionales | De acuerdo | 0003 v4 |
| No hace falta otra arquitectura | De acuerdo; coherente con consolidar una sola al cerrar H0 (C5) | — |
| Ficha con SÍ / NO / INCONCLUSO | Ya es así; la lección de que el "OK" de un comando no basta está aplicada en todo H0 | — |
| Tiempo sí, dinero no | De acuerdo | — |
