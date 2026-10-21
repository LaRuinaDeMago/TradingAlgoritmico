# Revisión externa 11 – ¿Cambiar el centro de gravedad del proyecto?

Fecha: 2026-10-21 · Origen: otra IA, aportada por Diego (probablemente la misma que la 10). Tipo: propuesta de enfoque y
de arquitectura; menciona familias de estrategias, pero como hipótesis por investigar, no como ventajas.

## Resumen de lo que propone (redactado por Claude)

- **Cambio de misión:** de "fábrica de estrategias" (SQX genera y el laboratorio valida) a "sistema de investigación,
  descubrimiento de ventajas y asignación de capital bajo incertidumbre", donde SQX es **un método más** que compite.
- **Competición entre métodos** con el mismo presupuesto de cómputo y de revisión humana, y criterios congelados antes:
  una **referencia simple** con reglas predefinidas, **SQX con búsqueda limitada** y una **vía por hipótesis** (con IA
  si aporta). Métricas: proporción que supera cada filtro, coste por candidata válida, rendimiento neto frente a las
  referencias con incertidumbre, estabilidad, número efectivo de decisiones, horas humanas y rendimiento prospectivo.
  No gana quien saque el mejor Sharpe (puede ser quien más combinaciones probó).
- **Familias candidatas:** A tendencia/momentum (prioridad), B reversión a la media, C regímenes de volatilidad, D cartera
  y diversificación, E generación con SQX medida como método. Empezar comparando A, B y E; D después; C solo con una
  hipótesis concreta. Un mercado, no muchos.
- **Cinco capas:** datos y ejecución fiel · motor de hipótesis · validador independiente · investigación asistida por IA
  (sin poder tocar reglas de aceptación ni el sellado) · economía y cartera. Módulos pequeños, no cinco programas.
- **Tres objetivos con criterios separados:** A ventaja estadística; B rentabilidad neta explotable; C que el proyecto
  compense económicamente (licencias, datos, horas, fiscalidad, capital inmovilizado, coste de oportunidad).
- **Secuencia:** cerrar bloqueos técnicos → piloto con tres lotes → definir la comparación justa → fijar por escrito
  presupuesto, horas y criterios de parada → solo entonces investigación comparativa y examen confirmatorio.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| SQX como un método más, no como el centro | **De acuerdo en el fondo.** La 0001 ya dice que la IA y las herramientas se quedan donde demuestren valor; faltaba decirlo de SQX | Se recoge en C20 y C21 |
| **Referencia simple frente a la que se mide todo** | **De acuerdo, y es lo más valioso de las revisiones 10–11.** La 0003 §3 (b) abandona si las candidatas "no baten con claridad a las referencias comparables", pero **nunca dice cuáles son**. Sin definirlas antes, se pueden elegir después a conveniencia (grado de libertad, regla 8) | **C20:** definir y preregistrar las referencias **antes del piloto** (p. ej. no operar; una regla de tendencia con parámetros fijados sin optimizar; entradas al azar con la misma exposición y costes). Cada referencia cuenta como hipótesis (regla 7). Entra en la 0003 cuando Diego la revise (A1) |
| Competición de tres métodos en paralelo | **En desacuerdo por ahora.** Triplica las pruebas y las horas de Diego, y con pocas candidatas no hay potencia para distinguir métodos (C7). El piloto es de 1 familia y así debe seguir | **D:** se reconsidera tras el piloto, si el coste por candidata válida lo permite |
| Familias A–E | Razonables como hipótesis; **ninguna tiene evidencia** en nuestro laboratorio. Elegir familia es de Diego con la 0003 | Se anotan como candidatas para la familia del piloto (A1b), sin preferencia de Claude todavía |
| Cinco capas | **No como arquitectura nueva** (C5 y la lista D lo descartan). Encajan casi una a una en lo que hay: datos (B1, C12), hipótesis (registro + regla 7), validador (H1–H2, C11), IA (0001), economía (A7) | Se usará al consolidar la arquitectura única al cerrar H0 (C5) |
| Objetivos A, B y C separados | De acuerdo; **amplía A7** con el objetivo C completo, incluido el **coste de oportunidad** | A7 ampliada |
| Secuencia | Coincide con la nuestra; añade "definir la comparación justa" antes de escalar, que es C20 | — |

### Aportación de Claude: un control negativo para la búsqueda

Ninguna revisión lo propone y es la versión barata de la pregunta de la 11 (¿SQX descubre o fabrica?). **Ejecutar la
misma búsqueda del piloto sobre datos sintéticos sin ventaja** (paseo aleatorio con la volatilidad y los costes del
instrumento, o rendimientos barajados). Si SQX y sus filtros "encuentran" en el ruido estrategias tan buenas como en los
datos reales, los filtros no discriminan y ninguna candidata real significa nada. No gasta datos de investigación ni del
sellado. Es lo mismo que aprendimos el 20-10 (un resultado igual necesita un control que pueda fallar), aplicado a la
búsqueda. Depende de poder importar datos propios en SQX por línea de comandos, que se comprueba en B1. → **B17**.

**Balance:** la 11 aporta **una idea clave** (definir las referencias antes) y una reformulación útil de la misión, que
decide Diego (A5). El resto, o ya estaba, o añadiría complejidad antes de tener datos que la justifiquen.
