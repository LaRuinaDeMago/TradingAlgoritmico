"""Comprueba que cada evidencia citada en el registro está en git (en la revisión dada) con el hash registrado.
Las privadas se comprueban en disco y deben NO estar en git."""
import json
import hashlib
import subprocess
import sys
from pathlib import Path

rev = sys.argv[1] if len(sys.argv) > 1 else "HEAD"


def blob(ruta):
    r = subprocess.run(["git", "cat-file", "-p", f"{rev}:{ruta}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


fallos = 0
for linea in open("registry/experimentos.jsonl", encoding="utf-8"):
    e = json.loads(linea)
    r = e["resultado"]
    if not isinstance(r, dict) or "evidencia" not in r:
        continue
    contenido = blob(r["evidencia"])
    if contenido is None:
        estado = "NO ESTÁ EN GIT (ver entradas posteriores)"
    else:
        estado = "coincide" if hashlib.sha256(contenido).hexdigest() == r["sha256_evidencia"] else "NO COINCIDE"
        fallos += estado != "coincide"
    print(e["n"], estado, r["evidencia"])
    if r.get("evidencia_privada"):
        p = Path(r["evidencia_privada"])
        ok = p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == r["sha256_evidencia_privada"]
        en_git = blob(r["evidencia_privada"]) is not None
        fallos += (not ok) or en_git
        print("   privada:", "coincide en disco" if ok else "NO COINCIDE", "| en git:", "SÍ (MAL)" if en_git else "no")
print("fallos:", fallos)
