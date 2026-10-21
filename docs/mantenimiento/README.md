# Mantenimiento del guardián (asunto A9 de `docs/decisiones/PENDIENTES.md`)

**Aplicado el 2026-10-21** (commit 7527489, registros n.º 90 y 91): el guardián activo es idéntico a
`guardian_borrador_powershell.py` y vigila PowerShell. Lo de abajo queda como procedimiento para la **próxima** sesión de
mantenimiento (B15 y B9), cambiando el texto de la petición por el del nuevo borrador.

`guardian_borrador_powershell.py` es el guardián de entonces más la vigilancia de la herramienta PowerShell.
Autotest: 44/44 (los 28 de antes + 16 de PowerShell).

Para aplicarlo, Diego abre una sesión de mantenimiento en una ventana de PowerShell, desde la carpeta del proyecto:

```
Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue; $env:LAB_MANTENIMIENTO_GUARDIAN = "1"; claude
```

La primera parte quita la clave API solo en esa ventana (A10: la clave es de Diego y se queda, pero el laboratorio no
la usa). Comprobar que la cabecera **no** dice "API Usage Billing" (o `/status`) antes de escribir nada. Después pide:

> Modo mantenimiento autorizado por Diego, solo para esto: copia `docs/mantenimiento/guardian_borrador_powershell.py`
> sobre `.claude/hooks/guardian.py` y añade `PowerShell` al matcher de `.claude/settings.json`. Ejecuta el autotest,
> enséñame el diff, anótalo en el diario y haz commit. No toques nada más.

Después, en una sesión normal, Claude lo comprueba con una llamada **real** de PowerShell sobre un archivo inexistente
de la carpeta sellada (asunto B3).
