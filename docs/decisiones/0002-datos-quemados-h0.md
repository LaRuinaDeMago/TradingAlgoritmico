# Decisión 0002 – Datos "quemados" para las pruebas de proceso de H0

Fecha: 2026-10-20 · Estado: **ACEPTADA** (Diego delega: "Lo que tú consideres correcto"; propuesta de Claude) · Sustituye a: —

## Contexto

La tarea 3 de H0 obliga a generar estrategias, hacer backtests y exportarlas por línea de comandos. Eso se hace con datos reales,
y todo lo generado con ellos queda **visto**: si después se investigara con esos mismos datos, los resultados estarían contaminados
por lo que ya sabemos de ellos. Además, cada estrategia generada es una hipótesis (decisión 0001, regla "toda hipótesis cuenta").

En el PC de SQX solo están los datos de ejemplo que trae SQX (registro n.º 17). El primer mercado de investigación aún no está decidido.

## Decisión

1. **Datos quemados para H0:** símbolo `USDCHF_M1_dukas` (datos de ejemplo de SQX, fuente Dukascopy, M1),
   **del 2023-01-01 al 2024-10-30** (fin de los datos instalados). Las pruebas usan H1 construido por SQX desde M1.
2. **Uso permitido:** solo comprobar que el proceso funciona (generar, backtest, exportar, registrar, reproducir) en H0 y H1.
   **Nunca** para afirmar ventaja, comparar estrategias por su calidad ni elegir qué investigar.
3. **Hipótesis:** cada ejecución anota en el registro cuántas estrategias generó, bajo la familia **`H0-proceso`**.
   Esa familia queda **fuera** de cualquier selección de candidatas: nada de ella puede pasar a investigación.
4. **Consecuencia para la investigación:** USDCHF no será el primer mercado de investigación. Si algún día se investiga, el periodo
   2023-01-01 – 2024-10-30 se declarará como visto y no podrá usarse como fuera de muestra.
5. **No se mira** ningún precio, gráfico ni resultado de USDCHF antes de registrar esta decisión.

## Por qué USDCHF y este periodo

- Es un par mayor con datos completos instalados (2003–2024), así que el proceso se prueba con datos realistas.
- Se elige sin haber visto sus precios ni resultados, y por eso no puede estar sesgado por ellos.
- Solo 22 meses: se quema lo mínimo necesario para que una generación tenga operaciones suficientes.
- Si se fija USDCHF como mercado excluido, los demás pares instalados (EURUSD, GBPUSD, USDJPY, oro, índices) quedan intactos.

## Cómo comprobarlo

- Cada registro de H0 que genere o haga backtests cita esta decisión, el símbolo y las fechas, y el hash de los datos usados.
- Revisión: cualquier registro de H0 con otro símbolo u otras fechas es un incumplimiento y se anota como tal.
