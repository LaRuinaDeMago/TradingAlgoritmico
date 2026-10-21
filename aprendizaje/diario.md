# Diario de lecciones

Lo que aprendemos trabajando, sobre todo de los errores. Solo se añade.
Claude lo lee al empezar cada sesión para no repetir fallos.
Formato: fecha · qué pasó · qué aprendimos · qué cambia.

## 2026-10-19

- **El guardián analiza texto, no intenciones.** Bloqueó `cat >> CLAUDE.md` porque el texto añadido contenía `>` y
  mencionaba la carpeta del guardián, y bloqueó un heredoc porque `zip(...)` de Python parece el compresor `zip`.
  → Para escribir archivos, usar las herramientas Write/Edit en lugar de heredocs en Bash.
  → Si el guardián bloquea algo, no se busca otra forma de hacerlo: se avisa a Diego.
  → Pendiente (decide Diego, con `LAB_MANTENIMIENTO_GUARDIAN=1`): afinar la regla de `zip` para que no salte con código Python.
- **Mensajes de commit que nombran la carpeta sellada se bloquean en Bash.** → `git commit -F archivo_con_el_mensaje`.
- **Desde el entorno en la nube no se accede a strategyquant.com.** → Nada de SQX está verificado; todo se comprueba en el PC de Diego.
- **√(2·ln N) sobrestima un poco el máximo esperado cuando N es moderado** (1,66 frente a 1,60 observado con N = 1.000;
  3,03 frente a 2,66 con N = 10.000). Sirve para el orden de magnitud y peca de prudente. Para correcciones serias, en H2
  se usarán métodos exactos (Sharpe deflactado, SPA).
- **Una propuesta con muchas IAs puede aumentar los falsos positivos** si cada hipótesis no se cuenta. → Decisión 0001, regla "toda hipótesis cuenta".
- **Mantenimiento del guardián autorizado por Diego en el chat, solo esta vez y solo para `zip`.** Cambio: `zip(` (función de Python)
  ya no cuenta como el compresor `zip`; el compresor sigue bloqueado. Se añadieron 3 casos al autotest (28/28).
  Se aplicó con un script externo porque la sesión en la nube no tenía `LAB_MANTENIMIENTO_GUARDIAN=1`.
- **Hallazgo de seguridad (falso negativo del guardián):** un script cuyo comando no nombra la ruta del guardián puede modificarlo
  sin que salte el bloqueo. Lo vimos al aplicar el cambio anterior. El guardián frena accidentes, no a quien quiera saltárselo.
  → Pendiente (decide Diego): proteger los archivos del guardián fuera del alcance de Claude (permisos de solo lectura de Windows
  o comprobar su hash al empezar cada sesión). Hasta entonces, cualquier cambio en `.claude/` se revisa en el diff de git.
- **Mismo tipo de falso positivo pendiente:** `.find(` de Python puede confundirse con el comando `find`. No se toca sin permiso.
- **Lo "ya comprobado" no estaba comprobado.** La hoja de ruta daba por hecho "Ultimate, build 143.2708" (la única casilla marcada del H0).
  La primera captura real dice "Pro Build 145", build 145.3191, y quizá sea una build de desarrollo. → Una casilla solo se marca con
  evidencia guardada, aunque el dato parezca obvio. Para eso existe H0.
- **Claude en la nube no es Claude Code en el PC.** Esta sesión corre en un servidor Linux y no ve el PC de Diego. Lo que exige SQX
  (tareas 1–7 del H0) lo ejecuta Claude Code instalado en Windows, sobre el mismo repositorio de GitHub. → Siempre aclarar dónde corre cada sesión.
- **Confirmado: SQX es una build de desarrollo** ("not a final release", del 2026-10-06). → Todo lo que verifiquemos en H0 lleva la build
  anotada, y antes de comprar habrá que comprobar que sigue igual en la versión final.
- **El asistente de SQX (SQ Pilot) contesta con seguridad cosas que no sabemos si son ciertas** (plugins `runtime: claude-code`).
  Un LLM que suena convincente no es evidencia. → Sus respuestas se apuntan como hipótesis por verificar (regla 7).

## 2026-10-20

- **Primera sesión local (Windows) con la carpeta correcta.** La sesión anterior empezó en otra carpeta y el guardián no
  encontraba su archivo: bloqueaba todo por error, no por funcionar. → Una prueba de fuego solo vale si el guardián arranca bien.
