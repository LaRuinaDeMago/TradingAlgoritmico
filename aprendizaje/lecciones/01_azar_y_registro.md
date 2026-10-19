# Lección 01 – El azar que parece ventaja, y cómo nos protegemos de él

Nivel 1 · Hito H0 · Lo que construimos el primer día y el porqué de cada pieza.

## 1. El problema, con números

El ratio de Sharpe mide cuánto gana una estrategia por cada unidad de riesgo que asume:
rentabilidad media dividida entre su variabilidad, en términos anuales. Como orientación,
un Sharpe anual de 1 sostenido en el tiempo ya es muy bueno, y uno de 2 es excepcional.

El ejercicio [`01_azar_que_parece_edge.py`](../ejercicios/01_azar_que_parece_edge.py) crea un mercado
**sin ventaja para nadie** y N estrategias que cada día compran o venden **lanzando una moneda**.
Ninguna tiene ventaja real. Resultado (semilla 2026):

| Estrategias probadas | Años de datos | Sharpe medio | Sharpe de la mejor | Con Sharpe > 1 |
|---|---|---|---|---|
| 10 | 5 | +0,08 | +0,90 | 0 |
| 1.000 | 5 | −0,00 | **+1,60** | 8 |
| 10.000 | 2 | +0,01 | **+2,66** | 779 |

Si de las 10.000 solo enseñas la mejor, tienes un "sistema" con Sharpe 2,66. Es ruido puro.

### Por qué pasa

Con datos limitados, el Sharpe que mides tiene un error. Con rentabilidades diarias independientes,
el error típico del Sharpe anual es más o menos **1 / √años**: con 5 años, ±0,45; con 2 años, ±0,71.
Una estrategia sin ventaja dará un Sharpe medido de 0 ± 0,45, unas veces más y otras menos.

Cuando eliges **la mejor de N**, eliges a propósito la que tuvo más suerte. El máximo de N valores
aleatorios crece como **√(2·ln N)** errores típicos:

- N = 10 → 2,1 errores típicos
- N = 1.000 → 3,7
- N = 10.000 → 4,3

Por eso el ejercicio imprime la "aproximación teórica" √(2·ln N)/√años. Fíjate en que da algo más
que lo observado (1,66 frente a 1,60; 3,03 frente a 2,66): es una aproximación asintótica, buena para
el orden de magnitud y algo pesimista cuando N no es enorme. Mejor así, a favor de la prudencia.

### Qué tiene que ver con SQX

SQX genera y prueba miles o cientos de miles de estrategias, y su banco de datos muestra las mejores.
Es exactamente el experimento de arriba, con más parámetros. Los filtros de robustez de SQX (Monte Carlo,
walk-forward, otros mercados) ayudan, pero no anulan el problema: también se eligen después de ver resultados.

**Conclusión:** un resultado no vale nada si no sabes **cuántas cosas probaste para llegar a él**.

## 2. Cómo nos protegemos (lo que construimos y por qué)

### Registrar todo, también lo fallido
Si solo apuntas lo que sale bien, no sabes N, y sin N no puedes corregir el efecto de arriba.
Por eso `python -m lab ejecutar` registra cada experimento **aunque falle**, y por eso la decisión 0001
añade que toda hipótesis cuenta, venga de quien venga (Diego, Claude, otra IA o SQX).

### Hash SHA-256: la huella de un archivo
Un hash convierte un archivo de cualquier tamaño en 64 caracteres. Si cambia un solo byte, el hash cambia
por completo, y es prácticamente imposible encontrar dos archivos distintos con el mismo hash.
Lo usamos para saber **exactamente** con qué datos y con qué código se hizo cada experimento.
Ejemplo real: vuelves a descargar datos de Darwinex y han corregido unas velas. Sin hash no te enteras
y tu backtest "ya no da lo mismo" sin explicación. Con hash, lo ves al instante.

### Registro encadenado: que no se pueda maquillar
Cada entrada de `registry/experimentos.jsonl` guarda el hash de la anterior. Si alguien edita o borra una línea
intermedia, la cadena se rompe y `python -m lab verificar` lo detecta. Límite: borrar la **última** línea no rompe
nada. Por eso hacemos commit en git al final de cada sesión y lo subimos a GitHub, que guarda la fecha y queda fuera de nuestro PC.

