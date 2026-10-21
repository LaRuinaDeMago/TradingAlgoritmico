"""Compara vela a vela dos exportaciones de `sqcli -data action=export` (asunto B1, plan en h0/b1_plan_integridad.md).

Uso:  python -I h0/configs/b1_comparar_velas.py A.csv B.csv [--tramo-a AAAA.MM.DD AAAA.MM.DD]

Formato esperado (lo fija el plan): cabecera Date,Time,Open,High,Low,Close,Volume; fecha yyyy.MM.dd y hora HH:mm:ss.
Los números se comparan como Decimal normalizado, así que "0.91230" y "0.9123" son iguales (solo formato) pero un punto
de diferencia no. Con --tramo-a, de A solo se toman las velas de esos días, ambos incluidos (para comprobar límites).
Imprime un resumen JSON y devuelve 0 solo si las dos series son idénticas.
"""

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

COLUMNAS = ["Date", "Time", "Open", "High", "Low", "Close", "Volume"]


def leer(ruta: str | Path) -> list[tuple[datetime, tuple[Decimal, ...]]]:
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.reader(f)
        cabecera = [c.strip() for c in next(lector)]
        if cabecera != COLUMNAS:
            raise ValueError(f"{ruta}: cabecera {cabecera}, se esperaba {COLUMNAS}")
        velas = []
        for fila in lector:
            if not fila:
                continue
            momento = datetime.strptime(f"{fila[0]} {fila[1]}", "%Y.%m.%d %H:%M:%S")
            velas.append((momento, tuple(Decimal(x).normalize() for x in fila[2:7])))
    return velas


def tramo(velas, desde: str, hasta: str):
    inicio = datetime.strptime(desde, "%Y.%m.%d")
    fin = datetime.strptime(hasta, "%Y.%m.%d") + timedelta(days=1)
    return [v for v in velas if inicio <= v[0] < fin]


def desplazamiento_global(a, b) -> int | None:
    """Minutos si B es A con todas las horas movidas lo mismo (mismos valores, en el mismo orden); si no, None."""
    if len(a) != len(b) or not a:
        return None
    deltas = {b[i][0] - a[i][0] for i in range(len(a))}
    if len(deltas) == 1 and all(a[i][1] == b[i][1] for i in range(len(a))):
        minutos = int(deltas.pop().total_seconds() // 60)
        return minutos or None
    return None


def comparar(a, b) -> dict:
    cuenta_a, cuenta_b = Counter(v[0] for v in a), Counter(v[0] for v in b)
    dic_a, dic_b = dict(a), dict(b)
    ausentes = sorted(set(dic_a) - set(dic_b))
    sobrantes = sorted(set(dic_b) - set(dic_a))
    distintas = sorted(t for t in set(dic_a) & set(dic_b) if dic_a[t] != dic_b[t])
    resumen = {
        "velas_a": len(a), "velas_b": len(b),
        "primera_a": a[0][0].isoformat(sep=" ") if a else None, "ultima_a": a[-1][0].isoformat(sep=" ") if a else None,
        "primera_b": b[0][0].isoformat(sep=" ") if b else None, "ultima_b": b[-1][0].isoformat(sep=" ") if b else None,
        "duplicadas_a": sum(n - 1 for n in cuenta_a.values() if n > 1),
        "duplicadas_b": sum(n - 1 for n in cuenta_b.values() if n > 1),
        "ausentes_en_b": len(ausentes), "sobrantes_en_b": len(sobrantes), "valores_distintos": len(distintas),
        "desordenadas_b": sum(1 for i in range(1, len(b)) if b[i][0] <= b[i - 1][0]),
        "desplazamiento_global_min": desplazamiento_global(a, b),
        "ejemplos": {
            "ausentes": [t.isoformat(sep=" ") for t in ausentes[:3]],
            "sobrantes": [t.isoformat(sep=" ") for t in sobrantes[:3]],
            "distintas": [[t.isoformat(sep=" "), [str(x) for x in dic_a[t]], [str(x) for x in dic_b[t]]]
                          for t in distintas[:3]],
        },
    }
    claves_cero = ("duplicadas_a", "duplicadas_b", "ausentes_en_b", "sobrantes_en_b", "valores_distintos",
                   "desordenadas_b")
    resumen["identicas"] = len(a) == len(b) and all(resumen[k] == 0 for k in claves_cero)
    return resumen


def main(argv: list[str]) -> int:
    a, b = leer(argv[0]), leer(argv[1])
    if len(argv) == 5 and argv[2] == "--tramo-a":
        a = tramo(a, argv[3], argv[4])
    elif len(argv) != 2:
        sys.exit(__doc__)
    resumen = comparar(a, b)
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    return 0 if resumen["identicas"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
