"""B17, DIAGNÓSTICO posterior (no es criterio): rendimiento logarítmico de cada serie en el tramo dentro de muestra
(2023.02.01–2024.03.31) y fuera de muestra (2024.04.01–2024.10.30). Un paseo aleatorio sin deriva total puede tener
tendencia en cada tramo; si los dos tramos van en el mismo sentido, las estrategias con sesgo comprador o vendedor
"persisten" sin ninguna ventaja.

Uso:  python -I h0/configs/b17_deriva_tramos.py NOMBRE=ARCHIVO_CUSTOM.csv [NOMBRE=ARCHIVO_CUSTOM.csv ...]
"""

import json
import math
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from b1_comparar_velas import leer  # noqa: E402

TRAMOS = {"IS": ("2023.02.01", "2024.04.01"), "OOS": ("2024.04.01", "2024.10.31")}


def deriva(velas, desde: str, hasta: str) -> float:
    a, b = datetime.strptime(desde, "%Y.%m.%d"), datetime.strptime(hasta, "%Y.%m.%d")
    tramo = [v for v in velas if a <= v[0] < b]
    return math.log(float(tramo[-1][1][3]) / float(tramo[0][1][0]))


def main(argv: list[str]) -> int:
    salida = {}
    for par in argv:
        nombre, ruta = par.split("=", 1)
        velas = leer(ruta)
        d = {t: round(deriva(velas, *rango), 4) for t, rango in TRAMOS.items()}
        d["mismo_sentido"] = (d["IS"] > 0) == (d["OOS"] > 0)
        salida[nombre] = d
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
