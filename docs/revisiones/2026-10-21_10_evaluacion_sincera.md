# Revisión externa 10 – Evaluación sincera del proyecto y de las próximas fases

Fecha: 2026-10-21 · Origen: otra IA, aportada por Diego. Declara basarse en la **inspección estática del ZIP** (no
ejecutó nada ni miró GitHub); cita las nueve revisiones del 20-10 y la 0003 v5, así que leyó un ZIP posterior al de la
09. Estilo y estructura muy parecidos a la 09: probablemente **el mismo modelo**, y su coincidencia con ella no es
evidencia independiente. Tipo: evaluación de enfoque y riesgos (no propone estrategias).

## Resumen de lo que concluye (redactado por Claude)

- **Veredicto:** continuar como experimento controlado; no dar el sistema por validado; no invertir dinero esperando
  rentabilidad; sí invertir tiempo limitado en cerrar H0.
- **Lo conseguido:** el n.º 86 (10 estrategias con operaciones idénticas, 54,7 s, configuraciones restauradas) demuestra
  un experimento pequeño reproducible de extremo a extremo; no que el motor sea correcto en todos los casos, ni que dos
  ejecuciones iguales no compartan el mismo error, ni rentabilidad.
- **Siguiente prueba importante:** no repetir con 100 estrategias, sino **atacar el validador con errores sembrados**
  (fuga de futuro, comisión omitida, vela desplazada) y **reconstruir las operaciones en Python** con discrepancias explicadas.
- **Cinco riesgos:** (1) que el laboratorio se convierta en el proyecto (nueve revisiones en un día, varias arquitecturas);
  (2) validación que aún no es independiente; (3) ilusión de seguridad del sellado (y exposición histórica del repositorio);
  (4) buscar demasiado: las fórmulas no compensan un universo de búsqueda mal registrado; (5) confundir validez
  estadística con negocio viable: añadir una **tercera comprobación económica** (capital, tiempo y trabajo necesarios
  frente al rendimiento neto esperado).
- **Orden:** seguridad → integridad de datos → validador independiente atacado + registro tipado → piloto → decidir escala.
  No comprar SQX porque caduque la prueba; 7 + 2 años son una propuesta inicial, no una garantía de examen concluyente.
- **Principio rector:** maximizar la evidencia útil por euro, hora y unidad de complejidad; cada mejora responde a tres
  preguntas: qué error o coste reduce, cómo se demuestra y qué se deja de hacer por ella.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| Lectura del n.º 86 | **Correcta y bien acotada.** Coincide con lo que dice la ficha H0: proceso, no ventaja | — |
| Validador atacado con errores sembrados | De acuerdo; **ya estaba** (C11) | Sin cambios |
| Reconstrucción en Python operación a operación | De acuerdo; **ya estaba** (objetivo de H1, B7) | Sin cambios |
| Riesgo 1: el laboratorio como proyecto | **De acuerdo, y es el aviso más útil de la revisión.** Se aplica también a las revisiones: once en dos días, cada una consume tiempo de Diego y de Claude, y la mayor parte de lo que aportan ya estaba | **A21:** que Diego decida una pausa de revisiones externas hasta terminar el piloto (salvo la auditoría independiente B13) |
| Riesgo 3: sellado y exposición del repositorio | De acuerdo; ya estaba (B1, B15, A4) | Sin cambios |
| Riesgo 4: universo de búsqueda | De acuerdo; ya estaba (B14) | Sin cambios |
| Riesgo 5: tercera comprobación económica | **De acuerdo; amplía A7** (hoy solo "rentabilidad neta frente al coste total") con capital necesario, horas y trabajo de explotación | A7 ampliada |
| Orden de los pasos | **Coincide** con `ESTADO_Y_CONTINUACION.md` §7 y la 0003 v5 | Sin cambios |
| 7 + 2 años no garantizan un examen concluyente | De acuerdo; ya estaba (0003 v5: 100 operaciones ≠ 100 observaciones independientes; C9, C15) | Sin cambios |
| Principio rector (evidencia por euro, hora y complejidad) | De acuerdo; es la regla de proporcionalidad (A6) extendida a todo, no solo a la seguridad | Se anota en A6 como formulación alternativa |
| "API local en todas las interfaces sin autenticación comprobada" | Correcto; ya estaba (B2). Matiz: el cortafuegos de Windows bloquea la entrada y no hay regla para SQX (comprobado el 20-10) | Sin cambios |

**Balance:** revisión de buena calidad y **casi nada nuevo**: de diez puntos, uno amplía un asunto (A7) y otro sugiere una
decisión nueva (A21). Que coincida con la 09 no suma evidencia, porque probablemente viene del mismo modelo.
