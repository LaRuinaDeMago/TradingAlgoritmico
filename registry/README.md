# Registro

Solo se añade; nunca se edita ni se borra. El guardián bloquea editar o sobrescribir lo que ya hay aquí.

| Archivo | Contenido | Quién escribe |
|---|---|---|
| `experimentos.jsonl` | Un experimento por línea, también los fallidos | `python -m lab ejecutar` / `python -m lab registrar` |
| `accesos.log` | Cada acceso permitido a `data/sealed/` | el guardián, automáticamente |

## Campos de cada experimento

`n`, `fecha_utc`, `descripcion`, `comando` (exacto), `version_sqx`, `datos` (ruta → SHA-256),
`codigo` (commit y si había cambios sin confirmar), `semilla`, `costes`, `estado` (OK / FALLIDO / INCONCLUSO),
`resultado`, `notas`, `entorno`, `hash_anterior`, `hash`.

Cada entrada incluye el hash de la anterior: si alguien edita o borra una línea intermedia,
`python -m lab verificar` lo detecta. Borrar la **última** línea no lo detecta la cadena;
por eso el registro se confirma en git después de cada sesión de trabajo.

Un experimento con `"sucio": true` en `codigo` se hizo con cambios sin confirmar: no se puede
reproducir solo desde el commit. Antes de un experimento que cuente, hacer commit.
