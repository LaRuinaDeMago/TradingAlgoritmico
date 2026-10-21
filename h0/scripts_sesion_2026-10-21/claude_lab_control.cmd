@echo off
rem Abre Claude Code para el laboratorio SIN la clave ANTHROPIC_API_KEY (asunto A10, decision de Diego 2026-10-21:
rem la clave es suya y se queda en Windows, pero el laboratorio no la usa). Asi la sesion va con la suscripcion.
rem Solo afecta a esta ventana: no toca la variable de Windows ni la configuracion de Claude Code.
rem Uso: doble clic, o desde una consola:  claude_lab.cmd [argumentos de claude]
rem No activa el modo mantenimiento del guardian: eso lo hace Diego a mano (docs\mantenimiento\README.md).
setlocal
cd /d "%~dp0"
set "LAB_MANTENIMIENTO_GUARDIAN="
if defined ANTHROPIC_API_KEY (
  echo ERROR: no se pudo quitar ANTHROPIC_API_KEY. No se abre Claude.
  exit /b 1
)
echo Laboratorio: ANTHROPIC_API_KEY quitada en esta ventana; se usa la suscripcion. Comprueba la cabecera con /status.
claude %*
