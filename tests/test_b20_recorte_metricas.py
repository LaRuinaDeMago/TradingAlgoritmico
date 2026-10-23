"""Tests de B20 (h0/configs/b20_recorte_metricas.py) con bancos inventados de resultado conocido: uno que recorta, uno
que no, y uno cuya fórmula no coincide (el control tiene que tumbar la prueba).
Ejecutar desde la raíz: python -m unittest discover -s tests"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b20_recorte_metricas as b20  # noqa: E402

MET = ["Net profit", "# of trades", "Profit factor", "Drawdown", "Win/Loss ratio", "Ret/DD Ratio", "Avg. Win",
       "Avg. Loss"]


def exportacion(ruta: Path, filas: list[dict]) -> Path:
    cols = ["Strategy Name"] + [f"{m} ({t})" for t in ("IS", "OOS") for m in MET]
    lineas = [";".join(f'"{c}"' for c in cols)]
    for i, f in enumerate(filas):
        valores = [f"S{i}"] + [f[m] for t in ("IS", "OOS") for m in MET]
        lineas.append(";".join(f'"{v}"' for v in valores))
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return ruta


def fila(neto, dd, gana, pierde, wl, recorta=True, error=1.0):
    retdd, pf = neto / dd, abs(gana / pierde) * wl
    if recorta:
        retdd, pf = min(retdd, 10.0), min(pf, 5.0)
    return {"Net profit": neto, "# of trades": 100, "Drawdown": dd, "Ret/DD Ratio": round(retdd * error, 2),
            "Avg. Win": gana, "Avg. Loss": pierde, "Win/Loss ratio": wl, "Profit factor": round(pf * error, 2)}


BANCO = [(500, 100, 30, -10, 1.0), (1000, 50, 30, -10, 2.5), (300, 200, 20, -10, 1.2), (2000, 100, 40, -10, 2.0),
         (100, 50, 15, -10, 0.9)]


class TestB20(unittest.TestCase):
    def veredictos(self, **kw):
        with tempfile.TemporaryDirectory() as t:
            r = b20.analizar(b20.leer(exportacion(Path(t) / "b.csv", [fila(*x, **kw) for x in BANCO])))
            return {m: b20.veredicto(v) for m, v in r.items()}

    def test_detecta_recorte(self):
        self.assertEqual(self.veredictos(recorta=True), {"retdd": "SÍ, SQX recorta", "pf": "SÍ, SQX recorta"})

    def test_control_negativo_sin_recorte(self):
        self.assertEqual(self.veredictos(recorta=False), {"retdd": "NO recorta", "pf": "NO recorta"})

    def test_control_negativo_formula_equivocada(self):
        v = self.veredictos(recorta=True, error=1.3)
        self.assertTrue(all(x.startswith("INCONCLUSO") for x in v.values()))


if __name__ == "__main__":
    unittest.main()
