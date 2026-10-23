"""Tests del archivo de bancos de B21 (h0/configs/b21_archivo.py), con controles negativos: cada comprobación tiene
que fallar cuando la copia está mal. Ejecutar desde la raíz: python -m unittest discover -s tests"""

import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b21_archivo as ar  # noqa: E402


def banco(carpeta: Path, archivos: dict[str, bytes]) -> Path:
    carpeta.mkdir(parents=True)
    for nombre, contenido in archivos.items():
        (carpeta / nombre).write_bytes(contenido)
    return carpeta


EJEMPLO = {"Strategy 0.0(1).sqx": b"uno", "Strategy 0.0(2).sqx": b"dos", "Strategy 1.5.sqx": b"tres"}


class TestManifiesto(unittest.TestCase):
    def test_cuenta_tamanos_y_hashes(self):
        with tempfile.TemporaryDirectory() as t:
            m = ar.manifiesto(banco(Path(t) / "b", EJEMPLO))
            self.assertEqual(len(m), 3)
            self.assertEqual(m["Strategy 0.0(1).sqx"]["bytes"], 3)
            self.assertEqual(m["Strategy 0.0(1).sqx"]["sha256"], hashlib.sha256(b"uno").hexdigest())
            self.assertNotEqual(m["Strategy 0.0(1).sqx"]["sha256"], m["Strategy 0.0(2).sqx"]["sha256"])

    def test_solo_sqx(self):
        with tempfile.TemporaryDirectory() as t:
            m = ar.manifiesto(banco(Path(t) / "b", {**EJEMPLO, "notas.txt": b"x"}))
            self.assertEqual(len(m), 3)

    def test_se_para_con_subcarpetas(self):
        with tempfile.TemporaryDirectory() as t:
            b = banco(Path(t) / "b", EJEMPLO)
            (b / "sub").mkdir()
            with self.assertRaises(SystemExit):
                ar.manifiesto(b)


class TestComparar(unittest.TestCase):
    def test_iguales(self):
        with tempfile.TemporaryDirectory() as t:
            a = ar.manifiesto(banco(Path(t) / "a", EJEMPLO))
            b = ar.manifiesto(banco(Path(t) / "b", EJEMPLO))
            self.assertEqual(ar.comparar(a, b), {"faltan": [], "sobran": [], "distintos": []})

    def test_control_negativo_un_byte(self):
        with tempfile.TemporaryDirectory() as t:
            a = ar.manifiesto(banco(Path(t) / "a", EJEMPLO))
            b = ar.manifiesto(banco(Path(t) / "b", {**EJEMPLO, "Strategy 1.5.sqx": b"treS"}))
            self.assertEqual(ar.comparar(a, b)["distintos"], ["Strategy 1.5.sqx"])

    def test_control_negativo_falta_y_sobra(self):
        with tempfile.TemporaryDirectory() as t:
            a = ar.manifiesto(banco(Path(t) / "a", EJEMPLO))
            otro = dict(EJEMPLO)
            del otro["Strategy 0.0(2).sqx"]
            otro["Strategy 9.sqx"] = b"nueva"
            r = ar.comparar(a, ar.manifiesto(banco(Path(t) / "b", otro)))
            self.assertEqual(r["faltan"], ["Strategy 0.0(2).sqx"])
            self.assertEqual(r["sobran"], ["Strategy 9.sqx"])

    def test_conservadas_admite_nuevas_pero_no_cambios(self):
        with tempfile.TemporaryDirectory() as t:
            a = ar.manifiesto(banco(Path(t) / "a", EJEMPLO))
            b = ar.manifiesto(banco(Path(t) / "b", {**EJEMPLO, "Strategy 9.sqx": b"nueva"}))
            self.assertTrue(ar.conservadas(a, b))
            c = ar.manifiesto(banco(Path(t) / "c", {**EJEMPLO, "Strategy 1.5.sqx": b"otro"}))
            self.assertFalse(ar.conservadas(a, c))


class TestCopiar(unittest.TestCase):
    def test_copia_identica(self):
        with tempfile.TemporaryDirectory() as t:
            origen = banco(Path(t) / "a", EJEMPLO)
            r = ar.copiar(origen, Path(t) / "copia")
            self.assertEqual(r["comparacion"], {"faltan": [], "sobran": [], "distintos": []})
            self.assertEqual(r["n"], 3)

    def test_no_sobrescribe(self):
        with tempfile.TemporaryDirectory() as t:
            origen = banco(Path(t) / "a", EJEMPLO)
            destino = banco(Path(t) / "copia", {"x.sqx": b"x"})
            with self.assertRaises(SystemExit):
                ar.copiar(origen, destino)
            self.assertEqual((destino / "x.sqx").read_bytes(), b"x")


