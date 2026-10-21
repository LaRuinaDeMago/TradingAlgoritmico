"""¿Marca `ejecutar` como sucio un repositorio limpio? Se prueba en un repo temporal desechable."""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])  # carpeta src del laboratorio
from lab.ejecutar import ejecutar

with tempfile.TemporaryDirectory() as d:
    raiz = Path(d)
    (raiz / "a.txt").write_text("x")
    git = ["git", "-c", "user.name=prueba", "-c", "user.email=prueba@example.invalid"]
    subprocess.run(["git", "init", "-q"], cwd=raiz, check=True)
    subprocess.run(git + ["add", "."], cwd=raiz, check=True)
    subprocess.run(git + ["commit", "-qm", "inicial"], cwd=raiz, check=True)
    antes = subprocess.run(["git", "status", "--porcelain"], cwd=raiz, capture_output=True, text=True).stdout
    print("repo limpio antes de ejecutar:", antes.strip() == "")
    e = ejecutar([sys.executable, "-c", "print(1)"], nombre="prueba", version_sqx="N/A", raiz=raiz)
    print("codigo registrado:", e["codigo"])
