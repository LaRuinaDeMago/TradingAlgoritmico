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
- **Referencia (benchmark)**: estrategia sencilla fijada de antemano (no operar, una regla sin optimizar, entradas al azar con la misma exposición) que una candidata debe batir con claridad. Si se elige después de ver resultados, deja de ser una referencia y pasa a ser un grado de libertad (C20).
- **Control negativo de la búsqueda**: lanzar la misma búsqueda sobre datos sintéticos que, por construcción, no tienen ventaja. Lo que "encuentre" ahí mide cuánto fabrica el proceso por azar (B17).
- **Coste de oportunidad**: lo que habrían rendido el mismo dinero y las mismas horas en la mejor alternativa sencilla; el proyecto solo compensa si lo supera (A7).
- **Calentamiento de indicadores (warm-up)**: velas previas que un indicador necesita para dar su primer valor. Un backtest que empieza en el primer dato disponible opera distinto al principio que uno con historia previa (B1: 18 operaciones de la primera semana); se evita con un margen previo (B1-bis).
- **Desbordamiento (entero de 32 bits)**: un número mayor que 2.147.483.647 no cabe en ese tipo de dato; SQX lo recorta al máximo al importar volúmenes (B1).
- **Distribución nula simulada**: lo que da un procedimiento (búsqueda, filtros, costes) cuando se le pasan datos fabricados sin ninguna ventaja. Es la referencia correcta para saber si un resultado real es mejor que el azar; compararlo con cero no basta, porque los costes ya crean patrones (B17).
- **Tasa de falsos positivos de un embudo**: fracción de estrategias que aprueba un conjunto de filtros cuando no hay nada que aprobar. En B17: 0,8 % sin costes y 0,1 % con costes.
- **Desalojo de un banco de estrategias**: cuando el banco de SQX llega a su capacidad, entra lo nuevo con mejor fitness y sale lo peor, sin avisar. Convierte "guardar todo" en "guardar lo mejor": una selección escondida (B17).
- **Etiqueta de zona horaria**: dato que dice en qué hora están las velas, sin cambiarlas. En SQX, una etiqueta equivocada no se nota en el backtest: el reloj real de los datos hay que comprobarlo por fuera (B1, B4).
- **Walk-forward**: optimizar con un tramo de datos, probar en el siguiente tramo no usado, avanzar la ventana y repetir. Mide si los parámetros optimizados aguantan en datos nuevos (n.º 59).
- **Ventaja sembrada**: ventaja pequeña, de tamaño conocido, metida a propósito en datos sintéticos para medir si un procedimiento la encuentra (su *potencia*). Complementa a la distribución nula: una mide cuánto se equivoca aprobando ruido; la otra, cuánto se equivoca dejando pasar señal (0004, P3).
- **Potencia de un procedimiento**: probabilidad de detectar una ventaja que sí existe, de un tipo y tamaño dados. Sin medirla, "no encontramos nada" no distingue entre "no hay" y "no sabemos ver" (0004).
- **Fuga de información (sesgo de anticipación)**: usar, al decidir una operación, datos que en ese momento aún no existían (el cierre de la vela en curso, un dato corregido después). Invalida cualquier resultado, por bueno que sea el resto (0004, P12).
- **Controles de desarrollo y de aceptación**: los primeros se usan para ajustar el procedimiento; los segundos se fijan antes y no se miran hasta el final, para que el procedimiento no se "adapte" a sus propios controles (0004, P3).
- **Amplitud efectiva**: número de apuestas de verdad independientes de una cartera. Diez pares con dólar pueden ser casi una sola apuesta (ley fundamental de la gestión activa, IR ≈ IC·√B; 0004, P1).
- **Expectativa por operación**: lo que se gana de media en cada operación, neto de costes: E = p·G − (1−p)·L − C. Es lo que decide, no el porcentaje de acierto ni el ratio configurado (C24).
- **Racha de pérdidas esperada**: con un acierto p, en n operaciones la racha más larga de pérdidas ronda ln(n·p) / ln(1/(1−p)). Con 30 % y 300 operaciones, ~12 pérdidas seguidas: es lo normal, no una avería (C24).
- **Tramo de reserva**: parte final de cada serie que ningún filtro ni selección toca; sirve de examen dentro de una prueba de proceso (fase 1).
- **Remuestreo por bloques**: fabricar series nuevas reordenando trozos (días, semanas) de la original en vez de velas sueltas, para conservar parte de su estructura (volatilidad, horarios) sin su dirección (fase 1, nulos N2 y N3).
- **Réplica**: repetición completa de un experimento con datos nuevos del mismo tipo (otra semilla, otra serie sintética). Es la unidad de observación cuando se calibra un procedimiento: las estrategias de una misma réplica no son independientes (fase 1).
- **Regla del tres**: si algo no ocurre en R intentos independientes, su probabilidad todavía puede ser de hasta ~3/R (95 %). Con 3 réplicas sin falsos positivos, la tasa real puede llegar al 63 % (cálculo exacto: 1 − 0,05^(1/R)).
- **Memoria experimental**: todo lo necesario para repetir un experimento y obtener lo mismo: código (git), datos de entrada (con hash), configuración, semillas, salidas y registro. Si falta una pieza o solo existe en un disco, el experimento no es reproducible aunque esté anotado (B25).
- **Prueba de restauración**: rehacer un experimento desde la copia de seguridad, en limpio, y comprobar que salen los mismos números y hashes. Es lo único que demuestra que una copia sirve (B25).
- **Hash de contenido**: huella de lo que hay dentro de un archivo empaquetado (cada archivo interno y sus bytes), sin la fecha ni la compresión del paquete. SQX reescribe sus `.sqx` (zip) en cada arranque: el hash del archivo cambia y el de contenido no. Para saber si una estrategia es la misma, se compara el contenido (B21).
- **Valor centinela**: número que un programa pone cuando el cálculo no tiene sentido (p. ej. dividir por un drawdown de 0). SQX pone Ret/DD = 10 y factor de beneficio = 5 a las estrategias sin ninguna pérdida; parecen buenísimas y casi siempre tienen una sola operación (B20).
- **Condición de carrera**: dos operaciones que van a la vez y cuyo resultado depende de cuál termina antes. En SQX, la carga de estrategias es asíncrona: un recuento lanzado en el mismo proceso puede contar a medias (6.747 de 7.003). Se evita esperando a que una termine, aquí con órdenes separadas (B21).
- **Memoria de Java (heap)**: memoria máxima que puede usar SQX. Si se acaba al cargar un banco, SQX no carga el resto y, al salir, borra esos archivos de la carpeta. La línea de comandos tenía 4 GiB y la interfaz 8 GiB; desde A24, las dos 8 GiB (B21).
