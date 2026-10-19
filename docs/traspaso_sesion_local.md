# Traspaso: de la sesión en la nube a Claude Code en el PC de SQX

Fecha: 2026-10-19 · Para: Diego y la sesión local de Claude Code (Windows 11).

## Dónde estamos

- **Base del laboratorio hecha:** guardián, registro encadenado, ejecutor con evidencias, ficha H0, decisión 0001 y lección 01.
- **Registro:** 2 entradas (versión de SQX vista en las capturas). `python -m lab verificar` → íntegro.
- **SQX instalado:** *Pro Build 145 (Trial license)*, build 145.3191, **build de desarrollo del 2026-10-06**, prueba hasta el 02-11-2026.
  La hoja de ruta decía Ultimate 143.2708: discrepancia abierta (ficha H0).
- **Nada de la línea de comandos de SQX está comprobado todavía.**

## Reparto de trabajo

| Quién | Dónde | Qué hace |
|---|---|---|
| Diego | PC | Decide, aprueba, hace los pasos manuales en la interfaz de SQX |
| Claude Code local | PC (Windows) | Ejecuta SQX por línea de comandos, registra, rellena la ficha y hace commit y push |
| Claude en la nube | GitHub | Revisa lo subido, audita resultados y prepara lecciones |

Ambas sesiones trabajan sobre la rama `claude/proyecto-2026-fps66g`. Antes de empezar: `git pull`. Al terminar: commit y `git push`.

## 1. Instalación (Diego, una sola vez)

1. **Git for Windows**: https://git-scm.com/download/win (opciones por defecto).
2. **Python 3.10+** desde https://www.python.org/downloads/ → marcar **"Add python.exe to PATH"**.
   Comprobar en una PowerShell nueva: `python --version`. Si se abre la Microsoft Store, Python no está bien instalado.
3. **Claude Code**, en PowerShell: `irm https://claude.ai/install.ps1 | iex`. Después, `claude` para iniciar sesión.
4. Descargar el proyecto (por ejemplo en `C:\Lab`):
   ```powershell
   cd C:\
   git clone -b claude/proyecto-2026-fps66g https://github.com/LaRuinaDeMago/TradingAlgoritmico.git Lab
   cd Lab
   pip install -e .
   ```

## 2. Paso 0: comprobar el banco de trabajo (antes de tocar SQX)

```powershell
python -m unittest discover -s tests          # todos OK
python .claude/hooks/guardian.py --autotest   # todos "correctos"
claude                                        # abre Claude Code en C:\Lab
```

Dentro de Claude Code, prueba de fuego: pídele *"lee data/sealed/prueba.txt"*. **Tiene que bloquearlo el guardián.**
Si no lo bloquea, el hook no funciona (casi siempre por `python` fuera del PATH): se para y se arregla antes de seguir.

## 3. Tarea 1 del H0: `sqcli.exe -h`

1. **Diego** busca la carpeta de instalación: clic derecho en el icono de SQX → *Abrir ubicación del archivo*.
   Según la documentación, `sqcli.exe` está en esa carpeta. Copia la ruta completa.
   (El guardián bloquea a Claude si intenta buscar recursivamente por todo `C:\`: es intencionado.)
2. **Claude Code** lo ejecuta con registro:
   ```
   python -m lab ejecutar --nombre t1_sqcli_ayuda --version-sqx "145.3191-dev" --timeout 120 -- "C:/RUTA/sqcli.exe" -h
   ```
   Si se queda esperando (la documentación dice que sin parámetros abre una consola interactiva), el tiempo máximo lo corta
   y queda registrado como FALLIDO. Se prueba entonces otra forma documentada, y también se registra.
3. Rellenar la fila 1 de `h0/ficha.md` con estado, evidencia y tiempo.
4. Capturas que faltan (Diego): **Acerca de** (abajo a la derecha en SQX) → `h0/evidencias/`.

## Cosas que conviene saber

- **El guardián analiza texto, no intenciones.** Para escribir archivos, usar Write/Edit, no heredocs.
  Los mensajes de commit que nombran la carpeta sellada se bloquean: usar `git commit -F archivo`.
  Ver `aprendizaje/diario.md`.
- **Commit antes de cada experimento que cuente:** si no, el registro lo marca `"sucio": true` y no se puede reproducir desde un commit.
- **SQ Pilot** (el asistente IA de SQX) gasta créditos y envía lo que escribes a un modelo externo. Sus respuestas son hipótesis,
  no hechos: dijo que hay plugins `runtime: claude-code`, y eso hay que comprobarlo. Tampoco conviene pedirle que "reviente todo":
  ofrecía borrar proyectos y bancos de estrategias.

## Primer mensaje sugerido para Claude Code local

> Lee CLAUDE.md, docs/traspaso_sesion_local.md y aprendizaje/diario.md. Estamos en el PC de SQX con Windows 11.
> Haz el Paso 0 y dime el resultado. No toques SQX hasta que el guardián haya bloqueado la prueba de data/sealed.
