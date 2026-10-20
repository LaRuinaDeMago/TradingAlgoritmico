# Glosario

Se amplía con cada lección. Entre paréntesis, la lección donde aparece por primera vez.

- **Backtest**: simular cómo habría funcionado una estrategia con datos históricos. (01)
- **Commit**: foto del estado del código guardada en git, con fecha y un identificador único (su hash). (01)
- **Datos sellados**: el conjunto de datos reservado como examen final; solo se abre una vez, con un protocolo escrito antes. (01)
- **Edge (ventaja)**: esperanza de ganancia positiva después de costes, que no se explica por el azar. (01)
- **Error típico**: cuánto variaría una medida si repitiéramos el experimento con otros datos del mismo tipo. (01)
- **Falso positivo / falso negativo**: aprobar algo que no lo merece / rechazar algo que sí lo merecía. (01)
- **Hash (SHA-256)**: huella de 64 caracteres de un archivo; cambia por completo si cambia un solo byte. (01)
- **Hook (gancho)**: programa que Claude Code ejecuta automáticamente antes o después de cada acción; aquí, el guardián. (01)
- **Pruebas múltiples**: al probar muchas cosas, alguna sale bien por azar; hay que corregir por el número de pruebas. (01)
- **Ratio de Sharpe**: rentabilidad media dividida entre su variabilidad, anualizada. Mide la ganancia por unidad de riesgo. (01)
- **Registro solo-añadir**: registro donde solo se escriben líneas nuevas; nunca se editan ni se borran las anteriores. (01)
- **Semilla**: número que fija el punto de partida del azar del ordenador; con la misma semilla, el mismo resultado. (01)

Términos aparecidos trabajando en H0 (2026-10-20), sin lección propia todavía (entre paréntesis, el registro):

- **Control negativo**: repetir una prueba cambiando a propósito algo que *debe* alterar el resultado. Si el resultado no cambia, el "sale igual" no demostraba nada. Ejemplo: spread 3 en vez de 2 → 0 de 10 iguales (n.º 49–53).
- **Control positivo**: incluir algo que *sí debe* funcionar, para distinguir "está bloqueado" de "no se ejecuta nada" (Monte Carlo en la tarea 2, n.º 57–61).
- **Datos quemados**: datos gastados a propósito en pruebas de proceso; quedan vistos y no se usan para investigar (decisión 0002, n.º 18).
- **Evidencia redactada**: copia pública de una evidencia con los datos privados sustituidos por `[REDACTADO:tipo]`; el original queda solo en el PC (n.º 10).
- **Experimento discriminante**: el que da resultados distintos según cuál de dos explicaciones sea la cierta (Walk-Forward Matrix, n.º 62–65).
- **Fuera de muestra (OOS)**: datos que no se usaron para construir u optimizar la estrategia; solo ahí se puede medir si generaliza.
- **Walk-forward**: optimizar con un tramo de datos, probar en el siguiente tramo no usado, avanzar la ventana y repetir. Mide si los parámetros optimizados aguantan en datos nuevos (n.º 59).
