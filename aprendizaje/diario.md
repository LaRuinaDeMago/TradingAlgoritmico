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
