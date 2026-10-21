"""B17, DIAGNÓSTICO posterior a ver los datos (no sustituye a ningún criterio): ¿la persistencia dentro/fuera de muestra
del Sharpe en los brazos SIN ventaja se explica por la frecuencia de operaciones (los costes castigan igual en los dos
tramos a las estrategias que operan mucho)?

Uso:  python -I h0/configs/b17_diagnostico_persistencia.py N ANTES_REAL DESPUES_REAL ANTES_NULO1 DESPUES_NULO1 ...

Por brazo, sobre las mismas estrategias que usa la comprobación S (≥ 30 operaciones dentro y ≥ 10 fuera): Spearman del
Sharpe con el número de operaciones dentro de muestra, y Spearman parcial dentro/fuera controlando esa frecuencia
(correlación parcial de los rangos).
"""

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b17_analizar as ba  # noqa: E402


def parcial(rxy: float, rxz: float, ryz: float) -> float:
    return (rxy - rxz * ryz) / math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))


def main(argv: list[str]) -> int:
    n = int(argv[0])
    pares = [(argv[i], argv[i + 1]) for i in range(1, len(argv), 2)]
    salida = {}
    for nombre, (a, d) in zip(["real"] + [f"nulo{k}" for k in range(1, len(pares))], pares):
        es = [e for e in ba.nuevas(a, d, n) if e["ops_is"] >= 30 and e["ops_oos"] >= 10]
        si, so, ops = [e["sharpe_is"] for e in es], [e["sharpe_oos"] for e in es], [e["ops_is"] for e in es]
        r_io, r_iz, r_oz = ba.spearman(si, so), ba.spearman(si, ops), ba.spearman(so, ops)
        salida[nombre] = {"estrategias": len(es), "spearman_IS_OOS": round(r_io, 4),
                          "spearman_sharpe_IS_con_operaciones": round(r_iz, 4),
                          "spearman_sharpe_OOS_con_operaciones": round(r_oz, 4),
                          "spearman_parcial_IS_OOS_sin_frecuencia": round(parcial(r_io, r_iz, r_oz), 4),
                          "cota_aprox_95": round(2 / math.sqrt(len(es)), 4)}
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
