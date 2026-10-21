# B16 – Licencia de SQX frente al calendario

Fecha: 2026-10-21 · Autor: Claude · Asunto B16 (revisión 09, H7). Base para la decisión **A12**, que es de Diego.
Regla de la 0003 §3: **que caduque la prueba no es un motivo para comprar.**

## 1. Hechos comprobados

| Hecho | Fuente |
|---|---|
| Instalado: *StrategyQuant X Pro Build 145 (Trial license)*, build 145.3191 de desarrollo; la prueba caduca el **2026-11-02** | Registros n.º 9–11, `h0/ficha.md` |
| La web oficial ofrece una prueba de **14 días**, "fully functional"; las compras **no se reembolsan** | strategyquant.com/pricing (consultada 2026-10-21) |
| Precios (USD sin IVA; la web muestra dos cifras por edición sin decir cuál rige): Starter 1.290 · Professional 1.490 o 1.790 (1 año de actualizaciones; ampliar, 300) · Ultimate 2.900 o 4.900 (actualizaciones de por vida). A plazos, +17 % | Ídem |
| **Starter no tiene Walk-Forward, Monte Carlo ni Optimizer** → no sirve para el método de la 0003 | Ídem |
| Funciones solo de Ultimate en la documentación instalada: ATM y generación de salidas múltiples (no las usamos) | `C:\StrategyQuantX145\docs\overview\settings\multiple-exits.md`, `…\fields\atm.md` |
| La prueba ("Special Trial") desactiva algunos cross checks; WFO y What If sí funcionaron en H0 | `docs\overview\snippets\cross-checks.md`; registros n.º 57–71 |

## 2. INCONCLUSO (no se puede afirmar todavía)

1. **Si Professional incluye la línea de comandos (`sqcli`).** Ni la tabla de precios ni la documentación lo dicen. Sin
   CLI, el laboratorio tal como está construido (ejecutor con registro, tandas reproducibles) no funciona.
2. **Qué hace SQX al caducar la prueba:** si deja de arrancar, si solo bloquea la generación o si permite exportar.
3. **Si los datos de Darwinex** (328 símbolos, registro n.º 87) siguen accesibles con Professional, o dependen de la
   edición o de la cuenta.
4. **Exportar código MT4/MT5** por edición: la tabla solo lo asocia a "SQ for Business"; en la prueba Pro sí exportó
   (registros n.º 27–31).
5. **Si la build final** (no la 145.3191 de desarrollo) se comporta igual en lo que hemos comprobado.

→ Se resuelven preguntando al soporte (texto en §5) y, el 2026-11-02, observando qué pasa (registrado).

## 3. Qué necesita SQX y qué no

| Tarea | ¿Necesita SQX? | Antes del 02-11 |
|---|---|---|
| B1 integridad exportar/importar | Sí | **Hacerla ya** |
| Exportar a CSV todo lo que H1 necesita para la reconstrucción en Python (velas M1 de USDCHF quemado, operaciones de las estrategias de H0, código) | Sí | **Hacerlo ya** (B1 deja exportadas las velas de la ventana W) |
| Descargar Darwinex | Sí (y A12 si caduca) | **No**: faltan B15, B18 y el protocolo aprobado |
| Piloto de búsqueda (0003) | Sí | No (va después de Darwinex) |
| B14 registro tipado, B18 revisión del curso, C20 referencias, diseño de B17, reconstrucción en Python | No | Se pueden hacer con o sin licencia |

**Consecuencia:** la investigación con Darwinex **no puede empezar antes del 02-11** por condiciones previas, no por la
licencia. Después del 02-11, sin licencia, el laboratorio sigue avanzando en todo lo que no necesita SQX. Con eso, la
decisión A12 puede tomarse con calma y con las respuestas del §2, no con prisa por la caducidad.

## 4. Recomendación de Claude (la decisión es de Diego, A12)

1. **No comprar antes del 02-11.**
2. **Pedir al soporte** las respuestas del §2 y, de paso, una **ampliación de la prueba**, porque el proyecto aún no ha
   podido usar SQX con los datos que importan. No cuesta nada y es habitual que lo concedan.
3. Si hiciera falta comprar, la candidata es **Professional** (la más barata que tiene WF, MC y Optimizer),
   **solo si** el soporte confirma la CLI y los datos de Darwinex. Ultimate no aporta nada que el método use hoy.
4. Antes de comprar, el criterio de la 0003 v6: el gasto se justifica por el trabajo concreto que permite (el piloto y
   su control negativo), no por lo ya invertido.

## 5. Texto para el soporte de StrategyQuant (lo envía Diego si quiere)

> Hello, I'm evaluating StrategyQuant X with the trial (Pro, build 145.3191) and it expires on 2 Nov 2026.
> Before deciding which edition to buy, could you confirm:
> 1. Is the command line interface (sqcli.exe) fully available in the Professional edition?
> 2. Are Darwinex data downloads (datasource=darwinex) available in Professional?
> 3. Does Professional allow exporting strategy source code for MetaTrader 4 and 5?
> 4. What happens when the trial expires (does the program stop starting, or are only some functions locked)?
> 5. Is it possible to extend the trial? We are running a structured evaluation and have not yet been able to test with
>    the data we will use.
> Thank you.

Fuentes web: [precios](https://strategyquant.com/pricing/), [introducción a la CLI](https://strategyquant.com/doc/cli-command-line/introduction-to-cli/).
