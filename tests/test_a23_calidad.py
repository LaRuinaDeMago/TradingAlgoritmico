"""Errores sembrados para el analizador de calidad de A23 (h0/a23_plan_calidad_usdchf.md): cada defecto que el plan
quiere detectar se siembra en datos sintéticos limpios y el criterio que le toca tiene que fallar; los datos limpios
tienen que pasarlos todos. Ejecutar desde la raíz: python -m unittest discover -s tests"""

import sys
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import a23_calidad as ac  # noqa: E402


def semanas(inicio: date, n: int, quitar=(), planas=(), saltos=(), desplazar_h=0):
    """Velas M1 inventadas de lunes 00:00 a viernes 23:59 durante n semanas (valores de prueba, no de mercado).
    quitar: instantes que no se generan; planas: instantes con O=H=L=C; saltos: instantes con +5 % en el cierre."""
    filas, lunes = [], datetime.combine(inicio, datetime.min.time())
    for s in range(n):
        base = lunes + timedelta(weeks=s, hours=desplazar_h)
        for m in range(5 * 1440):
            t = base + timedelta(minutes=m)
            if t in quitar:
                continue
            p = 1.0 + 0.0001 * ((m % 50) - 25) / 25
            o, h, l, c = p, p + 0.0003, p - 0.0003, p + 0.0001
            if t in planas:
                o = h = l = c = p
            if t in saltos:
                c = p * 1.05
                h = max(h, c)
            filas.append([t.strftime("%Y.%m.%d"), t.strftime("%H:%M:%S"), f"{o:.5f}", f"{h:.5f}", f"{l:.5f}",
                          f"{c:.5f}", "100"])
    return filas


REF = (date(2024, 1, 1), date(2024, 12, 31))


def analizar(filas_2023, filas_2024=None):
    filas = filas_2023 + (filas_2024 if filas_2024 is not None else semanas(date(2024, 1, 1), 6))
    stats = ac.leer(filas, *REF)
    ref = stats.pop("ref")
    return {y: ac.criterios(s, ref) for y, s in stats.items()}, stats


class TestCalidad(unittest.TestCase):
    def test_limpio_pasa_todo(self):
        v, _ = analizar(semanas(date(2023, 1, 2), 6))
        self.assertTrue(v[2023]["pasa"], v[2023])
        self.assertTrue(v[2024]["pasa"], v[2024])
        self.assertEqual(ac.tramo_utilizable(v), [2023, 2024])

    def test_duplicado_y_desorden(self):
        f = semanas(date(2023, 1, 2), 6)
        f.insert(100, f[99])
        v, _ = analizar(f)
        self.assertFalse(v[2023]["C1_integridad"])

    def test_ohlc_incoherente(self):
        f = semanas(date(2023, 1, 2), 6)
        f[500][3] = "0.50000"  # high por debajo de open y close
        v, _ = analizar(f)
        self.assertFalse(v[2023]["C1_integridad"])

    def test_dia_entero_sin_datos_baja_la_cobertura(self):
        dia = datetime(2023, 1, 4)
        quitar = {dia + timedelta(minutes=m) for m in range(1440)}
        # 6 semanas sin un día: 29/30 = 0,967 de cobertura; no baja del 90 %; con 4 días quitados, sí
        quitar |= {datetime(2023, 1, d) + timedelta(minutes=m) for d in (10, 11, 12) for m in range(1440)}
        v, s = analizar(semanas(date(2023, 1, 2), 6, quitar=quitar))
        self.assertAlmostEqual(s[2023]["cobertura"], 26 / 30, places=3)
        self.assertFalse(v[2023]["C2_cobertura"])

    def test_huecos_dentro_de_la_semana(self):
        quitar = set()
        for s in range(6):
            for k in range(3):  # 3 huecos de 2 h por semana = 26 por 52 semanas... x6 semanas
                ini = datetime(2023, 1, 3 + 7 * s, 4 + 6 * k) if 3 + 7 * s <= 31 else datetime(2023, 2, 3 + 7 * s - 31, 4 + 6 * k)
                quitar |= {ini + timedelta(minutes=m) for m in range(120)}
        v, s = analizar(semanas(date(2023, 1, 2), 6, quitar=quitar))
        self.assertGreater(s[2023]["huecos_por_52_semanas"], 10)
        self.assertFalse(v[2023]["C3_huecos"])

    def test_velas_planas(self):
        planas = {datetime(2023, 1, 2) + timedelta(minutes=m) for m in range(0, 6 * 7 * 1440, 7)}
        v, s = analizar(semanas(date(2023, 1, 2), 6, planas=planas))
        self.assertGreater(s[2023]["planas"], 0.05)
        self.assertFalse(v[2023]["C4_planas"])

    def test_convencion_horaria_desplazada(self):
        v, s = analizar(semanas(date(2023, 1, 2), 6, desplazar_h=1))
        self.assertNotEqual(s[2023]["apertura_semanal"], s[2024]["apertura_semanal"])
        self.assertFalse(v[2023]["C5_convencion"])

    def test_salto_de_precio(self):
        v, s = analizar(semanas(date(2023, 1, 2), 6, saltos={datetime(2023, 1, 5, 10, 0)}))
        self.assertGreaterEqual(s[2023]["n_saltos"], 1)
        self.assertFalse(v[2023]["C6_saltos"])

    def test_salto_del_snb_es_excepcion(self):
        v, s = analizar(semanas(date(2015, 1, 12), 2, saltos={datetime(2015, 1, 15, 10, 30)}), )
        self.assertEqual(s[2015]["n_saltos"], 0)

    def test_tramo_se_corta_en_el_primer_año_malo_hacia_atras(self):
        v = {2020: {"pasa": True}, 2021: {"pasa": False}, 2022: {"pasa": True}, 2023: {"pasa": True}}
        self.assertEqual(ac.tramo_utilizable(v), [2022, 2023])
        self.assertIsNone(ac.tramo_utilizable({2023: {"pasa": False}}))


if __name__ == "__main__":
    unittest.main()
