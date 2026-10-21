"""Tests del análisis de B17 (h0/configs/b17_analizar.py) con casos de resultado conocido.
Ejecutar desde la raíz: python -m unittest discover -s tests"""

import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b17_analizar as ba  # noqa: E402

COLUMNAS = list(ba.COL.values())


def exportacion(ruta: Path, filas: list[dict]) -> Path:
    """Escribe un CSV con el mismo formato que `-databank action=export` (separador ';', todo entre comillas)."""
    lineas = [";".join(f'"{c}"' for c in COLUMNAS)]
    for f in filas:
        lineas.append(";".join(f'"{f.get(c, 0)}"' for c in COLUMNAS))
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return ruta


def fila(nombre, ops_is=150, pf_is=1.3, retdd_is=2.5, ops_oos=30, neto_oos=10.0, pf_oos=1.2, sh_is=0.5, sh_oos=0.2):
    return {"Strategy Name": nombre, "# of trades (IS)": ops_is, "Profit factor (IS)": pf_is,
            "Ret/DD Ratio (IS)": retdd_is, "Sharpe Ratio (IS)": sh_is, "Net profit (IS)": 100,
            "# of trades (OOS)": ops_oos, "Profit factor (OOS)": pf_oos, "Net profit (OOS)": neto_oos,
            "Sharpe Ratio (OOS)": sh_oos}


class AnalisisB17(unittest.TestCase):
    def test_fisher_caso_clasico(self):
        # tabla 3-1 / 1-3: P(X >= 3) = (C(4,3)C(4,1) + C(4,4)C(4,0)) / C(8,4) = 17/70
        self.assertAlmostEqual(ba.fisher_una_cola(3, 1, 1, 3), 17 / 70, places=12)
        self.assertAlmostEqual(ba.fisher_una_cola(0, 4, 4, 0), 1.0, places=12)

    def test_spearman_monotono_e_inverso_y_empates(self):
        x = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(ba.spearman(x, [10, 20, 30, 40, 50]), 1.0)
        self.assertAlmostEqual(ba.spearman(x, [5, 4, 3, 2, 1]), -1.0)
        self.assertEqual(ba.rangos([3, 1, 3, 2]), [3.5, 1.0, 3.5, 2.0])

    def test_permutacion_distingue_relacion_de_azar(self):
        r = random.Random(3)
        x = [r.gauss(0, 1) for _ in range(200)]
        _, p_rel = ba.spearman_permutacion(x, [v + r.gauss(0, 0.3) for v in x], veces=500)
        _, p_azar = ba.spearman_permutacion(x, [r.gauss(0, 1) for _ in x], veces=500)
        self.assertLess(p_rel, 0.01)
        self.assertGreater(p_azar, 0.01)

    def test_limites_del_embudo(self):
        e = {"ops_is": 100, "pf_is": 1.20, "retdd_is": 2.0, "ops_oos": 20, "neto_oos": 0.01, "pf_oos": 1.10}
        self.assertTrue(ba.pasa_is(e) and ba.pasa_oos(e))
        self.assertFalse(ba.pasa_is(dict(e, ops_is=99)))
        self.assertFalse(ba.pasa_oos(dict(e, neto_oos=0)))

    def test_nuevas_excluye_las_de_antes_y_para_si_no_son_n(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            antes = exportacion(d / "a.csv", [fila("Strategy 0.1"), fila("Strategy 0.2")])
            despues = exportacion(d / "b.csv", [fila("Strategy 0.1"), fila("Strategy 0.2"), fila("Strategy 0.3")])
            self.assertEqual([e["nombre"] for e in ba.nuevas(antes, despues, 1)], ["Strategy 0.3"])
            with self.assertRaises(SystemExit):  # menos de las pedidas: para
                ba.nuevas(antes, despues, 2)
            sobra_una = exportacion(d / "e.csv", [fila("Strategy 0.1"), fila("Strategy 0.2"), fila("Strategy 0.3"),
                                                   fila("Strategy 0.4")])
            self.assertEqual(len(ba.nuevas(antes, sobra_una, 1)), 2)  # exceso de un hilo: se usan todas
            muchas = exportacion(d / "f.csv", [fila("Strategy 0.1"), fila("Strategy 0.2")] +
                                 [fila(f"Strategy 1.{i}") for i in range(ba.EXCESO_MAXIMO + 2)])
            with self.assertRaises(SystemExit):  # exceso mayor que el número de hilos: para
                ba.nuevas(antes, muchas, 1)
            sin_una = exportacion(d / "c.csv", [fila("Strategy 0.1"), fila("Strategy 0.3")])
            with self.assertRaises(SystemExit):
                ba.nuevas(antes, sin_una, 1)


if __name__ == "__main__":
    unittest.main()
