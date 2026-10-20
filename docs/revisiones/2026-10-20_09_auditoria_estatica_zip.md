# Revisión externa 09 – Auditoría maestra estática (sobre un ZIP del proyecto)

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego, usando el prompt de `docs/auditoria/` sobre un **ZIP antiguo**
del repositorio (88 registros, sin `.git` ni evidencias privadas). **No es** la auditoría en sesión independiente
propuesta en B13 (sigue pendiente). Tipo: auditoría de diseño y de evidencias (no propone estrategias).

## Resumen de lo que concluye (redactado por Claude)

- **Veredicto:** continuar solo hasta cerrar la viabilidad técnica y construir una validación independiente fiable. Sin
  evidencia para invertir dinero esperando una estrategia rentable. Secuencia: seguridad → integridad de datos →
  presupuesto de búsqueda → reconstrucción independiente → evaluación estadística → examen sellado → demo.
- **Cifras del registro (88 entradas):** 81 OK, 6 FALLIDO, 1 INCONCLUSO; 88 sin semilla; 78 sin costes; 58 sin datos;
  0 con campo de familia; 7 con código "sucio".
- **Hallazgos críticos:** H1 guardián no demostrado como barrera (PowerShell; y la variable `LAB_PROTOCOLO_SELLADO`
  autoriza de forma demasiado amplia: debería ligar cada permiso a un recurso, finalidad y salida); H2 sellado no validado
  de extremo a extremo (límites, zona horaria, y que la investigación no pueda leer el archivo sellado); H3 búsqueda sin
  límite completo; **H4 el registro no permite reconstruir el universo de selección** (sin campo de familia ni tipos de
  evento). Altos: H5 no hay reconstrucción independiente; H6 costes que no son los del vehículo; H7 licencia y calendario
  no coordinados. Medio: H8 el ZIP no permite verificar el estado remoto.
- **Esquema de registro propuesto:** tipos de evento con campos obligatorios por tipo: GENERACION, BACKTEST, VALIDACION,
  CAMBIO_PROCESO, OPERACION_TECNICA, REVISION. Aceptación: reconstruir automáticamente cuántas estrategias, variantes,
  filtros, parámetros, mercados y procesos se probaron, incluidos los que no dieron resultados.
- **Examen sellado:** un candidato principal (o una cartera definida por reglas previas) congelado con hashes; una sola
  ejecución; si se examinan varios, **es una prueba múltiple** y hay que ajustarla; si falla, no se retoca. 24 meses no se
  dan por suficientes sin conocer frecuencia, dependencia e incertidumbre: **100 operaciones no son 100 observaciones
  independientes**.
- **Presupuesto de SQX sin inventar cifras:** medir tres tamaños de lote, separar generación/validación/optimización/
  exportación, coste **por estrategia válida para el análisis**, y límites de cómputo, evaluaciones y **tiempo humano**,
  con parada automática.
- **Otros:** registrar UTC y normalizar aparte la hora de mercado; no inventar semillas retrospectivas, declarar que la
  generación no es reproducible; código limpio en toda ejecución confirmatoria; añadir Sullivan, Timmermann y White (1999)
  a la literatura; piloto de 2–3 vídeos; lista de lo que no construir; seis niveles de decisión (técnica, estadística,
  ventaja neta, vehículo, demo, economía global); el tiempo de Diego no es gratis.
- **Plan priorizado (6 pasos)** y **5 decisiones para Diego**: primer mercado; horas semanales; gasto aceptable antes de
  tener evidencia; prioridad principal; licencia cuando expire la prueba.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| Cifras del registro | **Verificadas una a una: exactas** sobre las 88 primeras entradas (hoy son 89). Los 7 "sucios" están explicados (n.º 10 y 12: redacción; 44–48: descuido de Claude, en el diario) | — |
| "Ejecuciones sin límite" (H3, 5.4) | Se basa en una versión antigua: la 0003 v4 ya tiene piloto con cifras y techos. Su método para medir el coste (tres lotes, coste por estrategia válida, tiempo humano, parada automática) **mejora** el piloto | 0003 v5 |
| **H4: registro sin tipos de evento ni familia** | **De acuerdo: es el hallazgo más importante.** Sin esto no se puede contar el universo de pruebas que exigen DSR, PBO y MinBTL | B14: esquema de eventos tipados en el núcleo, con tests, antes de H1 |
| H1: `LAB_PROTOCOLO_SELLADO` demasiado amplia | **De acuerdo; no lo había visto.** Hoy cualquier protocolo "aprobado" abre todo `data/sealed/` | B15: permiso ligado a recurso, finalidad y salida; en la sesión de mantenimiento (A9) |
| H2: sellado sin validar; que la investigación no pueda leer el archivo sellado | De acuerdo | B1 (integridad) y condición previa de la 0003 |
| Examen sellado como prueba múltiple si hay varias candidatas | **De acuerdo; faltaba en la 0003** | 0003 v5: con más de una candidata se corrige por pruebas múltiples; preferible una principal |
| 100 operaciones ≠ 100 observaciones independientes | **De acuerdo**: la muestra mínima de 100 es necesaria, no suficiente | 0003 v5 |
| UTC, semillas, código limpio en confirmatoria | De acuerdo | C17–C19 |
| H7: licencia frente a calendario | De acuerdo | B16: qué tareas de H1 se pueden hacer con la licencia actual y cuáles no |
| Sullivan, Timmermann y White (1999) | De acuerdo | Añadido a `LECTURAS.md` |
| 5 decisiones de Diego | Correctas; coinciden con A2, A3 y A12 del índice y añaden dos | A19 (mercado) y A20 (prioridad principal) |
