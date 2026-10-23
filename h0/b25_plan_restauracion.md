# B25 – Prueba de restauración (plan escrito ANTES de ejecutar)

Fecha: 2026-10-23 · Autor: Claude · Asunto B25 de `PENDIENTES.md`, punto (3): "desde un clon limpio + la copia, rehacer
el análisis de B17 v3 y obtener los mismos números (falsos positivos 16/2.002, p = 0,99) y comprobar los hashes".

## Pregunta

¿Se puede rehacer un resultado registrado **solo con lo que está en GitHub** (código, registro, evidencias) **más los
archivos de entrada**, y obtener exactamente lo mismo? Si no, ¿qué falta?

## Qué se rehace

El análisis de B17 v3 (registro **n.º 221**): `python -I h0/configs/b17_analizar.py 1000` sobre seis CSV de
`lab_h0\b17\`, en el commit registrado `65e9a57`. Es la conclusión más importante del laboratorio hasta hoy (D1).

## Cómo (`h0/configs/b25_restaurar.py`, 6 tests con 4 controles negativos)

1. Clon **desde GitHub** (no desde este disco) en el scratchpad de la sesión; registro y evidencias, de ese clon en su
   último commit; código, de un segundo clon en el commit `65e9a57`, sin cambios.
2. Datos de entrada: hoy, en su sitio original (`C:\StrategyQuantX145\user\lab_h0\b17\`). Cuando exista la copia de
   A14, se repite cambiando solo el prefijo de la ruta (opción `ORIGEN=DESTINO`): esa es la prueba completa de B25.

## Criterios (fijados ahora)

- **R1:** el clon de código está en el commit registrado y sin cambios.
- **R2:** el SHA-256 de cada archivo con hash en el registro coincide (3 CSV y `b17_analizar.py`).
- **R3:** la salida es **byte a byte** la de la evidencia registrada (`20261021T163802Z_b17_v3_analisis.txt`, sacada
  del clon de GitHub), con código de salida 0.
- **Informe, sin criterio:** los archivos que el comando lee **sin** hash registrado. Ya se sabe que son tres (los
  `Results_antes_*`, leyendo el registro): la prueba tiene que encontrarlos.

**Decisión:** R1–R3 → restauración desde GitHub + datos locales **SÍ**. Si falla R2 o R3, se diagnostica antes de
seguir con la fase 1 (un resultado que no se reproduce no puede sostener decisiones). Lo que no tenga hash se corrige
**hacia delante** (desde la fase 1, todo archivo que lea un análisis va en `--datos`), sin tocar el registro.

## Lo que no demuestra

Que la copia de A14 exista y se lea (eso es la segunda pasada); que un experimento **de SQX** se reproduzca (la
generación no tiene semilla, C18); que los CSV sin hash sean los que se usaron el 21-10 (no hay con qué comprobarlo,
salvo por coherencia: "antes del nulo 1" = "después del real", n.º 223).

## Resultado de la primera pasada (n.º 280–281, 2026-10-23)

- **R1 SÍ:** clon en `65e9a57`, sin cambios.
- **R3 SÍ:** la salida del análisis de B17 v3 es **byte a byte** la registrada (1.811 bytes, código 0). D1 se reproduce
  desde GitHub más los CSV de `lab_h0\b17`.
- **R2 SÍ en los tres CSV; NO, tal como se escribió, en `b17_analizar.py`.** Causa demostrada (n.º 281): el hash
  registrado es el del contenido del commit tal como lo guarda git (LF, 6.606 bytes); el clon lo saca con CRLF
  (`core.autocrlf=true` en este PC: 147 saltos, 6.753 bytes). Mismo código, distinto envoltorio.
- **Sin hash registrado:** los tres `Results_antes_*` (como se esperaba).
- **Veredicto:** restauración desde GitHub con datos locales **SÍ en lo que importa (mismo resultado, mismos datos)**;
  R2 queda NO para el código en esta pasada, como se midió.

## Criterio R2 para la segunda pasada (con la copia de A14), fijado ahora

Para los archivos **del repositorio** (rutas relativas), la referencia es su contenido en el **commit registrado**
(`git show COMMIT:RUTA`), no la copia de trabajo, cuyo salto de línea depende de cómo esté configurado git en cada
máquina. Para los archivos de fuera del repositorio, su hash tal cual. Implementado en `b25_restaurar.py` con dos tests
nuevos (CRLF en la copia de trabajo → igual; contenido distinto en el commit → distinto).

**Hacia delante (desde la fase 1):** todo archivo que lea un análisis va en `--datos`, también los que hoy se quedaron
sin hash.