### Datos sellados: el examen que solo se hace una vez
Si miras el examen final mientras estudias, la nota deja de medir lo que sabes. Los datos sellados son ese examen.
Cada vez que se miran, dejan de ser independientes. Por eso:
- Antes de abrirlos se escribe el protocolo: qué estrategia, qué métricas y **qué decisión se toma con cada resultado**.
- Después, ese conjunto ya no sirve como examen final de la siguiente iteración.

### El guardián: reglas impuestas, no solo escritas
Las reglas escritas se olvidan con las prisas o cuando un resultado ilusiona. El guardián (un *hook* de Claude Code)
revisa cada acción **antes** de ejecutarla y bloquea lo prohibido.
Hoy mismo dio dos falsas alarmas: confundió la función `zip()` de Python con el compresor `zip`.
Es el mismo dilema que validar estrategias:
- **Falso positivo** (bloquear algo inocente): molesta, pero no cuesta dinero.
- **Falso negativo** (dejar pasar algo prohibido): invalida el experimento.
Elegimos ser estrictos y aceptar algunas molestias. Igual que al aprobar estrategias: preferimos rechazar una buena
antes que aprobar una mala.

### Semilla: el azar reproducible
Los ordenadores generan azar con una fórmula que arranca desde un número, la semilla. Misma semilla, mismo resultado.
Así cualquier experimento con azar (Monte Carlo, bootstrap, el ejercicio de hoy) se puede repetir y comprobar.

## 3. Ejercicios (en tu PC, desde la carpeta del proyecto)

1. **Predice antes de ejecutar.** ¿Qué Sharpe tendrá la mejor de 100 estrategias con 10 años de datos?
   Calcúlalo con la fórmula √(2·ln 100)/√10 y después compruébalo:
   ```
   python aprendizaje/ejercicios/01_azar_que_parece_edge.py --estrategias 100 --anios 10
   ```
   ¿Qué ves? Que **más años de datos** reducen el problema, porque el error típico baja.
2. **Cambia la semilla** (`--semilla 1`, `--semilla 2`...). La mejor cambia, pero el orden de magnitud no.
3. **Hash.** Crea un archivo `prueba.txt`, calcula `python -m lab hash prueba.txt`, cambia una letra y vuelve a calcularlo.
4. **Rompe un registro (en una carpeta de pruebas, nunca en el real):**
   ```powershell
   $env:LAB_RAIZ = "$env:TEMP\lab_prueba"; $env:PYTHONPATH = "src"
   python -m lab registrar --descripcion "uno" --comando "x" --version-sqx N/A --estado OK --resultado 1
   python -m lab registrar --descripcion "dos" --comando "x" --version-sqx N/A --estado OK --resultado 2
   python -m lab verificar
   notepad "$env:TEMP\lab_prueba\registry\experimentos.jsonl"   # cambia "resultado": 1 por 9 y guarda
   python -m lab verificar
   Remove-Item Env:LAB_RAIZ
   ```

## 4. Comprueba que lo has entendido

1. Un vendedor te enseña una estrategia con Sharpe 2,5 en 3 años de backtest. ¿Qué es lo primero que le preguntas?
2. ¿Por qué registrar un experimento que falló, si "no sirve para nada"?
3. Hemos mirado los datos sellados y la estrategia ha salido mal. La retocamos un poco. ¿Podemos volver a evaluarla en los mismos datos sellados?
4. ¿Qué detecta el registro encadenado y qué **no** detecta?

<details>
<summary>Respuestas</summary>

1. ¿Cuántas estrategias, variantes y parámetros probó hasta llegar a esa? Con 3 años, el error típico es ±0,58. Con unas 1.000 pruebas, la mejor sin ventaja ya rondaría 3,7 × 0,58 ≈ 2,1.
2. Porque cuenta para N. Sin los fallidos, el número de pruebas parece menor y cualquier resultado parece más significativo de lo que es.
3. No. Ya no son un examen independiente: el retoque se ha hecho sabiendo cómo salió. Hacen falta datos nuevos (o esperar a acumularlos en demo).
4. Detecta ediciones y borrados intermedios. No detecta que se borre la última línea; eso lo cubre el historial de git en GitHub.
</details>

## Lo que viene (nivel 2)

Cómo funciona un backtest por dentro y las cuatro formas más habituales de que mienta:
costes irreales, sesgo de anticipación, datos de mala calidad y confundir "dentro de muestra" con "fuera de muestra".
