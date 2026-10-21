"""Clasifica las velas que difieren entre dos exportaciones (B1, criterio A4): precio frente a volumen, y si las de
volumen son exactamente las que superan el máximo de un entero de 32 bits (2.147.483.647).

Uso:  python -I h0/configs/b1_analizar_diferencias.py A.csv B.csv
"""

import json
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from b1_comparar_velas import leer  # noqa: E402

INT32_MAX = Decimal(2**31 - 1)


def main(ruta_a: str, ruta_b: str) -> int:
    a, b = dict(leer(ruta_a)), dict(leer(ruta_b))
    comunes = set(a) & set(b)
    precio_distinto = [t for t in comunes if a[t][:4] != b[t][:4]]
    solo_volumen = [t for t in comunes if a[t][:4] == b[t][:4] and a[t][4] != b[t][4]]
    sobre_int32_a = [t for t in a if a[t][4] > INT32_MAX]
    recortadas = [t for t in solo_volumen if a[t][4] > INT32_MAX and b[t][4] == INT32_MAX]
    resumen = {
        "velas_comunes": len(comunes),
        "precio_distinto": len(precio_distinto),
        "solo_volumen_distinto": len(solo_volumen),
        "volumen_original_sobre_int32": len(sobre_int32_a),
        "recortadas_exactamente_a_int32_max": len(recortadas),
        "volumen_distinto_sin_explicar": len(set(solo_volumen) - set(recortadas)),
        "las_recortadas_son_todas_las_que_superan_int32": set(recortadas) == set(sobre_int32_a),
        "volumen_original_maximo": str(max(v[4] for v in a.values())),
        "primera_recortada": min(recortadas).isoformat(sep=" ") if recortadas else None,
        "ultima_recortada": max(recortadas).isoformat(sep=" ") if recortadas else None,
    }
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