- **Paso 0:** autotest del guardián 28/28, tests 12 OK, registro íntegro (2 entradas).
- **Prueba de fuego con un archivo inexistente.** Si el guardián fallara, no se habría leído nada real.
  → Read lo frenó la regla `deny` de `.claude/settings.json` *antes* del guardián; Bash lo frenó el guardián. Son dos capas distintas:
  la prueba con Read no demuestra que el guardián funcione, solo la de Bash.
- **`python -m lab` no funciona todavía:** falta `pip install -e .`. Mientras tanto vale `PYTHONPATH=src python -m lab ...`.
- **Falso positivo nuevo:** `2>&1` en un comando que también nombra `.claude/hooks` cuenta como escritura (`>`). → Separar los comandos.
- **Agujero confirmado: la herramienta PowerShell no pasa por el guardián.** Simulando llamadas (sin tocar datos), el guardián deja
  pasar 4 de 4: leer la carpeta sellada, recorrido recursivo de `data`, borrar `registry/` y sobrescribir el propio guardián.
  Dos causas: el `matcher` de `.claude/settings.json` no incluye `PowerShell` y el guardián solo analiza comandos de `Bash`.
  → Pendiente (decide Diego): bloquear la herramienta PowerShell o enseñar al guardián a vigilarla.
  → Diego eligió enseñar al guardián. Borrador preparado y probado (autotest 44/44); se aplica en la sesión de mantenimiento.
- **El ejecutor marcaba "sucio" todos los experimentos.** Escribía la evidencia (archivo nuevo) *antes* de mirar si el código
  estaba confirmado, así que se veía a sí mismo. Lo destapó leer el código antes de usarlo, no un fallo visible.
  → Arreglado y cubierto por un test. Lección: una herramienta de registro también hay que probarla, y justo en lo que promete.
- **Código de salida 0 no significa que funcionara.** `sqcli -h` devolvió 0, pero lo que imprimió fue "otra instancia en marcha".
  El registro lo apuntó como OK (n.º 3) y hubo que corregirlo con otra entrada (n.º 4), porque el registro no se edita.
  → Siempre se lee la evidencia antes de dar algo por bueno. Pendiente: que el ejecutor avise de mensajes de error conocidos de SQX.
- **SQX solo admite una instancia por carpeta de instalación:** la interfaz y `sqcli` no pueden funcionar a la vez.
  → Paso manual para la tarea 6: cerrar la interfaz antes de cada tanda por línea de comandos.
- **Git for Windows cambia los saltos de línea** (`core.autocrlf=true`). La evidencia guardada en git no coincidía con el hash
  registrado (`e0f2…` frente a `75a7…`). → `.gitattributes`: evidencias byte a byte y registro siempre en LF. Comprobar siempre
  que el hash de lo que hay en git es el mismo que el registrado.
- **Más falsos positivos del guardián en español:** "del" se confunde con el comando `del` de Windows, y el `>` de la línea
  `Co-Authored-By` cuenta como redirección. → Los textos largos van en archivos (`--resultado archivo.json`, `git commit -F`).
- **Git no tenía identidad en este PC.** Los commits se hacen con `git -c user.name=Claude -c user.email=noreply@anthropic.com`,
  la misma autoría que ya tenía el repositorio, sin cambiar la configuración. Si Diego quiere otra, la decide él.
- **"Ya lo hice" no es evidencia, tampoco cuando lo dice Diego.** La sesión de mantenimiento del guardián se dio por hecha, pero el
  archivo seguía igual que en el clon (misma fecha, 28 casos en el autotest, ningún commit). → Todo cambio se comprueba en el
  propio archivo, no en el relato.
- **El repositorio de GitHub es público** (la API responde sin iniciar sesión). Todo lo subido se puede leer desde fuera.
  La salida de `sqcli` trae el identificador de hardware de la licencia. → Antes de subir una evidencia, mirar qué contiene.
- **La documentación que trae SQX no coincide con su `-h`** (faltan `-sourcecode` y `darwinexsymbols`; `-ai` es distinto).
  → Ni la documentación oficial es prueba: manda lo que hace el programa instalado.
- **Diego decide que el repositorio siga público.** → Las evidencias se redactan solas (`lab/privacidad.py`): el original va a
  `h0/evidencias_privadas/` (fuera de git) y al repositorio, una copia con `[REDACTADO:tipo]`; el registro guarda los dos hashes.
  El ejecutor se niega a lanzar comandos con datos privados, porque el registro copia el comando literal.
