"""Propiedades del generador de datos sin ventaja de B17 (h0/configs/b17_sintetico.py).
Ejecutar desde la raíz: python -m unittest discover -s tests"""

import math
import random
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b17_sintetico as bs  # noqa: E402


def velas_con_tendencia(n=3000, semilla=7):
    """Serie inventada (no de mercado) con tendencia y dependencia: lo que el generador debe destruir."""
    r = random.Random(semilla)
    velas, cierre, t = [], 1.0, datetime(2023, 1, 2, 0, 0)
    choque = 0.0
    for i in range(n):
        choque = 0.6 * choque + r.gauss(0, 0.0002)  # autocorrelación fuerte a propósito
        o = cierre
        c = o * math.exp(0.00005 + choque)  # deriva positiva a propósito
        h, l = max(o, c) * 1.0001, min(o, c) * 0.9999
        velas.append((t + timedelta(minutes=i), o, h, l, c, str(1000 + i)))
        cierre = c
    return velas


def autocorrelacion(x):
    m = sum(x) / len(x)
    num = sum((x[i] - m) * (x[i - 1] - m) for i in range(1, len(x)))
    return num / sum((v - m) ** 2 for v in x)


class GeneradorSinVentaja(unittest.TestCase):
    def setUp(self):
        self.reales = velas_con_tendencia()
        self.sint = bs.sintetizar(self.reales, 1)

    def test_mismas_horas_y_mismo_numero(self):
        self.assertEqual([v[0] for v in self.sint], [v[0] for v in self.reales])

    def test_formas_conservadas_salvo_el_salto(self):
        # 9 decimales: el viaje exp/log deja errores de coma flotante del orden de 1e-12 (un precio tiene 5 decimales)
        a = sorted((round(h, 9), round(l, 9), round(c, 9), v) for _, h, l, c, v in bs.formas(self.reales))
        b = sorted((round(h, 9), round(l, 9), round(c, 9), v) for _, h, l, c, v in bs.formas(self.sint))
        self.assertEqual(a, b)

    def test_ohlc_coherente(self):
        for _, o, h, l, c, _ in self.sint:
            self.assertGreaterEqual(h, max(o, c) - 1e-15)
            self.assertLessEqual(l, min(o, c) + 1e-15)

    def test_deriva_eliminada(self):
        real = math.log(self.reales[-1][4] / self.reales[0][4])
        sint = math.log(self.sint[-1][4] / self.sint[0][4])
        self.assertGreater(abs(real), 0.1)
        self.assertLess(abs(sint), 1e-9)

    def test_dependencia_destruida(self):
        rend = lambda vs: [math.log(vs[i][4] / vs[i - 1][4]) for i in range(1, len(vs))]  # noqa: E731
        self.assertGreater(autocorrelacion(rend(self.reales)), 0.4)
        self.assertLess(abs(autocorrelacion(rend(self.sint))), 4 / math.sqrt(len(self.sint)))

    def test_repetible_con_la_semilla_y_distinto_con_otra(self):
        self.assertEqual(bs.sintetizar(self.reales, 1), self.sint)
        self.assertNotEqual(bs.sintetizar(self.reales, 2), self.sint)

    def test_escritura_mt4_redondeo_coherente(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / "s.csv"
            bs.escribir_mt4(self.sint, ruta)
            for linea in ruta.read_text(encoding="utf-8").splitlines():
                f = linea.split(",")
                o, h, l, c = map(float, f[2:6])
                self.assertEqual(len(f), 7)
                self.assertGreaterEqual(h, max(o, c))
                self.assertLessEqual(l, min(o, c))


if __name__ == "__main__":
    unittest.main()
