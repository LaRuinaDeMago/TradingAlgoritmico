# Revisión externa 05 – Un laboratorio cuantitativo integrado que aprende de sus errores

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego en el chat · Tipo: arquitectura y forma de aprender (no propone estrategias)

## Resumen de lo que propone (redactado por Claude)

- No conectar todas las herramientas con todas: que cada una aporte información **verificable** al mismo proceso, con
  resultados trazables, y que ninguna convierta sus conclusiones en verdades sin comprobación independiente.
- **Arquitectura en 6 capas:** (1) datos y trazabilidad; (2) motor de investigación (SQX); (3) validación independiente
  (Python, costes, sobreajuste, MC, WF, bloque sellado); (4) inteligencia y aprendizaje (Claude Code, análisis de fallos,
  hipótesis justificadas); (5) ejecución prospectiva (demo, VPS cuando proceda); (6) control económico y decisiones.
  Transversales: **registro central** con identificadores, versiones, configuraciones, resultados, costes y decisiones;
  y un **sistema de permisos y seguridad** (datos reservados, credenciales, APIs, bloque sellado).
- **Ciclo de aprendizaje:** registrar qué estrategias fallan y **por qué**; agrupar los fallos (costes, sensibilidad a
  parámetros, concentración temporal, pocas operaciones, dependencia de un régimen…); distinguir patrones respaldados de
  hipótesis; proponer familias nuevas que respondan a esos hallazgos con **un presupuesto nuevo y sin reutilizar el bloque
  sellado**; comparar con investigaciones anteriores. Regla: el aprendizaje cambia las **siguientes** hipótesis, nunca las
  pruebas ya hechas ni convierte un negativo en positivo. Nada de IA reentrenándose sola: informes estructurados y
  propuestas que aprueba Diego; automatizar solo lo que demuestre valor.
- Papel de cada herramienta: SQX genera/retesta/optimiza; Python coordina y comprueba; Claude Code desarrolla, audita y
  propone; el curso aporta hipótesis; hojas de cálculo e informes para revisar sin cajas negras; demo y VPS para medir
  la ejecución.
- **VPS:** sí, pero para ejecución continua de una estrategia ya validada, no para investigar.
- Prioridades: cerrar la base técnica; **definir la arquitectura completa antes de ampliar** (qué componente genera cada
  dato, quién lo consume, cómo se versiona, qué pruebas necesita) sin reescribir lo que funciona; integrar el curso como
  fuente controlada de hipótesis; medir la mejora de cada pieza nueva. La 0003 sigue pendiente.
- **Objetivo propuesto para el proyecto:** "construir un laboratorio cuantitativo integrado, reproducible, auditable y
  progresivamente automatizado, cuyo propósito sea encontrar —o descartar con evidencia— ventajas de mercado explotables
  por un particular". Con una salida digna: detenerse sin ventaja suficiente es una decisión racional.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| Cada herramienta aporta información verificable | De acuerdo; es el principio 6 de la hoja de ruta | — |
| Arquitectura en 6 capas | De acuerdo en el fondo. **Riesgo: ya hay tres arquitecturas escritas** (hoja de ruta, revisión 02 con 5 capas, esta con 6). Hay que consolidar **una**, cuando toque | Pendiente en `PENDIENTES.md`: una sola arquitectura al cerrar H0, no antes |
| Registro central transversal | De acuerdo; existe (`registry/experimentos.jsonl`) | Le faltará el **motivo de descarte** de cada estrategia (ver siguiente fila) |
| **Ciclo de aprendizaje con taxonomía de fallos** | **Lo más valioso de esta revisión**: concreto y barato | Requisito para H2: cada estrategia descartada registra su motivo (costes, sensibilidad a parámetros, concentración temporal, pocas operaciones, régimen…) |
| El aprendizaje cambia las siguientes hipótesis, no las pruebas hechas | De acuerdo; es la regla 8 de CLAUDE.md | — |
| Sin IA reentrenándose sola | De acuerdo; coherente con la decisión 0001 | — |
| VPS solo para ejecución validada | De acuerdo | — |
| Definir la arquitectura antes de ampliar | De acuerdo, con proporcionalidad: documentar flujos de datos cuando se construya H1 | — |
| Nuevo enunciado del objetivo | Mejor que el actual de CLAUDE.md: añade "integrado, auditable, progresivamente automatizado" y la salida digna. **Cambiar el objetivo lo decide Diego** | Pendiente en `PENDIENTES.md` |

Nota: las revisiones 02 a 05 coinciden mucho entre sí. Si vienen del mismo modelo, esa coincidencia **no** es evidencia
independiente (lo dice la propia revisión 02).