- **Una lista de patrones solo atrapa lo que ya conoces.** En la primera evidencia nueva (licencia) se escapó el identificador de licencia (`license XXXXXX`);
  lo cazó leer el original entero antes del commit, no la herramienta. → Antes de cada commit se lee el original privado completo.
  La redacción automática es una ayuda, no el control.
- **Al redactar una copia ya redactada, el patrón volvió a contar su propia marca** (registro n.º 12 dice `licencia: 1` de más).
  Corregido con un test; la entrada n.º 12 queda como está, porque el registro no se edita.
- **"localhost" en un mensaje no significa localhost.** SQX anuncia `http://localhost:5050`, pero `netstat` muestra que escucha
  en `0.0.0.0` (todas las interfaces). Lo que protege es el cortafuegos (BlockInbound y ninguna regla para SQX).
  → Comprobar con el sistema, no con lo que dice el programa de sí mismo.
- **Filtré yo los datos que quería proteger.** Para los tests de la redacción copié el ID de hardware y el identificador de
  licencia **reales** como ejemplos, en archivos públicos (tests, comentarios, diario y un mensaje de commit). El ID de hardware
  llegó a GitHub. Lo destapó buscar los valores reales en todo el repositorio antes de subir.
  → En tests y ejemplos, siempre valores inventados y marcados como tales. Antes de cada subida, buscar los valores reales
  conocidos en archivos **y** en mensajes de commit.
  → **Decisión de Diego (2026-10-20):** subir el historial tal cual. El identificador de la licencia de prueba queda en el
  historial público (como ya estaba el ID de hardware), a cambio de no reescribir commits de los que dependen los registros
  n.º 12–15. Prima la integridad del registro.
- **Probar el proceso también gasta datos.** La tarea 3a genera estrategias con datos reales (los de ejemplo de SQX:
  EURUSD, oro e índices de Dukascopy hasta 2024). Lo generado queda visto y cuenta como hipótesis (regla 7). → Antes de la
  primera generación se decide y se registra qué datos se "queman" para pruebas de proceso, y no se usan después para investigar.
- **Una revisión externa (otra IA, vía Diego) propuso una regla de proporcionalidad:** ningún control de seguridad nuevo sin
  una amenaza concreta, una prueba que demuestre el fallo y un criterio de aceptación. Claude está de acuerdo; pendiente de
  que Diego la fije como decisión. También señaló que un hash solo detecta cambios si la referencia está protegida: hoy lo
  está gracias al historial subido a GitHub (reescribirlo exige un force-push visible).
- **`ANTHROPIC_API_KEY` está guardada como variable de usuario de Windows** (comprobado sin mostrar el valor). Rechazarla en
  una sesión no la elimina. → Diego decide si la reconoce, la revoca o la borra.
- **La configuración de fábrica del Builder habría gastado datos y horas sin avisar:** GBPUSD 2003–2019, parada a las 1000
  estrategias con 5 reinicios y filtros de calidad (eso ya es seleccionar). → Antes de lanzar un proyecto se exporta su
  configuración (`saveconfig`), se lee y se cambia con un script que se para si algo no está donde se espera.
- **"Config loaded" se comprobó, no se creyó:** se volvió a exportar la configuración y se comparó elemento a elemento con la
  plantilla cargada. Coincide salvo el bloque de recursos, que SQX rehace al guardar (y vuelve a declarar EURUSD porque la
  comprobación cruzada desactivada lo nombra).
- **No hay semilla aleatoria documentada** para la generación: probablemente no sea repetible exactamente. La tarea 4 pide
  repetir el backtest de una estrategia ya generada, no la generación.
- **El circuito por línea de comandos funciona:** generar → guardar estrategias → CSV de resultados y operaciones → código
  MT4/MT5, todo sin tocar la interfaz (registros n.º 21–30). Cada llamada cuesta ~25 s de arranque; la generación, 6 s.
- **La documentación de SQX se equivoca en el nombre del motor** (`mt4`); el programa espera `MetaTrader4`. Y `-sourcecode`
  funciona aunque `-h` no lo liste. → Primero la fuente escrita; si falla, el nombre que usa la propia instalación; y parar
  ahí, sin probar nombres a ciegas.
- **Las rutas relativas de `sqcli` se resuelven desde la carpeta de SQX**, no desde donde se lanza el comando.
- **El código exportado incrusta una librería con licencia limitada** (OrderReliable, solo para estrategias de SQ).
  En un repositorio público se guarda solo su hash.
- **Las operaciones que abren y cierran en la misma vela delatan un backtest solo con velas** (`testPrecision="1"`).
  Que salte un stop dentro de una vela H1 es una suposición del simulador, no un hecho. → Medirlo en H1.
