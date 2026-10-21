#!/usr/bin/env python3
"""Guardián del laboratorio: hook PreToolUse de Claude Code.

Bloquea (exit 2) antes de que se ejecute la herramienta:
  1. Cualquier acceso a data/sealed/ (leer, listar, buscar, copiar, hashear...).
     Solo se permite si Diego arrancó la sesión con la variable de entorno
     LAB_PROTOCOLO_SELLADO apuntando a un protocolo aprobado en protocols/.
     Cada acceso permitido se anota en registry/accesos.log.
  2. Recorridos recursivos (find, grep -r, rg, tree, ls -R, cp -r...) que
     podrían entrar en data/sealed/ sin excluirla.
  3. Editar, sobrescribir o borrar lo ya escrito en registry/ (solo se añade).
  4. Modificar este guardián o .claude/settings*.json, salvo que Diego arranque
     la sesión con LAB_MANTENIMIENTO_GUARDIAN=1.

Los comandos de Bash y de PowerShell se analizan con las mismas reglas.

Es una red de seguridad heurística, no una garantía absoluta: la protección
fuerte es guardar los datos sellados cifrados (ver protocols/README.md).
Autocomprobación: python .claude/hooks/guardian.py --autotest
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

CAMPOS_RUTA = ("file_path", "path", "notebook_path", "pattern", "glob")
HERRAMIENTAS_RUTA_PATRON = {"Glob"}  # en Grep, "pattern" es el texto buscado, no una ruta
CONSOLAS = {"Bash", "PowerShell"}  # herramientas cuyo "command" se analiza como texto

SELLADA = re.compile(r"data/+(sealed|s[^/\s\"']*[*?\[{])")
# Formas reconocidas de excluir la carpeta sellada en un recorrido recursivo.
EXCLUSIONES = [
    re.compile(r"--exclude-dir[= ]['\"]?(\*\*/)?(data|sealed)/?['\"]?"),
    re.compile(r"(-not|!)\s+-path\s+['\"]?[^'\"\s]*sealed[^'\"\s]*['\"]?"),
    re.compile(r"-path\s+['\"]?[^'\"\s]*sealed[^'\"\s]*['\"]?\s+-prune"),
    re.compile(r"(--glob|-g)[= ]['\"]?![^'\"\s]*sealed[^'\"\s]*['\"]?"),
]
RECURSIVO = re.compile(
    r"\b(find|tree|du|rg|ag|tar|7z|robocopy|xcopy|rsync)\b"
    r"|\bzip\b(?!\s*\()"  # zip( es la función de Python, no el compresor
    r"|\bls\s+(-\w*R\w*\b|--recursive)"
    r"|\b(e|f)?grep\b[^|;&]*\s-(\w*[rR]\w*\b|-recursive)"
    r"|\bcp\s+(-\w*[rR]\w*\b|--recursive)"
    r"|\b(get-childitem|gci|dir|ls|copy-item|cpi)\b[^|;&]*(-r(ecurse)?\b|/s\b)"
    r"|\b(compress-archive|expand-archive)\b"
    r"|\bos\.walk\b|\brglob\b|\bglob\.glob\b|\bshutil\.(copytree|make_archive)\b"
)
DESTINO_SEGURO = re.compile(r"(^|[\s'\"=])(\./)?(src|tests|h0|registry|protocols|docs|\.claude)(/|\b)")
MENCIONA_DATA = re.compile(r"(^|[\s'\"=(,])(\./)?data\b")
ESCRITURA_BASH = re.compile(
    r"\b(rm|del|erase|mv|move|ren|rename|truncate|shred|remove-item|set-content|clear-content|out-file)\b"
    r"|\b(new-item|ni|ri|rni|mi|cpi|sc|rmdir|rd)\b"  # PowerShell y sus alias
    r"|::(copy|move|delete|replace|write\w*)\b"  # [IO.File]::WriteAllText(...) y similares
    r"|\bsed\s+(-\w*i|--in-place)|\bgit\s+(rm|mv|checkout|restore|clean)\b"
    r"|(^|[^>])>(?!>)|\bcp\b|\bcopy\b|\btee\b(?!\s+-a)"
)


def normalizar(texto: str) -> str:
    return texto.replace("\\", "/").lower()


def relativa(ruta: str) -> str:
    """Ruta normalizada y relativa a la raíz del proyecto si está dentro."""
    r = normalizar(ruta)
    raiz = normalizar(str(RAIZ)).rstrip("/") + "/"
    if r.startswith(raiz):
        r = r[len(raiz):]
    while r.startswith("./"):
        r = r[2:]
    return r


def motivo_sellado(herramienta: str, entrada: dict) -> str | None:
    if herramienta in CONSOLAS:
        cmd = normalizar(entrada.get("command", ""))
        excluida = False
        for patron in EXCLUSIONES:
            cmd, n = patron.subn(" ", cmd)
            excluida = excluida or n > 0
        if "sealed" in cmd:
            return "el comando menciona la carpeta sellada"
        if RECURSIVO.search(cmd) and not excluida:
            if MENCIONA_DATA.search(cmd):
                return "recorrido recursivo sobre data/ sin excluir sealed"
            if not DESTINO_SEGURO.search(cmd):
                return ("recorrido recursivo sin carpeta concreta (podría entrar en data/sealed/); "
                        "indica la carpeta (src, tests, h0...) o añade --exclude-dir=sealed")
        return None

    for campo in CAMPOS_RUTA:
        valor = entrada.get(campo)
        if not isinstance(valor, str):
            continue
        if campo == "pattern" and herramienta not in HERRAMIENTAS_RUTA_PATRON:
            continue
        r = relativa(valor)
        if SELLADA.search(r) or r.startswith("sealed") or "/sealed" in r:
            return f"{campo} apunta a la carpeta sellada"
    # Glob/Grep sobre data/ con comodines podrían listar la carpeta sellada.
    if herramienta in ("Glob", "Grep"):
        base = relativa(entrada.get("path") or "")
        patron = relativa(entrada.get("pattern" if herramienta == "Glob" else "glob") or "")
        combinado = f"{base}/{patron}" if base else patron
        if re.match(r"(data/*)?\*\*", combinado.lstrip("/")) and base in ("data", "data/"):
            return "búsqueda recursiva sobre data/ sin excluir sealed"
        if re.match(r"data/+\*", combinado):
            return "búsqueda con comodín sobre data/ (incluiría sealed)"
    return None


def motivo_registro(herramienta: str, entrada: dict) -> str | None:
    if herramienta in ("Edit", "MultiEdit", "NotebookEdit"):
        if relativa(entrada.get("file_path") or entrada.get("notebook_path") or "").startswith("registry/"):
            return "registry/ solo admite añadir; no se edita lo ya escrito"
    if herramienta == "Write":
        r = relativa(entrada.get("file_path", ""))
        if r.startswith("registry/") and (RAIZ / r).exists():
            return "registry/ solo admite añadir; no se sobrescribe un archivo existente"
    if herramienta in CONSOLAS:
        cmd = normalizar(entrada.get("command", ""))
        if "registry" in cmd and ESCRITURA_BASH.search(cmd):
            return "comando que podría borrar o sobrescribir registry/ (usa >> o python -m lab)"
    return None


def motivo_guardian(herramienta: str, entrada: dict) -> str | None:
    if os.environ.get("LAB_MANTENIMIENTO_GUARDIAN") == "1":
        return None
    protegidas = (".claude/hooks/", ".claude/settings.json", ".claude/settings.local.json")
    if herramienta in ("Edit", "MultiEdit", "Write", "NotebookEdit"):
        r = relativa(entrada.get("file_path") or entrada.get("notebook_path") or "")
        if any(r.startswith(p) for p in protegidas):
            return "el guardián y la configuración de hooks solo los cambia Diego (LAB_MANTENIMIENTO_GUARDIAN=1)"
    if herramienta in CONSOLAS:
        cmd = normalizar(entrada.get("command", ""))
        if (".claude/hooks" in cmd or ".claude/settings" in cmd) and ESCRITURA_BASH.search(cmd):
            return "comando que podría alterar el guardián o la configuración de hooks"
    return None


def protocolo_aprobado() -> Path | None:
    valor = os.environ.get("LAB_PROTOCOLO_SELLADO")
    if not valor:
        return None
    ruta = Path(valor)
    if not ruta.is_absolute():
        ruta = RAIZ / ruta
    try:
        texto = ruta.read_text(encoding="utf-8")
    except OSError:
        return None
    dentro = normalizar(str(ruta.resolve())).startswith(normalizar(str((RAIZ / "protocols").resolve())))
    aprobado = re.search(r"^estado:\s*aprobado\s*$", texto, re.I | re.M) and re.search(
        r"^aprobado por:\s*diego\b", texto, re.I | re.M
    )
    return ruta if dentro and aprobado else None


def anotar_acceso(herramienta: str, entrada: dict, protocolo: Path) -> None:
    linea = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "herramienta": herramienta,
        "entrada": entrada,
        "protocolo": relativa(str(protocolo)),
        "sha256_protocolo": hashlib.sha256(protocolo.read_bytes()).hexdigest(),
    }
    log = RAIZ / "registry" / "accesos.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


def decidir(herramienta: str, entrada: dict) -> str | None:
    """Devuelve el motivo del bloqueo, o None si la herramienta puede ejecutarse."""
    motivo = motivo_guardian(herramienta, entrada) or motivo_registro(herramienta, entrada)
    if motivo:
        return motivo
    motivo = motivo_sellado(herramienta, entrada)
    if motivo:
        protocolo = protocolo_aprobado()
        if protocolo is None:
            return f"DATOS SELLADOS: {motivo}. Requiere protocolo aprobado por Diego (ver protocols/README.md)."
        anotar_acceso(herramienta, entrada, protocolo)
    return None


def autotest() -> int:
    casos = [
        ("Read", {"file_path": "data/sealed/xauusd.csv"}, True),
        ("Read", {"file_path": str(RAIZ / "data" / "sealed" / "x.csv")}, True),
        ("Read", {"file_path": "C:\\Lab\\data\\Sealed\\x.csv"}, True),
        ("Read", {"file_path": "data/raw/xauusd.csv"}, False),
        ("Glob", {"pattern": "data/**/*.csv"}, True),
        ("Glob", {"pattern": "data/s*/*"}, True),
        ("Glob", {"pattern": "**/*.py", "path": "src"}, False),
        ("Grep", {"pattern": "sealed", "path": "CLAUDE.md"}, False),
        ("Grep", {"pattern": "x", "path": "data/sealed"}, True),
        ("Bash", {"command": "cat data/sealed/a.csv"}, True),
        ("Bash", {"command": "python -c \"open('data/' + 'sealed/a')\""}, True),
        ("Bash", {"command": "ls data"}, False),
        ("Bash", {"command": "find data -name '*.csv'"}, True),
        ("Bash", {"command": "grep -rn foo ."}, True),
        ("Bash", {"command": "grep -rn foo . --exclude-dir=sealed"}, False),
        ("Bash", {"command": "grep -rn foo src tests"}, False),
        ("Bash", {"command": "git status"}, False),
        ("Bash", {"command": "python -c \"print(list(zip(a, b)))\""}, False),
        ("Bash", {"command": "zip -r copia.zip data"}, True),
        ("Bash", {"command": "zip copia.zip notas.txt"}, True),
        ("Bash", {"command": "python -m unittest discover -s tests"}, False),
        ("Edit", {"file_path": "registry/experimentos.jsonl"}, True),
        ("Bash", {"command": "rm registry/experimentos.jsonl"}, True),
        ("Bash", {"command": "echo x > registry/accesos.log"}, True),
        ("Bash", {"command": "echo x >> registry/notas.log"}, False),
        ("Edit", {"file_path": ".claude/settings.json"}, True),
        ("Bash", {"command": "rm .claude/hooks/guardian.py"}, True),
        ("Write", {"file_path": "h0/ficha.md"}, False),
        # PowerShell: mismas reglas que Bash
        ("PowerShell", {"command": "Get-Content data/sealed/a.csv"}, True),
        ("PowerShell", {"command": "Get-Content C:\\Lab\\data\\Sealed\\a.csv"}, True),
        ("PowerShell", {"command": "Get-ChildItem -Recurse data"}, True),
        ("PowerShell", {"command": "gci -r -Filter *.csv"}, True),
        ("PowerShell", {"command": "Get-ChildItem -Recurse src"}, False),
        ("PowerShell", {"command": "Get-ChildItem data"}, False),
        ("PowerShell", {"command": "Compress-Archive data copia.zip"}, True),
        ("PowerShell", {"command": "Remove-Item registry/experimentos.jsonl"}, True),
        ("PowerShell", {"command": "Set-Content registry/accesos.log x"}, True),
        ("PowerShell", {"command": "Move-Item registry/a.log registry/b.log"}, True),
        ("PowerShell", {"command": "Add-Content registry/notas.log x"}, False),
        ("PowerShell", {"command": "Set-Content .claude/hooks/guardian.py x"}, True),
        ("PowerShell", {"command": "Copy-Item x.json .claude\\settings.json"}, True),
        ("PowerShell", {"command": "[IO.File]::WriteAllText('.claude/hooks/guardian.py', 'x')"}, True),
        ("PowerShell", {"command": "git status"}, False),
        ("PowerShell", {"command": "python -m unittest discover -s tests"}, False),
    ]
    fallos = 0
    for herramienta, entrada, bloquear in casos:
        bloqueado = decidir(herramienta, entrada) is not None
        if bloqueado != bloquear:
            fallos += 1
            print(f"FALLO {herramienta} {entrada}: bloqueado={bloqueado}, esperado={bloquear}")
    print(f"autotest: {len(casos) - fallos}/{len(casos)} correctos")
    return 1 if fallos else 0


def main() -> int:
    if "--autotest" in sys.argv:
        os.environ.pop("LAB_PROTOCOLO_SELLADO", None)
        os.environ.pop("LAB_MANTENIMIENTO_GUARDIAN", None)
        return autotest()
    try:
        evento = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        print("guardián: entrada no válida; se bloquea por precaución", file=sys.stderr)
        return 2
    motivo = decidir(evento.get("tool_name", ""), evento.get("tool_input") or {})
    if motivo:
        print(f"Bloqueado por el guardián del laboratorio: {motivo}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