def csv_banco(ruta: Path, filas: list[list[str]]) -> Path:
    cab = ['"Strategy Name"', '"Net profit (IS)"']
    ruta.write_text("\n".join([";".join(cab)] + [";".join(f'"{c}"' for c in f) for f in filas]) + "\n",
                    encoding="utf-8")
    return ruta


class TestCompararCsv(unittest.TestCase):
    def test_mismas_filas_en_otro_orden(self):
        with tempfile.TemporaryDirectory() as t:
            a = csv_banco(Path(t) / "a.csv", [["S1", "10"], ["S2", "20"], ["S2", "20"]])
            b = csv_banco(Path(t) / "b.csv", [["S2", "20"], ["S1", "10"], ["S2", "20"]])
            r = ar.comparar_csv(a, b)
            self.assertTrue(r["iguales"])
            self.assertEqual(r["filas"], [3, 3])

    def test_control_negativo_una_cifra(self):
        with tempfile.TemporaryDirectory() as t:
            a = csv_banco(Path(t) / "a.csv", [["S1", "10"], ["S2", "20"]])
            b = csv_banco(Path(t) / "b.csv", [["S1", "10"], ["S2", "21"]])
            self.assertFalse(ar.comparar_csv(a, b)["iguales"])

    def test_control_negativo_fila_duplicada(self):
        with tempfile.TemporaryDirectory() as t:
            a = csv_banco(Path(t) / "a.csv", [["S1", "10"], ["S2", "20"]])
            b = csv_banco(Path(t) / "b.csv", [["S1", "10"], ["S2", "20"], ["S2", "20"]])
            self.assertFalse(ar.comparar_csv(a, b)["iguales"])


def sqx(ruta: Path, entradas: dict[str, bytes], fecha=(2026, 10, 21, 18, 0, 0)) -> Path:
    """Un .sqx de prueba: zip con archivos internos y una fecha fija (SQX pone la del guardado)."""
    with zipfile.ZipFile(ruta, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for nombre, datos in entradas.items():
            z.writestr(zipfile.ZipInfo(nombre, date_time=fecha), datos)
    return ruta


ESTRATEGIA = {"settings.xml": b"<s/>", "orders.bin": b"\x01\x02", "version.txt": b"1"}


class TestContenido(unittest.TestCase):
    def test_misma_estrategia_guardada_otro_dia_es_igual(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "a").mkdir()
            (Path(t) / "b").mkdir()
            sqx(Path(t) / "a" / "S.sqx", ESTRATEGIA)
            sqx(Path(t) / "b" / "S.sqx", ESTRATEGIA, fecha=(2026, 10, 23, 0, 5, 56))
            self.assertNotEqual(ar.manifiesto(Path(t) / "a"), ar.manifiesto(Path(t) / "b"))  # el zip cambia
            self.assertEqual(ar.manifiesto_contenido(Path(t) / "a"), ar.manifiesto_contenido(Path(t) / "b"))

    def test_control_negativo_una_operacion_distinta(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "a").mkdir()
            (Path(t) / "b").mkdir()
            sqx(Path(t) / "a" / "S.sqx", ESTRATEGIA)
            sqx(Path(t) / "b" / "S.sqx", {**ESTRATEGIA, "orders.bin": b"\x01\x03"})
            r = ar.comparar(ar.manifiesto_contenido(Path(t) / "a"), ar.manifiesto_contenido(Path(t) / "b"))
            self.assertEqual(r["distintos"], ["S.sqx"])

    def test_control_negativo_archivo_interno_de_mas(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "a").mkdir()
            (Path(t) / "b").mkdir()
            sqx(Path(t) / "a" / "S.sqx", ESTRATEGIA)
            sqx(Path(t) / "b" / "S.sqx", {**ESTRATEGIA, "extra.xml": b""})
            self.assertFalse(ar.conservadas(ar.manifiesto_contenido(Path(t) / "a"),
                                            ar.manifiesto_contenido(Path(t) / "b")))


if __name__ == "__main__":
    unittest.main()
