# Revisión externa 02 – Cómo organizar el proyecto con el máximo rigor

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego en el chat · Tipo: propuesta de organización (no propone estrategias)

## Resumen de lo que propone (redactado por Claude)

Idea central: no dar por bueno un método porque lo enseñe un curso, lo recomiende una IA o produzca un backtest
espectacular; se estudia, se formaliza, se contrasta y se decide.

1. **Arquitectura en 5 capas**, construidas solo cuando hagan falta: conocimiento y aprendizaje; investigación asistida
   por IA; motor experimental (SQX + Python); validación independiente; bots y operativa.
2. **Fichas de investigación** para cada concepto relevante del curso: afirmación, fundamento, implementación en SQX,
   riesgos de falso positivo, prueba, resultado con incertidumbre y decisión.
3. **IA medida, no supuesta:** Claude Code construye; otro modelo audita; los modelos proponen hipótesis registradas
   antes de evaluar; Python verifica los números. Comparar el proceso con IA frente a uno sin IA con presupuesto
   comparable. La coincidencia entre modelos no es evidencia.
4. **Bloque sellado central** (investigación / validación / final intocable) y control técnico del sistema operativo,
   no solo un hook. Misma disciplina para código, dependencias, semillas, configuraciones y costes.
5. **Cada decisión importante con dos resultados:** técnico y de aprendizaje para Diego. Una sola fuente de verdad.
6. **Orden:** cerrar H0 técnico; abrir una línea de validación del curso; medir la aportación de las herramientas.
   No incorporar al motor las configuraciones del curso ni usar sus resultados para elegir la estrategia definitiva.

## Respuesta de Claude

De acuerdo con el fondo; casi todo ya está en la hoja de ruta, la decisión 0001 y la ficha H0. Matices:

| Punto | Postura |
|---|---|
| 1. Capas | De acuerdo como mapa, no como plan de construcción: la propia revisión lo dice. Coincide con la arquitectura de la hoja de ruta |
| 2. Fichas del curso | **Buena idea, con proporcionalidad:** una ficha por concepto que vaya a entrar en una decisión, no por vídeo. Empezar por las que afectan a la validez: OOS usado para seleccionar, filtros de robustez, costes |
| 3. Medir la IA | De acuerdo; ya es H3 en la hoja de ruta y la decisión 0001 (errores sembrados). Advertencia: con pocas estrategias evaluadas la comparación IA/no-IA tendrá muy poca potencia estadística: hay que fijar la métrica y el tamaño antes |
| 4. Bloque sellado y control del sistema operativo | De acuerdo. Hoy el bloque sellado aún no existe; el protocolo y la decisión 0003 lo diseñan con cifrado y una instalación aparte. El agujero de PowerShell del guardián sigue abierto y es condición previa |
| 5. Doble resultado y una fuente de verdad | De acuerdo. **Riesgo real detectado:** `docs/hoja_de_ruta.md` aún dice "Ultimate, build 143.2708, prueba de 14 días", contradicho por la ficha H0. Fuente de verdad propuesta: decisiones en `docs/decisiones/`, estado en `h0/ficha.md`, hechos en `registry/`; la hoja de ruta es el PDF de Diego y se anota su desfase en vez de editarlo |
| 6. Orden | De acuerdo: cerrar H0 primero (falta la prueba de integridad export/import, Darwinex tras el protocolo y el guardián) |
