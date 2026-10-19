"""Registro de experimentos: solo se añade, nunca se borra ni se edita.

Cada línea de registry/experimentos.jsonl es un experimento (también los
fallidos). Cada entrada guarda el hash de la anterior, así que cualquier
edición o borrado posterior se detecta con `python -m lab verificar`.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from .hashing import estado_codigo, sha256_ruta
from .rutas import RAIZ

ESTADOS = ("OK", "FALLIDO", "INCONCLUSO")
HASH_INICIAL = "0" * 64


def archivo_registro(raiz: Path = RAIZ) -> Path:
    return raiz / "registry" / "experimentos.jsonl"


def _canonico(entrada: dict) -> bytes:
    return json.dumps(entrada, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _hash_entrada(entrada: dict) -> str:
    return hashlib.sha256(_canonico({k: v for k, v in entrada.items() if k != "hash"})).hexdigest()


def leer(raiz: Path = RAIZ) -> list[dict]:
    ruta = archivo_registro(raiz)
    if not ruta.exists():
        return []
    with open(ruta, encoding="utf-8") as f:
        return [json.loads(linea) for linea in f if linea.strip()]


def verificar(raiz: Path = RAIZ) -> list[str]:
    """Devuelve la lista de problemas encontrados; vacía si la cadena está intacta."""
    problemas = []
    anterior = HASH_INICIAL
    for i, entrada in enumerate(leer(raiz), start=1):
        if entrada.get("n") != i:
            problemas.append(f"línea {i}: número {entrada.get('n')} fuera de secuencia")
        if entrada.get("hash_anterior") != anterior:
            problemas.append(f"línea {i}: no enlaza con la entrada anterior")
        if entrada.get("hash") != _hash_entrada(entrada):
            problemas.append(f"línea {i}: contenido modificado después de registrarse")
        anterior = entrada.get("hash")
    return problemas


def registrar(
    *,
    descripcion: str,
    comando: str,
    version_sqx: str,
    estado: str,
    resultado,
    datos: list[str] | None = None,
    semilla: int | None = None,
    costes=None,
    notas: str = "",
    codigo: dict | None = None,
    raiz: Path = RAIZ,
) -> dict:
    """Añade un experimento al registro y devuelve la entrada escrita.

    `version_sqx` es obligatoria: si el paso no usa SQX, se escribe "N/A".
    `datos` son rutas (archivos o carpetas) cuyo SHA-256 se guarda.
    `codigo` es el estado del código tomado antes del experimento; si falta, se toma ahora.
    """
    if estado not in ESTADOS:
        raise ValueError(f"estado debe ser uno de {ESTADOS}, no {estado!r}")
    problemas = verificar(raiz)
    if problemas:
        raise RuntimeError("El registro está dañado; no se añade nada:\n" + "\n".join(problemas))

    previas = leer(raiz)
    entrada = {
        "n": len(previas) + 1,
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "descripcion": descripcion,
        "comando": comando,
        "version_sqx": version_sqx,
        "datos": {str(Path(d).as_posix()): sha256_ruta(d, raiz) for d in (datos or [])},
        "codigo": codigo if codigo is not None else estado_codigo(raiz),
        "semilla": semilla,
        "costes": costes,
        "estado": estado,
        "resultado": resultado,
        "notas": notas,
        "entorno": {"python": sys.version.split()[0], "plataforma": platform.platform()},
        "hash_anterior": previas[-1]["hash"] if previas else HASH_INICIAL,
    }
    entrada["hash"] = _hash_entrada(entrada)

    ruta = archivo_registro(raiz)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(entrada, ensure_ascii=False, sort_keys=True) + "\n")
    return entrada
