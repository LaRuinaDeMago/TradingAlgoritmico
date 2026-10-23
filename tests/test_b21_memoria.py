"""Tests del cambio de memoria de sqcli (h0/configs/b21_memoria.py, decisión A24): copia del original, una sola línea
añadida, nada sobrescrito, y restauración exacta. Ejecutar desde la raíz: python -m unittest discover -s tests"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b21_memoria as mem  # noqa: E402

ORIGINAL = b"option -XX:+UseParallelGC\r\noption -Xms4g\r\noption -Dsqx.console=true\r\n"


def preparar(t: str, contenido: bytes = ORIGINAL) -> tuple[Path, Path]:
    config = Path(t) / "sqcli.config"
    config.write_bytes(contenido)
    return config, Path(t) / "copia" / "sqcli.config.original"


class TestMemoria(unittest.TestCase):
    def test_anade_una_linea_y_guarda_el_original(self):
        with tempfile.TemporaryDirectory() as t:
            config, copia = preparar(t)
            mem.subir(config, copia, "8g")
            self.assertEqual(copia.read_bytes(), ORIGINAL)
            self.assertEqual(config.read_bytes(), ORIGINAL + b"option -Xmx8g\r\n")

    def test_respeta_un_final_sin_salto(self):
        with tempfile.TemporaryDirectory() as t:
            config, copia = preparar(t, ORIGINAL.rstrip(b"\r\n"))
            mem.subir(config, copia, "8g")
            self.assertEqual(config.read_bytes(), ORIGINAL + b"option -Xmx8g\r\n")

    def test_usa_el_salto_de_linea_del_archivo(self):
        with tempfile.TemporaryDirectory() as t:
            lf = ORIGINAL.replace(b"\r\n", b"\n")
            config, copia = preparar(t, lf)
            mem.subir(config, copia, "8g")
            self.assertEqual(config.read_bytes(), lf + b"option -Xmx8g\n")

    def test_control_negativo_ya_tiene_xmx(self):
        with tempfile.TemporaryDirectory() as t:
            config, copia = preparar(t, ORIGINAL + b"option -Xmx2g\r\n")
            with self.assertRaises(SystemExit):
                mem.subir(config, copia, "8g")
            self.assertFalse(copia.exists())

    def test_control_negativo_no_sobrescribe_la_copia(self):
        with tempfile.TemporaryDirectory() as t:
            config, copia = preparar(t)
            copia.parent.mkdir()
            copia.write_bytes(b"otra")
            with self.assertRaises(SystemExit):
                mem.subir(config, copia, "8g")
            self.assertEqual(config.read_bytes(), ORIGINAL)

    def test_restaurar_deja_el_original_exacto(self):
        with tempfile.TemporaryDirectory() as t:
            config, copia = preparar(t)
            mem.subir(config, copia, "8g")
            mem.restaurar(config, copia)
            self.assertEqual(config.read_bytes(), ORIGINAL)


if __name__ == "__main__":
    unittest.main()
