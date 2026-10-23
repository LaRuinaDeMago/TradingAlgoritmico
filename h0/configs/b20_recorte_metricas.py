"""B20 (plan h0/b20_plan_recorte_metricas.md): ¿recorta SQX Ret/DD a 10 y el factor de beneficio a 5?

Con una exportación de banco ya existente (`-databank action=export`), se recalcula cada métrica con las columnas que
la definen y se compara con la que da SQX:
  Ret/DD = Net profit / Drawdown
  PF     = |Avg. Win / Avg. Loss| · (Win/Loss ratio)       (ganadoras/perdedoras = Win/Loss ratio)
Control: donde lo recalculado queda claramente por debajo del supuesto tope, tiene que coincidir con SQX (si no, la
fórmula no es la de SQX y la prueba no vale). Prueba: donde lo recalculado queda claramente por encima, ¿SQX da justo
el tope?

Uso: python -I h0/configs/b20_recorte_metricas.py EXPORTACION.csv
"""

import csv
import io
import sys
from pathlib import Path

TOPES = {"retdd": 10.0, "pf": 5.0}
MARGEN = 0.05       # zona de exclusión alrededor del tope (relativa): ni control ni prueba
TOLERANCIA = 0.02   # diferencia relativa admitida en el control (las cifras del CSV van redondeadas)
ABSOLUTA = 0.02     # y absoluta, para valores pequeños


def _num(texto: str) -> float:
    return float(texto.replace(",", "") or 0)


def leer(ruta: str | Path) -> list[dict]:
    filas = list(csv.DictReader(io.StringIO(Path(ruta).read_bytes().decode("utf-8-sig")), delimiter=";"))
    salida = []
    for f in filas:
        for tramo in ("IS", "OOS"):
            g = lambda c: _num(f[f"{c} ({tramo})"])  # noqa: E731
            salida.append({"nombre": f["Strategy Name"], "tramo": tramo, "operaciones": g("# of trades"),
                           "neto": g("Net profit"), "dd": g("Drawdown"), "retdd_sqx": g("Ret/DD Ratio"),
                           "gana": g("Avg. Win"), "pierde": g("Avg. Loss"), "wl": g("Win/Loss ratio"),
                           "pf_sqx": g("Profit factor")})
    return salida


def recalcular(e: dict) -> dict:
    retdd = e["neto"] / abs(e["dd"]) if e["dd"] else None
    pf = abs(e["gana"] / e["pierde"]) * e["wl"] if e["pierde"] and e["wl"] else None
    return {"retdd": retdd, "pf": pf}


def analizar(filas: list[dict]) -> dict:
    res = {}
    for m in ("retdd", "pf"):
        tope, control, prueba = TOPES[m], [], []
        for e in filas:
            if e["operaciones"] < 1:
                continue
            calc, sqx = recalcular(e)[m], e[f"{m}_sqx"]
            if calc is None or calc <= 0:
                continue
            if calc < tope * (1 - MARGEN):
                control.append(abs(sqx - calc) <= max(TOLERANCIA * calc, ABSOLUTA))
            elif calc > tope * (1 + MARGEN):
                prueba.append(sqx == tope)
        maximo = max(e[f"{m}_sqx"] for e in filas)
        en_tope = sum(1 for e in filas if e[f"{m}_sqx"] == tope)
        res[m] = {"tope": tope, "control_n": len(control), "control_coinciden": sum(control),
                  "prueba_n": len(prueba), "prueba_en_tope": sum(prueba), "max_sqx": maximo, "filas_en_tope": en_tope}
    return res


def veredicto(r: dict) -> str:
    if r["control_n"] == 0 or r["control_coinciden"] / r["control_n"] < 0.99:
        return "INCONCLUSO (la fórmula no reproduce a SQX por debajo del tope)"
    if r["prueba_n"] == 0:
        return "INCONCLUSO (ningún caso por encima del tope)"
    if r["prueba_en_tope"] == r["prueba_n"] and r["max_sqx"] == r["tope"]:
        return "SÍ, SQX recorta"
    if r["prueba_en_tope"] == 0:
        return "NO recorta"
    return "INCONCLUSO (mezcla)"


def main(argv: list[str]) -> int:
    r = analizar(leer(argv[0]))
    for m, v in r.items():
        print(f"{m}: tope {v['tope']}; control {v['control_coinciden']}/{v['control_n']} coinciden; "
              f"por encima del tope {v['prueba_en_tope']}/{v['prueba_n']} valen justo el tope; "
              f"máximo en SQX {v['max_sqx']}; filas en el tope {v['filas_en_tope']} -> {veredicto(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
