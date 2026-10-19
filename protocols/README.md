# Protocolos

Un protocolo se escribe **antes** de cualquier examen y no se cambia después de ver resultados.
Si hace falta cambiarlo, se crea uno nuevo que cite al anterior y explique por qué.

## Acceso a `data/sealed/`

1. Se copia `plantilla_acceso_sellado.md` a `protocols/AAAA-MM-DD_<nombre>.md` y se rellena entera.
2. Se hace commit del protocolo **antes** de abrir nada (el hash del commit fecha la decisión).
3. Diego lo aprueba poniendo `Estado: APROBADO` y `Aprobado por: Diego` y arranca Claude Code con:

   ```
   # PowerShell
   $env:LAB_PROTOCOLO_SELLADO = "protocols/AAAA-MM-DD_<nombre>.md"; claude
   ```

   Sin esa variable, el guardián (`.claude/hooks/guardian.py`) bloquea cualquier acceso.
   Con ella, permite el acceso y anota cada uso en `registry/accesos.log` con el hash del protocolo.
4. Al terminar, se cierra la sesión. Ese conjunto sellado deja de ser prueba final para la siguiente iteración.

## Protección fuerte (recomendada)

El guardián es una red de seguridad heurística: impide los accidentes, no garantiza nada frente a un comando rebuscado.
La garantía real es que los datos sellados no se puedan leer sin Diego:

- Guardar el conjunto sellado como archivo cifrado (por ejemplo 7-Zip con AES-256 y contraseña que solo conoce Diego) y anotar su SHA-256 en el registro al crearlo.
- Descifrarlo solo dentro de una sesión con protocolo aprobado, y borrar la copia descifrada al acabar.
