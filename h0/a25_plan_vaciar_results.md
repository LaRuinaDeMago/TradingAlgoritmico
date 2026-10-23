# A25: vaciar `Builder/Results` antes de la fase 1 (plan con criterios previos)

**Decisión:** A25, delegada por Diego el 2026-10-23 ("haremos lo que tú consideres que es lo mejor y lo que más va a
servir para nuestros objetivos"), con la recomendación de Claude en `docs/decisiones/PENDIENTES.md` (A25): quitar el
riesgo de desalojo (capacidad de fábrica 1.000), ahorrar 31–54 s de guardado en cada orden que toca bancos y dejar que
cada brazo de la fase 1 empiece con un banco vacío. **No se pierde nada:** el banco sale entero a una copia verificada.
**Límite de tiempo:** 45 min. Todas las órdenes ya se usaron en B21 (ensayadas: `retirar` n.º 276, `contenido`
n.º 278, `count` sola n.º 267), así que no hay supuestos nuevos.

## Estado de partida (medido el 2026-10-23 a las 11:3x UTC, SQX cerrado)

- `Builder/Results`: **7.053** `.sqx`; los demás bancos del Builder, 0.
- `lab_h0\b21\archivo_Results` (copia de B21): **7.003**, todos con nombre presente en `Results`; 50 de más en
  `Results` (prueba de no desalojo de B21, n.º 258).
- `lab_h0\b21\M3_Results.json`: 7.053 nombres, **los mismos** que hay en `Results`.
- Destino `lab_h0\b21\Results_retirado_A25`: no existe. Disco libre: 307 GB.

## Pasos y criterios (todos por el ejecutor con registro)

1. **Retirar:** `python -I h0/configs/b21_archivo.py retirar <Results> <lab_h0>/b21/Results_retirado_A25`.
   Criterio R: la salida dice "retiradas 7053", "copia idéntica" y "quedan en el origen 0" (la herramienta se para sin
   borrar nada si la copia no es idéntica byte a byte o si el origen cambia mientras se copia).
2. **Contenido frente al archivo de B21:** `b21_archivo.py contenido <archivo_Results> <Results_retirado_A25>`.
   Criterio C: las 7.003 del archivo están en la copia con el mismo **contenido** (reglas, operaciones, curva,
   configuración; no el zip, que SQX reescribe en cada arranque).
3. **Nombres frente a M3:** los 7.053 nombres de la copia son exactamente los de `M3_Results.json`. Criterio N.
4. **SQX ve el banco vacío:** `sqcli.exe -databank action=count project=Builder name=Results`, en una orden sola.
   Criterio S: la evidencia contiene "Records: 0" y no contiene "failed" ni "Memory usage"; después, la carpeta sigue
   con 0 `.sqx` y los demás bancos del Builder siguen con 0.
   Control: el mismo recuento sobre un banco con 7.003 dio "Records: 7003" (n.º 267).

**Veredicto:** SÍ si se cumplen R, C, N y S. Si falla R, no se ha borrado nada (la herramienta se para) y se
diagnostica aparte. Si falla C, N o S después de R, la copia es idéntica byte a byte al banco de antes, así que se
repone con `b21_archivo.py reponer` y se diagnostica antes de volver a intentarlo.

**Después:** `Results_retirado_A25` entra en la copia de A14 (vive en `lab_h0`); `docs/ESTADO_Y_CONTINUACION.md` §3 y
`PENDIENTES.md` (A25) se ponen al día.
