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

from .hashing import estado_codigo, sha256_archivo
from .privacidad import CARPETA_PRIVADA, redactar
from .registro import registrar
from .rutas import RAIZ, AccesoSelladoError

PATRON_SELLADO = re.compile(r"data[\\/]+sealed", re.IGNORECASE)


def _relativa(ruta: Path, raiz: Path) -> str:
    return ruta.relative_to(raiz).as_posix() if ruta.is_relative_to(raiz) else str(ruta)


def redactar_evidencia(ruta: str | Path, *, version_sqx: str, raiz: Path = RAIZ) -> dict:
    """Para una evidencia ya escrita sin redactar: mueve el original a la carpeta privada,
    deja al lado una copia redactada (.redactada) y lo anota en el registro."""
    ruta = Path(ruta)
    if not ruta.is_absolute():
        ruta = raiz / ruta
    original = ruta.read_bytes()
    publica, redacciones = redactar(original)
    if not redacciones:
        raise ValueError(f"{ruta} no contiene nada que redactar; se deja como está")
    privada = raiz / CARPETA_PRIVADA / ruta.name
    if privada.exists():
        raise FileExistsError(f"ya existe {privada}; no se sobrescribe")
    copia = ruta.with_name(f"{ruta.stem}.redactada{ruta.suffix}")
    codigo_previo = estado_codigo(raiz)
    privada.parent.mkdir(parents=True, exist_ok=True)
    privada.write_bytes(original)
    copia.write_bytes(publica)
    ruta.unlink()
    resultado = {
        "evidencia_original": _relativa(ruta, raiz),
        "evidencia_privada": _relativa(privada, raiz),
        "sha256_evidencia_privada": sha256_archivo(privada, raiz),
        "evidencia": _relativa(copia, raiz),
        "sha256_evidencia": sha256_archivo(copia, raiz),
        "redacciones": redacciones,
    }
    return registrar(
        descripcion=f"Redacción de datos privados de {resultado['evidencia_original']} (repositorio público)",
        comando=f"python -m lab redactar --version-sqx {version_sqx} {resultado['evidencia_original']}",
        version_sqx=version_sqx,
        estado="OK",
        resultado=resultado,
        codigo=codigo_previo,
        raiz=raiz,
    )


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
    if redactar(texto_comando.encode("utf-8"))[1]:
        raise ValueError("El comando contiene datos privados y el registro (público) lo copia literal; "
                         "pásalos en un archivo (p. ej. -run file=...)")
    # Antes de escribir la evidencia: si no, el propio archivo nuevo marcaría el código como sucio.
    codigo_previo = estado_codigo(raiz)

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

    cabecera = (
        f"# comando: {texto_comando}\n# inicio_utc: {inicio.isoformat(timespec='seconds')}\n"
        f"# duracion_s: {duracion}\n# codigo_salida: {codigo}\n# incidencia: {motivo or '-'}\n"
    )
    original = cabecera.encode("utf-8") + b"\n=== STDOUT ===\n" + salida + b"\n=== STDERR ===\n" + errores
    publica, redacciones = redactar(original)
    evidencia.write_bytes(publica)

    resultado = {
        "codigo_salida": codigo,
        "duracion_s": duracion,
        "incidencia": motivo or None,
        "evidencia": _relativa(evidencia, raiz),
        "sha256_evidencia": sha256_archivo(evidencia, raiz),
        "redacciones": redacciones,
        "evidencia_privada": None,
        "sha256_evidencia_privada": None,
    }
    if redacciones:
        # El original completo se queda fuera de git (el repositorio es público).
        privada = raiz / CARPETA_PRIVADA / evidencia.name
        privada.parent.mkdir(parents=True, exist_ok=True)
        privada.write_bytes(original)
        resultado["evidencia_privada"] = _relativa(privada, raiz)
        resultado["sha256_evidencia_privada"] = sha256_archivo(privada, raiz)
    return registrar(
        descripcion=descripcion or nombre,
        comando=texto_comando,
        version_sqx=version_sqx,
        estado="OK" if codigo == 0 else "FALLIDO",
        resultado=resultado,
        datos=datos,
        semilla=semilla,
        costes=costes,
        codigo=codigo_previo,
        raiz=raiz,
    )
