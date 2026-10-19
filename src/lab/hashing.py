"""Hashes SHA-256 de datos y del estado del código."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

from .rutas import RAIZ, exigir_no_sellada

BLOQUE = 1 << 20


def sha256_archivo(ruta: str | os.PathLike, raiz: Path = RAIZ) -> str:
    exigir_no_sellada(ruta, raiz)
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for trozo in iter(lambda: f.read(BLOQUE), b""):
            h.update(trozo)
    return h.hexdigest()


def sha256_carpeta(ruta: str | os.PathLike, raiz: Path = RAIZ) -> str:
    """Hash estable de una carpeta: rutas relativas y contenido, en orden."""
    exigir_no_sellada(ruta, raiz)
    ruta = Path(ruta)
    h = hashlib.sha256()
    for archivo in sorted(p for p in ruta.rglob("*") if p.is_file()):
        relativa = archivo.relative_to(ruta).as_posix()
        h.update(relativa.encode("utf-8") + b"\0")
        h.update(sha256_archivo(archivo, raiz).encode("ascii") + b"\n")
    return h.hexdigest()


def sha256_ruta(ruta: str | os.PathLike, raiz: Path = RAIZ) -> str:
    return sha256_carpeta(ruta, raiz) if Path(ruta).is_dir() else sha256_archivo(ruta, raiz)


def _git(args: list[str], raiz: Path) -> str:
    return subprocess.run(
        ["git", *args], cwd=raiz, capture_output=True, check=True
    ).stdout.decode("utf-8", errors="replace")


def estado_codigo(raiz: Path = RAIZ) -> dict:
    """Commit actual y, si hay cambios sin confirmar, un hash de esos cambios.

    Un experimento con "sucio": true no es reproducible desde el commit solo.
    """
    try:
        commit = _git(["rev-parse", "HEAD"], raiz).strip()
    except (OSError, subprocess.CalledProcessError):
        return {"commit": "SIN_GIT", "sucio": None, "hash_cambios": None}
    estado = _git(["status", "--porcelain", "--untracked-files=all"], raiz)
    if not estado.strip():
        return {"commit": commit, "sucio": False, "hash_cambios": None}
    h = hashlib.sha256(_git(["diff", "HEAD", "--binary"], raiz).encode("utf-8"))
    for linea in sorted(estado.splitlines()):
        if linea.startswith("??"):
            nuevo = raiz / linea[3:].strip().strip('"')
            if nuevo.is_file():
                h.update(linea.encode("utf-8") + sha256_archivo(nuevo, raiz).encode("ascii"))
    return {"commit": commit, "sucio": True, "hash_cambios": h.hexdigest()}
