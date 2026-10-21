"""Errores sembrados para el comparador de velas de B1 (control negativo C1 del plan h0/b1_plan_integridad.md).
Ejecutar desde la raíz: python -m unittest discover -s tests"""

import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b1_comparar_velas as cv  # noqa: E402

CABECERA = "Date,Time,Open,High,Low,Close,Volume\n"


def filas_sinteticas(n=120, inicio=datetime(2023, 6, 29, 23, 0)):
    """Velas M1 inventadas (valores de prueba, no de mercado) que cruzan un cambio de día."""
    filas = []
    for i in range(n):
        t = inicio + timedelta(minutes=i)
        p = 0.9 + i * 0.00001
        filas.append([t.strftime("%Y.%m.%d"), t.strftime("%H:%M:%S"),
                      f"{p:.5f}", f"{p + 0.0002:.5f}", f"{p - 0.0002:.5f}", f"{p + 0.0001:.5f}", str(10 + i)])
    return filas


class ComparadorDeVelas(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.base = filas_sinteticas()
        self.a = self.escribir("a.csv", self.base)

    def tearDown(self):
        self._tmp.cleanup()

    def escribir(self, nombre, filas):
        ruta = self.dir / nombre
        ruta.write_text(CABECERA + "".join(",".join(f) + "\n" for f in filas), encoding="utf-8")
        return ruta

    def comparar_con(self, filas):
        return cv.comparar(cv.leer(self.a), cv.leer(self.escribir("b.csv", filas)))

    def test_identica_a_si_misma(self):
        r = self.comparar_con(self.base)
        self.assertTrue(r["identicas"])
        self.assertEqual(r["velas_a"], 120)

    def test_solo_formato_numerico_no_cuenta(self):
        filas = [f[:2] + [x + "0" for x in f[2:6]] + f[6:] for f in self.base]  # 0.90000 -> 0.900000
        self.assertTrue(self.comparar_con(filas)["identicas"])

    def test_vela_eliminada(self):
        r = self.comparar_con(self.base[:50] + self.base[51:])
        self.assertFalse(r["identicas"])
        self.assertEqual(r["ausentes_en_b"], 1)

    def test_vela_duplicada(self):
        r = self.comparar_con(self.base[:50] + [self.base[50]] + self.base[50:])
        self.assertFalse(r["identicas"])
        self.assertEqual(r["duplicadas_b"], 1)

    def test_precio_alterado_un_punto(self):
        filas = [list(f) for f in self.base]
        filas[70][5] = f"{float(filas[70][5]) + 0.00001:.5f}"
        r = self.comparar_con(filas)
        self.assertFalse(r["identicas"])
        self.assertEqual(r["valores_distintos"], 1)

    def test_una_vela_desplazada_un_minuto(self):
        filas = [list(f) for f in self.base]
        filas[30][1] = "23:30:30"  # 23:30:00 -> 23:30:30: deja un hueco y una vela fuera de su minuto
        r = self.comparar_con(filas)
        self.assertFalse(r["identicas"])
        self.assertEqual((r["ausentes_en_b"], r["sobrantes_en_b"]), (1, 1))

    def test_todo_desplazado_una_hora(self):
        filas = []
        for f in self.base:
            t = datetime.strptime(f"{f[0]} {f[1]}", "%Y.%m.%d %H:%M:%S") + timedelta(hours=1)
            filas.append([t.strftime("%Y.%m.%d"), t.strftime("%H:%M:%S")] + f[2:])
        r = self.comparar_con(filas)
        self.assertFalse(r["identicas"])
        self.assertEqual(r["desplazamiento_global_min"], 60)

    def test_tramo_incluye_dias_completos(self):
        velas = cv.tramo(cv.leer(self.a), "2023.06.30", "2023.06.30")
        self.assertEqual(velas[0][0], datetime(2023, 6, 30, 0, 0))
        self.assertEqual(velas[-1][0], datetime(2023, 6, 30, 0, 59))

    def test_cabecera_inesperada_para(self):
        ruta = self.dir / "mala.csv"
        ruta.write_text("Fecha,Hora\n2023.06.30,00:00:00\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            cv.leer(ruta)


if __name__ == "__main__":
    unittest.main()
