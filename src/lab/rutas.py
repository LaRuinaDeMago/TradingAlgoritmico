"""Rutas del proyecto y protección de data/sealed/.

Ningún código del núcleo puede leer, listar ni calcular el hash de los datos
sellados. Abrirlos exige un protocolo aprobado por Diego (ver protocols/).
"""

from __future__ import annotations

import os
from pathlib import Path

# LAB_RAIZ permite apuntar a otra raíz (lo usan los tests con carpetas temporales).
RAIZ = Path(os.environ.get("LAB_RAIZ") or Path(__file__).resolve().parents[2]).resolve()


class AccesoSelladoError(PermissionError):
    """Se intentó tocar data/sealed/ desde el núcleo."""


def carpeta_sellada(raiz: Path = RAIZ) -> Path:
    return (raiz / "data" / "sealed").resolve()


def es_sellada(ruta: str | os.PathLike, raiz: Path = RAIZ) -> bool:
    """True si la ruta está dentro de data/sealed/ o la contiene (p. ej. data/).

    Las rutas relativas se resuelven contra el directorio actual, igual que
    cuando luego se abren.
    """
    ruta = Path(ruta).resolve()
    sellada = carpeta_sellada(raiz)
    return ruta == sellada or sellada in ruta.parents or ruta in sellada.parents


def exigir_no_sellada(ruta: str | os.PathLike, raiz: Path = RAIZ) -> None:
    if es_sellada(ruta, raiz):
        raise AccesoSelladoError(
            f"Ruta bloqueada: {ruta} está en data/sealed/ o la contiene. "
            "Solo se abre con un protocolo aprobado por Diego."
        )
