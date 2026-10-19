"""Ejecuta un comando externo (p. ej. sqcli.exe), guarda su salida como evidencia
y lo anota en el registro, tanto si sale bien como si falla."""

from __future__ import annotations

import os
import re
import shlex
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from .hashing import sha256_archivo
from .registro import registrar
from .rutas import RAIZ, AccesoSelladoError

PATRON_SELLADO = re.compile(r"data[\\/]+sealed", re.IGNORECASE)


def ejecutar(
    comando: list[str],
    *,
    nombre: str,
    version_sqx: str,
    descripcion: str = "",
    datos: list[str] | None = None,
    semilla: int | None = None,
    costes=None,
    timeout: float = 900,
    evidencias: str | Path = "h0/evidencias",
    raiz: Path = RAIZ,
) -> dict:
    if any(PATRON_SELLADO.search(arg) for arg in comando):
        raise AccesoSelladoError("El comando menciona data/sealed/; bloqueado.")
    if not re.fullmatch(r"[\w.-]+", nombre):
        raise ValueError("nombre solo admite letras, números, '.', '_' y '-'")

    inicio = datetime.now(timezone.utc)
    carpeta = Path(evidencias)
    if not carpeta.is_absolute():
        carpeta = raiz / carpeta
    carpeta.mkdir(parents=True, exist_ok=True)
    evidencia = carpeta / f"{inicio:%Y%m%dT%H%M%SZ}_{nombre}.txt"
    texto_comando = subprocess.list2cmdline(comando) if os.name == "nt" else shlex.join(comando)

    t0 = time.perf_counter()
    try:
        # stdin cerrado: si el programa espera una entrada interactiva, no se queda colgado.
        proceso = subprocess.run(
            comando, capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout
        )
        codigo, salida, errores, motivo = proceso.returncode, proceso.stdout, proceso.stderr, ""
    except subprocess.TimeoutExpired as e:
        codigo, salida, errores = None, e.stdout or b"", e.stderr or b""
        motivo = f"superó el tiempo máximo de {timeout} s"
    except OSError as e:
        codigo, salida, errores, motivo = None, b"", b"", f"no se pudo lanzar: {e}"
    duracion = round(time.perf_counter() - t0, 3)

    with open(evidencia, "wb") as f:
        cabecera = (
            f"# comando: {texto_comando}\n# inicio_utc: {inicio.isoformat(timespec='seconds')}\n"
            f"# duracion_s: {duracion}\n# codigo_salida: {codigo}\n# incidencia: {motivo or '-'}\n"
        )
        f.write(cabecera.encode("utf-8"))
        f.write(b"\n=== STDOUT ===\n" + salida + b"\n=== STDERR ===\n" + errores)

    resultado = {
        "codigo_salida": codigo,
        "duracion_s": duracion,
        "incidencia": motivo or None,
        "evidencia": evidencia.relative_to(raiz).as_posix() if evidencia.is_relative_to(raiz) else str(evidencia),
        "sha256_evidencia": sha256_archivo(evidencia, raiz),
    }
    return registrar(
        descripcion=descripcion or nombre,
        comando=texto_comando,
        version_sqx=version_sqx,
        estado="OK" if codigo == 0 else "FALLIDO",
        resultado=resultado,
        datos=datos,
        semilla=semilla,
        costes=costes,
        raiz=raiz,
    )
