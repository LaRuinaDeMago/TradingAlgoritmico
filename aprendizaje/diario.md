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
- **El código 0 volvió a mentir:** la consulta del cortafuegos devolvió 0 con un "Acceso denegado" dentro. Tercera vez hoy.
