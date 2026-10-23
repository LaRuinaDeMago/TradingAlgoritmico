"""Tests de la prueba de restauración de B25 (h0/configs/b25_restaurar.py), con un repositorio git de juguete, un
registro y una evidencia inventados. Controles negativos: un dato cambiado, una salida distinta y un clon con cambios
tienen que dar FALLIDA. Ejecutar desde la raíz: python -m unittest discover -s tests"""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h0" / "configs"))

import b25_restaurar as b25  # noqa: E402

SCRIPT = "import sys\nfrom pathlib import Path\nprint(sum(len(Path(a).read_bytes()) for a in sys.argv[1:]))\n"


def git(carpeta: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(carpeta), "-c", "user.name=t", "-c", "user.email=t@t", *args],
                          capture_output=True, text=True, check=True).stdout.strip()


class Montaje:
    """Repositorio con un script, dos datos fuera del repo, una entrada de registro y su evidencia."""

    def __init__(self, t: str, salida: bytes | None = None, con_hash_b: bool = True):
        raiz = Path(t)
        self.clon = raiz / "clon"
        self.clon.mkdir()
        (self.clon / "cuenta.py").write_bytes(SCRIPT.encode())  # bytes: write_text pondría CRLF en Windows
        git(self.clon, "init", "-q")
        git(self.clon, "add", "cuenta.py")
        git(self.clon, "commit", "-q", "-m", "x")
        commit = git(self.clon, "rev-parse", "HEAD")
        self.datos = raiz / "datos"
        self.datos.mkdir()
        a, b = self.datos / "a.csv", self.datos / "b.csv"
        a.write_bytes(b"12345")
        b.write_bytes(b"678")
        pa, pb = a.as_posix(), b.as_posix()
        datos = {pa: hashlib.sha256(b"12345").hexdigest(), "cuenta.py": hashlib.sha256(SCRIPT.encode()).hexdigest()}
        if con_hash_b:
            datos[pb] = hashlib.sha256(b"678").hexdigest()
        self.evidencias = raiz / "evidencias"
        self.evidencias.mkdir()
        salida = b"8" + (b"\r\n" if sys.platform == "win32" else b"\n") if salida is None else salida
        (self.evidencias / "ev.txt").write_bytes(b"# cabecera\n=== STDOUT ===\n" + salida + b"\n=== STDERR ===\n")
        entrada = {"n": 7, "codigo": {"commit": commit}, "comando": f"python -I cuenta.py {pa} {pb}",
                   "datos": datos, "resultado": {"evidencia": "h0/evidencias/ev.txt"}}
        self.registro = raiz / "registro.jsonl"
        self.registro.write_text(json.dumps({"n": 6}) + "\n" + json.dumps(entrada) + "\n", encoding="utf-8")

    def args(self, *cambios: str) -> list[str]:
        return [str(self.registro), "7", str(self.clon), str(self.evidencias), *cambios]


class TestRestaurar(unittest.TestCase):
    def test_restauracion_ok(self):
        with tempfile.TemporaryDirectory() as t:
            m = Montaje(t)
            self.assertEqual(b25.main(m.args()), 0)

    def test_control_negativo_dato_cambiado(self):
        with tempfile.TemporaryDirectory() as t:
            m = Montaje(t)
            (m.datos / "a.csv").write_bytes(b"12346")
            r = b25.restaurar(m.registro, 7, m.clon, m.evidencias, [])
            self.assertEqual(r["hashes"][(m.datos / "a.csv").as_posix()], "distinto")
            self.assertEqual(b25.main(m.args()), 1)

    def test_control_negativo_salida_distinta(self):
        with tempfile.TemporaryDirectory() as t:
            m = Montaje(t, salida=b"9\n")
            self.assertFalse(b25.restaurar(m.registro, 7, m.clon, m.evidencias, [])["salida_igual"])
            self.assertEqual(b25.main(m.args()), 1)

    def test_control_negativo_clon_con_cambios(self):
        with tempfile.TemporaryDirectory() as t:
            m = Montaje(t)
            (m.clon / "otro.txt").write_text("x", encoding="utf-8")
            self.assertEqual(b25.main(m.args()), 1)

    def test_detecta_archivos_sin_hash(self):
        with tempfile.TemporaryDirectory() as t:
            m = Montaje(t, con_hash_b=False)
            r = b25.restaurar(m.registro, 7, m.clon, m.evidencias, [])
            self.assertEqual(r["sin_hash"], [(m.datos / "b.csv").as_posix()])

    def test_datos_desde_una_copia_en_otra_ruta(self):
        with tempfile.TemporaryDirectory() as t:
            m = Montaje(t)
            copia = Path(t) / "copia_externa"
            m.datos.rename(copia)
            self.assertEqual(b25.main(m.args()), 1)  # sin el cambio de prefijo no encuentra los datos
            self.assertEqual(b25.main(m.args(f"{m.datos.as_posix()}={copia.as_posix()}")), 0)


if __name__ == "__main__":
    unittest.main()
