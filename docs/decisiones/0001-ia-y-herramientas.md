# Decisión 0001 – Cómo usamos la IA y en qué orden entran las herramientas

Fecha: 2026-10-19 · Estado: **ACEPTADA** (Diego, "guarda esto") · Sustituye a: —

## Contexto

Diego trajo una propuesta externa: un laboratorio cuantitativo automatizable con varias IAs trabajando como un equipo de investigación,
organizado en ocho capas (construcción, investigación, cálculo, generación, datos, ejecución, orquestación y supervisión).
Claude la revisó: los principios son correctos, pero tenía tres riesgos y demasiadas piezas para empezar.

## Decisión

### Lo que se mantiene de la propuesta
- La IA propone; Python con reglas deterministas calcula; un evaluador con criterios fijados de antemano decide; Diego aprueba el paso a dinero real.
- Ninguna IA puede convertir una estrategia fallida en aprobada, cambiar las reglas de evaluación después de ver resultados ni activar operaciones reales.
- Cada herramienta o modelo entra solo si demuestra que mejora las decisiones (principio 6). El número de IAs lo deciden los resultados.
- El núcleo se diseña para poder añadir piezas sin reconstruirlo.

### Dos reglas nuevas
1. **Toda hipótesis cuenta.** Cada hipótesis propuesta (por Diego, por Claude, por otra IA o por SQX) se registra y entra en el
   número de pruebas que se usa para corregir los resultados. Más IAs proponiendo ideas significa más pruebas y más falsos positivos
   si no se cuentan. *Implementación: registro de hipótesis en H1.*
2. **Los cambios de proceso también son pruebas.** Cambiar el método (filtros, métricas, costes, periodos, umbrales) después de ver
   resultados es un grado de libertad más y se registra como tal. Nunca se cambia nada del proceso mirando los datos sellados.

### Cómo se mide si una IA aporta valor
Primero con tareas baratas y puntuables, no con "¿encuentra estrategias buenas?" (eso necesita muchísimas muestras para medirse):
- **Errores sembrados:** se introducen a propósito errores conocidos en una copia del código (usar información del futuro, costes mal
  aplicados, desfase de una vela, semilla no fijada...) y se mide qué revisor encuentra cuántos, con cuántas falsas alarmas y a qué coste.
- Tiempo para completar un experimento con y sin la herramienta.
- Si aporta algo que no aportan las que ya tenemos.

### Orden de entrada de las herramientas

| Fase | Pieza | Condición para entrar |
|---|---|---|
| Ya | Claude Code + núcleo Python + git/GitHub como registro externo con fecha | — |
| H0 | SQX por línea de comandos (`sqcli.exe`) | Lo que se verifique en la ficha H0 |
| H1 | Reconstrucción en Python del backtest de las estrategias exportadas, para comparar operación a operación con SQX | Necesaria para el criterio de salida de H1 |
| H1–H2 | numpy, pandas, scipy y `arch` (pruebas para muchas estrategias a la vez y remuestreo por bloques), con versiones fijadas | Software libre; cada dependencia se fija y se registra |
| H2 | Segundo modelo (Codex u otro) como **revisor adversario** del código de validación y de cada hipótesis antes de registrarla | Supera la prueba de errores sembrados. Si es de pago, lo aprueba Diego |
| H3 | IA analista que propone hipótesis | Se compara contra el mismo proceso sin IA, con criterios fijados antes |
| H4+ | Coordinador de tareas, alertas, supervisión externa | Cuando haya procesos que encadenar de verdad |

### Lo que nunca se automatiza
- La aprobación de una estrategia (la da el evaluador con criterios preregistrados y la revisa Diego).
- Cualquier paso a demo o a dinero real.
- La apertura de los datos sellados.

## Dónde esperamos marcar la diferencia (hipótesis, no promesa)

Nuestra ventaja realista no es tener más IA, sino engañarnos menos que la media de usuarios de SQX:
1. Reproducir por nuestra cuenta lo que dice SQX.
2. Estadística que tiene en cuenta cuántas cosas se han probado, y comparación con estrategias aleatorias equivalentes.
3. Costes realistas por franja horaria, con prueba de estrés.
4. Viabilidad simulada con las reglas exactas de cada vehículo (fondeadas, Darwinex Zero).
5. IA donde ya ha demostrado valor: construir y probar código, revisar de forma adversaria y resumir registros.

## Consecuencias
- No se añaden IAs ni capas por adelantado; cada una pasa por esta tabla.
- El registro de hipótesis pasa a ser parte del alcance de H1.