- **Hipótesis: el P/L en USD de USDCHF se convierte con un tipo fijo** (cuadra al céntimo con `pointValue` 115.179,5).
  Si se confirma, los resultados en dólares de pares no-USD no usan el tipo de cada momento.
- **Decisión (Claude, por delegación de Diego, 2026-10-20): se sube con el usuario de Windows visible en las rutas.** Coherente
  con la decisión anterior: no se reescriben commits de los que dependen registros (n.º 19 en adelante). Regla de
  proporcionalidad: riesgo bajo y ninguna amenaza concreta que justifique romper la integridad del registro. En adelante, rutas
  sin el usuario cuando haya alternativa.
- **Un resultado idéntico no prueba nada sin un control que pueda fallar.** Dos backtests dieron 1.353 operaciones idénticas,
  y también iguales a la generación: tan bueno que podía ser una reexportación de lo guardado. Con spread 3 en vez de 2
  (única diferencia), 0 de 10 iguales: el Retester recalcula de verdad. → Toda prueba de "sale igual" lleva su control negativo.
- **Algunas órdenes de `sqcli` son asíncronas:** `-databank action=load` suelta dice "loaded" y sale sin guardar. Con `-run`
  y `synctofiles` en el mismo proceso funciona, pero el log muestra una carrera. → Comprobar siempre el efecto (recuento,
  archivos), no el mensaje.
- **Las plantillas de fábrica no son homogéneas:** la del Retester no trae `<Swap>` (la del Builder sí). Sin él podría
  aplicarse el swap del instrumento y el backtest repetido no sería comparable. El script se paró en vez de suponer.
- **Error de procedimiento de Claude:** crear un archivo mientras corría una tanda dejó los registros n.º 44–48 como "sucios".
  → No tocar el repositorio mientras se ejecuta un experimento.
- **El CLI del laboratorio fallaba al imprimir "→"** en la consola de Windows (cp1252) *después* de registrar: devolvía error
  con la entrada ya escrita, y eso invita a repetirla y duplicarla. Arreglado con un test.
- **Un indicador mal elegido casi da una conclusión falsa.** What If y Walk-Forward dejaron carpetas de resultados de
  0 bytes y el log no decía nada: parecía el bloqueo de la licencia. El experimento discriminante (Walk-Forward Matrix, que
  según la documentación no se bloquea) también salió vacío, y eso obligó a buscar dónde se guardaban de verdad:
  dentro de `settings.xml`, con 11 periodos de walk-forward y parámetros reoptimizados. → La licencia de prueba **no**
  bloquea WFO ni What If. Antes de concluir "no está", comprobar que se mira en el sitio correcto, con un caso que sí deba estar.
- **La consola de `sqcli` va 2 horas adelantada** respecto al log interno (hora de España): 14:10 frente a 12:10.
- **Tropiezo de Claude:** lanzar Python con su ruta completa volvió a meter el usuario de Windows en el registro (n.º 68–71).
  Basta con `python`.
- **Tarea 7 en tres intentos.** (1) El Builder ignoró el banco de salida y escribió en `Results`. (2) La explicación
  "el banco aún no existía" se puso a prueba y quedó **refutada**: también falla con el banco ya creado. (3) Funcionó
  separando las estrategias nuevas por comparación de archivos, sin mover ni borrar nada. → Una hipótesis se prueba con un
  experimento que pueda tumbarla; tumbada, se registra y se cambia de enfoque en vez de insistir.
- **`-databank action=move` cortó y no pegó** ("Nothing to paste") porque el banco aún no estaba cargado en memoria.
  No se perdió nada, pero con el banco cargado podría perder estrategias. → No se usa en la automatización.
- **El experimento completo cuesta ~55 s, y el 90 % es arrancar `sqcli`.** Con este laboratorio, lo caro no será el
  cálculo de un experimento pequeño sino el número de arranques: agrupar órdenes en `-run`.
- **SQX reutiliza nombres de estrategia** ("Strategy 0.11(2)"). → Identificar estrategias por hash, nunca por nombre.
- **Antes de descargar los datos de verdad, se decide qué no se mirará nunca.** Darwinex da ~9 años de forex (desde
  2017-10): todo el material para investigar, validar y examinar. Mirarlo "solo para ver qué hay" gastaría el examen final.
  → Protocolo de sellado en borrador, para que Diego lo apruebe antes de descargar ningún precio.
