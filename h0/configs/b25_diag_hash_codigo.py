"""B25, diagnóstico (sin criterio): ¿por qué no coincide el hash registrado de un archivo de código con el del clon?
Compara el hash registrado con: el archivo del clon, la versión del commit tal como la guarda git (LF) y esa misma
versión con saltos CRLF (lo que deja `core.autocrlf=true` en Windows al sacar el archivo).
Uso: python -I h0/configs/b25_diag_hash_codigo.py CLON COMMIT RUTA HASH_REGISTRADO"""
import hashlib
import subprocess
import sys
from pathlib import Path

clon, commit, ruta, registrado = sys.argv[1:5]
blob = subprocess.run(["git", "-C", clon, "show", f"{commit}:{ruta}"], capture_output=True, check=True).stdout
h = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
en_clon = (Path(clon) / ruta).read_bytes()
crlf = blob.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
autocrlf = subprocess.run(["git", "-C", clon, "config", "core.autocrlf"], capture_output=True, text=True).stdout.strip()
print(f"registrado:                {registrado}")
print(f"archivo del clon:          {h(en_clon)} ({en_clon.count(b'\r\n')} CRLF, {len(en_clon)} bytes)")
print(f"commit tal cual (git, LF): {h(blob)} ({blob.count(b'\r\n')} CRLF, {len(blob)} bytes)")
print(f"commit con CRLF:           {h(crlf)} ({len(crlf)} bytes)")
print(f"core.autocrlf en el clon: {autocrlf or '(sin valor local; manda la configuración global)'}")
print("coincide el registrado con: " + ", ".join(n for n, v in [("clon", h(en_clon)), ("LF", h(blob)), ("CRLF", h(crlf))]
                                              if v == registrado) or "ninguno")
