# Mantenimiento del guardián (asunto A9 de `docs/decisiones/PENDIENTES.md`)

`guardian_borrador_powershell.py` es el guardián actual más la vigilancia de la herramienta PowerShell (hoy sin
control). Autotest: 44/44 (los 28 de antes + 16 de PowerShell). **No está activo**: el guardián en uso sigue siendo
`.claude/hooks/guardian.py`, que Claude no puede modificar.

Para aplicarlo, Diego abre una sesión de mantenimiento en una ventana de PowerShell, desde la carpeta del proyecto:

```
$env:LAB_MANTENIMIENTO_GUARDIAN = "1"; claude
```

(en la pregunta de la clave API, elegir "2. No") y pide:

> Modo mantenimiento autorizado por Diego, solo para esto: copia `docs/mantenimiento/guardian_borrador_powershell.py`
> sobre `.claude/hooks/guardian.py` y añade `PowerShell` al matcher de `.claude/settings.json`. Ejecuta el autotest,
> enséñame el diff, anótalo en el diario y haz commit. No toques nada más.

Después, en una sesión normal, Claude lo comprueba con una llamada **real** de PowerShell sobre un archivo inexistente
de la carpeta sellada (asunto B3).