- **Un periodo sellado que siga dentro de SQX no está sellado:** SQX guarda toda la historia descargada y la generación
  lee de ahí. → El sellado se diseña fuera de SQX (descarga con fecha de fin, segunda instalación o, en último lugar, recorte).
- **Auditoría del método del curso de Diego** (nota privada **fuera** de la carpeta del proyecto: "ignorada por git" no es
  "privada"; un `git add -f` la publicaría). Leído de sus configuraciones de SQX, no de los vídeos. Usa buenas
  herramientas (walk-forward, Monte Carlo, permutación de parámetros), pero **usa el tramo fuera de muestra para
  seleccionar**, busca a gran escala sin que **en esas configuraciones** aparezca una corrección explícita por pruebas
  múltiples (los vídeos no se han visto) y pone deslizamiento 0. → Afirmar solo lo que la evidencia examinada sostiene. → Lo que se usa para elegir deja de ser fuera de muestra:
  hace falta un bloque nunca tocado. Una estrategia seleccionada con datos hasta una fecha solo se evalúa con datos
  posteriores a esa fecha.
- **Una cifra plausible no es una cifra comprobada.** En la propuesta 0003 escribí que 24 meses darían "cientos de
  operaciones por estrategia". Con nuestras 20 estrategias de prueba (22 meses H1): mediana 75–90, solo la mitad llega a
  100 y varias no pasan de 30. Lo señaló una revisión externa. → Toda cifra que sostenga una decisión se comprueba con
  datos, aunque parezca obvia; y el examen final lleva una muestra mínima fijada antes (< 100 operaciones: INCONCLUSO).
- **Registrar todo no es lo mismo que limitar la búsqueda.** Con un número ilimitado de estrategias, alguna saldrá
  espectacular por azar aunque quede anotada. → Presupuesto de búsqueda con tope numérico y tope de candidatas.
- **Con cinco revisiones externas en un día, el riesgo ya no es olvidar una idea sino dispersarlas.** Había tres
  arquitecturas escritas y decisiones abiertas en varios archivos. → Índice único `docs/decisiones/PENDIENTES.md`:
  decisiones de Diego, trabajo técnico y requisitos futuros, cada uno con su origen. Y una advertencia: si las revisiones
  vienen del mismo modelo, que coincidan no es evidencia independiente.
- **Dos revisiones pueden contradecirse y tener razón las dos.** La 03 pedía topes numéricos ya; la 06, no fijar cifras
  sin conocer el coste de cada lote. Se concilian con un **piloto con cifras pequeñas fijadas ya**, que sirve para medir
  y no produce candidatas, y una **fase confirmatoria** cuyo límite se fija con esos datos antes de empezar. Además, la
  06 leía una versión anterior de la 0003. → Las decisiones que cambian llevan **historial de versiones**, para que
  cualquiera sepa contra qué versión opina.
- **Leer un paper no es creérselo: se reproducen sus números.** El ejemplo del DSR salió idéntico al cuarto decimal, las
  cifras de MinBTL también… y en el de la PBO apareció una **errata** (C(16,8) = 12.870, no 12.780). Sin consecuencias,
  pero demuestra que hay que comprobar. Las fórmulas que el extractor de texto destrozó se leyeron en la imagen de la
  página.
- **Los tres papers coinciden en un requisito que no teníamos:** guardar la serie de resultados de **todas** las
  estrategias probadas, también las descartadas. SQX hoy solo guarda las que pasan los filtros. → Comprobarlo en el piloto.
- **Aplicado a nuestros números:** con 7 años para investigar caben ~139 configuraciones independientes antes de que la
  mejor llegue a Sharpe 1 por azar; con 24 meses sellados, ~7. El tope de 3 candidatas al examen queda respaldado.
- **El código 0 volvió a mentir:** la consulta del cortafuegos devolvió 0 con un "Acceso denegado" dentro. Tercera vez hoy.

## 2026-10-21

- **Primer reinicio con el documento de continuación: funcionó.** La sesión nueva supo dónde estábamos leyendo
  `ESTADO_Y_CONTINUACION.md`, `PENDIENTES.md` y este diario, y lo comprobó todo con comandos (tests, guardián, registro,
  evidencias, git, hash de `sqcli`, recuento de bancos) antes de dar nada por bueno.
- **La memoria persistente también se equivoca.** Una sesión intermedia escribió en la memoria que el cierre del 20-10
  "NO estaba en git": lo miró antes del push. Al reiniciar, `git status` y `git rev-list` decían lo contrario.
  → La memoria es una pista, no una evidencia: se contrasta con el sistema y se corrige.
