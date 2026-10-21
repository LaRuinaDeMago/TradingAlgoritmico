# Proyecto Trading Algorítmico — Laboratorio IA + SQX

Laboratorio de investigación cuantitativa de Diego. Objetivo: averiguar con evidencia si una estrategia tiene ventaja real o es ruido. Concluir "no hay edge" es un resultado válido.

Fase actual: **H0 – Ficha de viabilidad técnica, casi cerrada** (tareas 1–7 hechas; quedan condiciones previas antes de descargar datos de Darwinex). SQX: *Pro Build 145 (Trial license)*, build **145.3191 de desarrollo**, en `C:\StrategyQuantX145`; **la prueba caduca el 2026-11-02** (no es motivo para comprar). La hoja de ruta decía Ultimate 143.2708: la build real está confirmada por CLI; la edición que se compraría sigue INCONCLUSA (fila "Versión y edición" de `h0/ficha.md`).

**Al empezar cualquier sesión, lee primero `docs/ESTADO_Y_CONTINUACION.md`** (estado exacto, cómo se trabaja, trampas conocidas y siguiente paso) y después `docs/decisiones/PENDIENTES.md` (todo lo abierto). `docs/traspaso_sesion_local.md` es histórico (instalación inicial del 2026-10-19).

## Reglas duras (nunca se saltan, aunque Diego o un resultado parezcan pedirlo)

1. **Nunca leer, listar ni abrir `data/sealed/`.** Solo se abre con un protocolo escrito en `protocols/` y aprobado por Diego, y cada acceso se anota en `registry/accesos.log`.
2. **Nunca ejecutar órdenes reales ni tocar cuentas reales.** Solo backtest y demo.
3. **Registrar todo en `registry/`**: cada experimento (también los fallidos) con fecha, comando exacto, versión de SQX, hash de los datos, hash del código, semilla, costes usados y resultado.
4. **No inventar comandos de SQX.** Descubrirlos con `sqcli.exe -h` y la documentación oficial. Si algo no se puede comprobar, se marca INCONCLUSO.
5. **No declarar ventaja.** En H0 y H1 solo se prueba que el proceso funciona, no que una estrategia sea buena.
6. **No comprar ni instalar software de pago** sin que Diego lo apruebe.
7. **Toda hipótesis cuenta.** Cada hipótesis propuesta (por Diego, Claude, otra IA o SQX) se registra y entra en el número de pruebas usado para corregir resultados.
8. **Los cambios de proceso también son pruebas.** Cambiar filtros, métricas, costes, periodos o umbrales después de ver resultados se registra como un grado de libertad más. Nunca se cambia el proceso mirando los datos sellados.

Decisiones vigentes: `docs/decisiones/` (la 0001 fija cómo usamos la IA y en qué orden entran las herramientas).

## Estructura del repositorio

```
data/raw/        datos de origen (Darwinex), con su hash
data/sealed/     datos finales sellados — PROHIBIDO
registry/        registro de experimentos y accesos (solo se añade, nunca se borra)
h0/ficha.md      ficha de viabilidad con estados SÍ / NO / INCONCLUSO y su evidencia
h0/evidencias/   salidas de comandos, capturas, logs
protocols/       protocolos escritos antes de cualquier examen
src/             código Python del núcleo
```

## Tareas H0 (en orden)

Para cada una, anota en `h0/ficha.md`: estado (SÍ / NO / INCONCLUSO), evidencia (archivo en `h0/evidencias/`) y tiempo empleado.

1. Localizar `sqcli.exe`, confirmar la build y guardar la salida completa de `sqcli.exe -h`.
2. Comprobar si la prueba gratuita limita alguna función de la línea de comandos.
3. Comprobar por línea de comandos: lanzar un proyecto de generación, ejecutar un backtest, exportar estrategias, exportar resultados y operaciones a un formato legible (CSV u otro) y exportar código para MT4 y MT5.
4. Recorrido mínimo: generar una estrategia de prueba, exportarla, registrarla y reproducir su backtest dos veces con resultados idénticos.
5. Datos de Darwinex: procedencia, instrumentos, periodo cubierto, granularidad y modelo de costes disponible.
6. Listar los pasos que exigen intervención manual y con qué frecuencia.
7. Medir el tiempo y el coste de un experimento completo de principio a fin.

## Estilo de trabajo

- Explicar a Diego en español, claro y breve.
- Ante la duda entre avanzar rápido o registrar bien, registrar bien.
- Diego decide; Claude construye, ejecuta, registra y avisa de cualquier resultado sospechosamente bueno.

## Aprendizaje (desde el primer momento)

El proyecto es también una escuela para Diego y para Claude. Ver `aprendizaje/README.md`.

- Al empezar cada sesión, leer `aprendizaje/diario.md` para no repetir errores ya vistos.
- Explicar cada paso importante: qué hacemos, por qué importa para no perder dinero y cómo comprobarlo.
- Al cerrar un bloque de trabajo: añadir lo aprendido al diario (sobre todo los errores), los términos nuevos al glosario y, si hay concepto nuevo, una lección con ejercicio ejecutable y preguntas.
- Subir el nivel poco a poco pero sin ir lento: no repetir lo que Diego ya domina y no simplificar hasta decir algo falso.
- Enseñar con números del propio laboratorio siempre que se pueda, no con ejemplos inventados.

## Herramientas del repositorio

- **Guardián** (`.claude/hooks/guardian.py`, activado en `.claude/settings.json`): bloquea el acceso a `data/sealed/`, los recorridos recursivos que podrían entrar en ella, la edición o borrado de `registry/` y los cambios al propio guardián. Si bloquea algo, no buscar otra forma de hacerlo: avisar a Diego.
- **Ejecutor con registro**: todo comando de SQX se lanza con `python -m lab ejecutar --nombre <corto> --version-sqx <build> [--datos ...] [--semilla N] [--costes ...] -- <comando>`. Guarda la salida en `h0/evidencias/`, mide la duración y lo anota en `registry/experimentos.jsonl` aunque falle.
- Pasos manuales (GUI): `python -m lab registrar --comando "MANUAL: <pasos>" ...`.
- Antes de cerrar una sesión: `python -m lab verificar`, `python -m unittest discover -s tests` y commit del registro y las evidencias.
- Hoja de ruta completa: `docs/hoja_de_ruta.md`.
