"""Línea de comandos del laboratorio.

    python -m lab hash RUTA...
    python -m lab verificar
    python -m lab registrar --descripcion ... --comando ... --version-sqx ... --estado OK --resultado ...
    python -m lab ejecutar --nombre tarea1_sqcli_ayuda --version-sqx 143.2708 -- "C:/ruta/sqcli.exe" -h
    python -m lab redactar --version-sqx 145.3191-dev h0/evidencias/ARCHIVO.txt

(Ejecutar desde la raíz del repositorio con PYTHONPATH=src, o tras `pip install -e .`)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import registro
from .ejecutar import ejecutar, redactar_evidencia
from .hashing import sha256_ruta


def _json_o_texto(valor: str | None):
    """Acepta un archivo .json, un texto JSON o texto libre."""
    if valor is None:
        return None
    if valor.lower().endswith(".json") and Path(valor).is_file():
        return json.loads(Path(valor).read_text(encoding="utf-8"))
    try:
        return json.loads(valor)
    except json.JSONDecodeError:
        return valor


def _comunes(p: argparse.ArgumentParser) -> None:
    p.add_argument("--version-sqx", required=True, help='build de SQX usada, o "N/A"')
    p.add_argument("--datos", nargs="*", default=[], help="archivos o carpetas de datos usados")
    p.add_argument("--semilla", type=int)
    p.add_argument("--costes", help="archivo .json, texto JSON o descripción de los costes usados")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m lab", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="orden", required=True)

    p_hash = sub.add_parser("hash", help="SHA-256 de archivos o carpetas")
    p_hash.add_argument("rutas", nargs="+")

    sub.add_parser("verificar", help="comprueba que el registro no se ha alterado")

    p_reg = sub.add_parser("registrar", help="anota un experimento hecho a mano")
    p_reg.add_argument("--descripcion", required=True)
    p_reg.add_argument("--comando", required=True, help='comando exacto, o "MANUAL: pasos en la GUI"')
    p_reg.add_argument("--estado", required=True, choices=registro.ESTADOS)
    p_reg.add_argument("--resultado", required=True)
    p_reg.add_argument("--notas", default="")
    _comunes(p_reg)

    p_eje = sub.add_parser("ejecutar", help="ejecuta un comando, guarda la evidencia y lo registra")
    p_eje.add_argument("--nombre", required=True, help="nombre corto para el archivo de evidencia")
    p_eje.add_argument("--descripcion", default="")
    p_eje.add_argument("--timeout", type=float, default=900)
    p_eje.add_argument("--evidencias", default="h0/evidencias")
    _comunes(p_eje)
    p_eje.add_argument("comando", nargs=argparse.REMAINDER, help="tras --, el comando a ejecutar")

    p_red = sub.add_parser("redactar", help="redacta datos privados de una evidencia ya escrita y lo registra")
    p_red.add_argument("--version-sqx", required=True, help='build de SQX que produjo la evidencia, o "N/A"')
    p_red.add_argument("evidencia")

    a = parser.parse_args(argv)

    if a.orden == "hash":
        for ruta in a.rutas:
            print(f"{sha256_ruta(ruta)}  {ruta}")
        return 0

    if a.orden == "verificar":
        problemas = registro.verificar()
        n = len(registro.leer())
        if problemas:
            print("REGISTRO ALTERADO:\n" + "\n".join(problemas))
            return 1
        print(f"Registro íntegro: {n} entradas.")
        return 0

    if a.orden == "registrar":
        entrada = registro.registrar(
            descripcion=a.descripcion, comando=a.comando, version_sqx=a.version_sqx,
            estado=a.estado, resultado=_json_o_texto(a.resultado), datos=a.datos,
            semilla=a.semilla, costes=_json_o_texto(a.costes), notas=a.notas,
        )
    elif a.orden == "redactar":
        entrada = redactar_evidencia(a.evidencia, version_sqx=a.version_sqx)
    else:
        comando = a.comando[1:] if a.comando[:1] == ["--"] else a.comando
        if not comando:
            parser.error("falta el comando a ejecutar tras --")
        entrada = ejecutar(
            comando, nombre=a.nombre, version_sqx=a.version_sqx, descripcion=a.descripcion,
            datos=a.datos, semilla=a.semilla, costes=_json_o_texto(a.costes),
            timeout=a.timeout, evidencias=a.evidencias,
        )
    print(json.dumps(entrada, ensure_ascii=False, indent=2))
    return 0 if entrada["estado"] != "FALLIDO" else 2


if __name__ == "__main__":
    sys.exit(main())