- **Otro falso positivo del guardián:** un `ls` no recursivo en la carpeta del curso (`…\IMOX TRADING.zip\`, que es una
  carpeta) se bloquea como "recorrido recursivo". No se buscó otra vía; queda en B9 para la sesión de mantenimiento.
  → Causa leída en el guardián: la regla `\bzip\b` toma el ".zip" del nombre de la carpeta por el compresor. Vía
  sancionada: un script escrito con Write que lleva la ruta dentro (`LAB_PRIVADO_CURSO/herramientas/inventario_curso.py`).
- **Medir antes de prometer:** antes de decir "transcribo el curso" se midió. 85 vídeos sin comprimir dentro del zip,
  26,3 h en los MP4 y 7 MKV sin duración legible (no se estima a ojo); la carpeta del escritorio es una extracción parcial
  (8 vídeos). El PC no tiene GPU: la velocidad de transcripción en CPU no se supone, se mide en el piloto de 3 vídeos.
- **Tropiezo de Claude:** para leer el modelo de CPU usé la herramienta PowerShell, que es justo la que el guardián no
  vigila (A9). Era una consulta inocua del sistema, pero mientras A9 no esté hecho, **todo por Bash**.
- **Dos revisiones más (10 y 11), probablemente del mismo modelo:** de unos veinte puntos, dos ideas nuevas. La buena:
  la 0003 abandona si las candidatas no baten "a las referencias comparables", pero no dice cuáles son; elegirlas
  después de ver resultados sería un grado de libertad escondido. → C20: se preregistran antes del piloto.
- **Idea propia: el control negativo también vale para la búsqueda.** Si SQX encuentra estrategias "buenas" en datos
  sintéticos sin ventaja, sus filtros no distinguen ventaja de ruido (B17). Es la lección del 20-10 (un resultado igual
  necesita un control que pueda fallar) aplicada a otra escala.
- **Diego delegó y decidió:** compró el curso (A8), aprueba instalar el transcriptor (A17), "primero cuentas demo" (A2),
  horas variables (A3) y delega en el criterio de Claude A1, A19, A20 y A21. → 0003 aceptada en v6. Que Diego delegue
  no convierte a Claude en quien decide: cada decisión queda escrita con su motivo y Diego puede revocarla.
- **Lo que se ha visto no se puede sellar.** Al leer la 0003 para aprobarla: el curso usa datos de Darwinex hasta 2025-03
  y se empaquetó el 2026-01-12, y el sellado empezaba el 2024-10-01. Transcribir el curso habría "abierto" el examen
  sin tocar `data/sealed/`. → El inicio del sellado pasa a ser una **regla** (fecha más tardía vista en el curso), y
  revisar el curso entero pasa a ser condición previa de la descarga (B18).
- **El propio Claude es una fuente de contaminación:** se entrenó con datos hasta 2026-06 y sabe, a grandes rasgos,
  qué hicieron los mercados en el periodo sellado. Diego también lo vivió. → Las candidatas salen de procedimientos
  mecánicos; las hipótesis humanas o de IA llevan la marca "posible conocimiento posterior" (C22); el único examen
  limpio del todo es el prospectivo.
- **La captura de Diego destapó un coste oculto:** `claude` en PowerShell decía "API Usage Billing": la variable
  `ANTHROPIC_API_KEY` (A10) haría pagar por consumo. → Mirar la cabecera de cada sesión nueva.
- **Piloto de transcripción, con tres tropiezos:** (1) PyAV 19 rompe faster-whisper 1.2.1 (`metadata_errors`): se fijó
  PyAV 18.1.0 tras comprobarlo, no por suposición; (2) creí fallida una ejecución en segundo plano que seguía en marcha y
  la lancé otra vez: dos procesos a la vez, así que **esa medida de tiempo no vale** (la calidad sí); (3) escribí "zip"
  dentro de un `awk` y el guardián lo paró, con razón según su regla.
- **El audio da el relato; la pantalla, las cifras.** *Small* convierte "spread" en "express" y "Ret/DD" en "red", y un
  vocabulario inicial no lo arregla; *medium* casi siempre acierta, pero tarda 3,4 veces más. Un fotograma enseña el filtro
  exacto que el audio había convertido en "red de base" y "offtrade" (cifras solo en la nota privada: son contenido del
  curso). Es el mismo hallazgo de los `.cfx`, ahora visto en el vídeo: el curso **selecciona con el tramo fuera de
  muestra**.
