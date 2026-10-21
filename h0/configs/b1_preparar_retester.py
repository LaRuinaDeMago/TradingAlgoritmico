"""Plantillas del Retester para B1 paso 7: las mismas de la tarea 4 (preparar_retester_usdchf.py: mismos datos, costes
y opciones, sin filtros ni cross checks) cambiando solo el símbolo y el banco.

Uso:  python -I h0/configs/b1_preparar_retester.py ORIGEN.cfx DESTINO.cfx SIMBOLO [DESDE]

DESDE (aaaa.mm.dd) solo para B1-bis: inicio del backtest después de un margen de calentamiento.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import preparar_retester_usdchf as base  # noqa: E402

BANCO_B1 = "H0_B1"


def main(origen: str, destino: str, simbolo: str, desde: str | None = None) -> None:
    base.SIMBOLO, base.BANCO = simbolo, BANCO_B1
    if desde:
        base.DESDE = desde
    base.main(origen, destino)


if __name__ == "__main__":
    main(*sys.argv[1:5])
