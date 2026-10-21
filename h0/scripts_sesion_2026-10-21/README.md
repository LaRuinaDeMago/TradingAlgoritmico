# Guiones y resultados auxiliares de la sesión del 2026-10-21

Rescatados de la carpeta temporal de la sesión, que se borra al cerrar. Los scripts de las tandas (B1, B17) están en
`h0/configs/`; aquí solo lo que no tenía otro sitio.

| Archivo | Qué es |
|---|---|
| `prueba_lanzador.cmd` | Prueba de `claude_lab.cmd` con una clave falsa (A10); espera una copia del lanzador junto a él |
| `claude_lab_control.cmd`, `prueba_control.cmd` | **Control negativo** de esa prueba: el lanzador sin la línea que borra la clave debe negarse a abrir |
| `prueba_real.cmd` | La misma prueba sobre `claude_lab.cmd` en su sitio (raíz del repositorio) |
| `ultimas_entradas.py` | Imprime las últimas 5 entradas del registro sin hashes (`python -I … registry/experimentos.jsonl`); útil porque el guardián bloquea atajos en línea con `>=` en comandos que nombran `registry` |
| `barrido_privacidad.py` | Barrido antes de subir (desde la raíz: `python -I h0/scripts_sesion_2026-10-21/barrido_privacidad.py`): identificadores sin redactar, correo, cifras del curso, vídeos y tipos de archivo prohibidos en lo que va a salir a GitHub |
| `resultado_a9.json`, `resultado_b3.json`, `resultado_b11.json` | Archivos `--resultado` de los registros n.º 90, 91 y 92 (su contenido ya está dentro del registro) |
