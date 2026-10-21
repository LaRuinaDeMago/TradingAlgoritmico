"""Barrido antes de subir: busca datos privados y contenido del curso en lo que va a salir a GitHub (commits sin subir +
cambios sin confirmar + archivos nuevos). Uso (desde la raíz del repo): python -I barrido_privacidad.py"""
import re
import subprocess

RAMA = "origin/claude/proyecto-2026-fps66g"
PATRONES = {
    "hardware sin redactar": re.compile(r"Hardware ID: (?!\[REDACTADO)"),
    "licencia sin redactar": re.compile(r"Licenser -- L: (?!\[REDACTADO)|license [0-9A-F]{6}"),
    "correo": re.compile(r"[\w.]+@gmail\.com"),
    "cifras de filtros del curso": re.compile(r"Ret/DD ≥ ?10|Ret/DD de base|SQN >|academia\.imox", re.I),
    "vídeo del curso": re.compile(r"\.(mp4|mkv)\b", re.I),
}


def sh(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


nuevos = [l[3:] for l in sh("git", "status", "--porcelain").splitlines() if l.startswith("??")]
texto = sh("git", "diff", RAMA) + sh("git", "diff")
for ruta in nuevos:
    for f in (sh("git", "ls-files", "--others", "--exclude-standard", ruta).split() or [ruta]):
        try:
            texto += "\n" + open(f, encoding="utf-8", errors="replace").read()
        except (IsADirectoryError, FileNotFoundError):
            pass
lineas = [l for l in texto.splitlines() if not l.startswith("-")]
hallazgos = {n: [l[:140] for l in lineas if p.search(l)] for n, p in PATRONES.items()}
for n, ls in hallazgos.items():
    print(f"{n}: {len(ls)}", *ls[:3], sep="\n   ")
tipos = [f for f in sh("git", "ls-files").split() + [x for r in nuevos for x in sh("git", "ls-files", "--others",
         "--exclude-standard", r).split()] if re.search(r"\.(pdf|mq4|mq5|ex4|ex5|mp4|mkv|zip)$", f, re.I)
         and not f.startswith("docs/hoja_de_ruta")]
print("archivos de tipo prohibido:", tipos or "ninguno")
print("archivos nuevos:", nuevos)
