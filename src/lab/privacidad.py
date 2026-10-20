"""Redacción de datos privados en las evidencias: el repositorio de GitHub es público.

El original completo se guarda en h0/evidencias_privadas/ (fuera de git, solo en el PC de SQX) y en
h0/evidencias/ va una copia con cada dato privado sustituido por [REDACTADO:tipo]. El registro guarda
el hash de las dos copias y cuántas sustituciones hubo de cada tipo.

Los patrones son una lista cerrada y conocida: lo que no encaja en ellos NO se redacta. Por eso,
antes de cada commit, la evidencia pública se lee entera.
"""

from __future__ import annotations

import re
from pathlib import Path

CARPETA_PRIVADA = Path("h0") / "evidencias_privadas"

PATRONES: dict[str, tuple[re.Pattern[bytes], bytes]] = {
    # Identificador de máquina con el que SQX liga la licencia ("Hardware ID: CAC3...").
    "hardware_id": (re.compile(rb"(Hardware ID:[ \t]*)[0-9A-Fa-f]+"), rb"\1[REDACTADO:hardware_id]"),
    # Línea de depuración del gestor de licencias ("Licenser -- L: 01234567").
    "licencia": (re.compile(rb"(Licenser -- L:[ \t]*)\S+"), rb"\1[REDACTADO:licencia]"),
    # Claves de API de Anthropic.
    "clave_api": (re.compile(rb"sk-ant-[\w-]+"), rb"[REDACTADO:clave_api]"),
    # Direcciones de correo.
    "email": (re.compile(rb"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), rb"[REDACTADO:email]"),
}


def redactar(contenido: bytes) -> tuple[bytes, dict[str, int]]:
    """Devuelve el contenido con los datos privados sustituidos y cuántos hubo de cada tipo."""
    cuentas = {}
    for nombre, (patron, sustituto) in PATRONES.items():
        contenido, n = patron.subn(sustituto, contenido)
        if n:
            cuentas[nombre] = n
    return contenido, cuentas
