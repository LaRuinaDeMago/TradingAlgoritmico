"""Tests del núcleo. Ejecutar desde la raíz: python -m unittest discover -s tests"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from lab import registro  # noqa: E402
from lab.ejecutar import ejecutar  # noqa: E402
from lab.hashing import sha256_archivo, sha256_carpeta  # noqa: E402
from lab.rutas import AccesoSelladoError, es_sellada  # noqa: E402


class ConRaizTemporal(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name).resolve()
        (self.raiz / "data" / "raw").mkdir(parents=True)
        (self.raiz / "data" / "sealed").mkdir(parents=True)
        (self.raiz / "data" / "raw" / "precios.csv").write_text("t,c\n1,10\n")
        (self.raiz / "data" / "sealed" / "final.csv").write_text("secreto\n")

    def tearDown(self):
        self._tmp.cleanup()

    def registrar(self, **extra):
        args = dict(descripcion="prueba", comando="echo", version_sqx="N/A",
                    estado="OK", resultado={"x": 1}, raiz=self.raiz)
        args.update(extra)
        return registro.registrar(**args)


class TestSellado(ConRaizTemporal):
    def test_detecta_sellada_y_sus_ancestros(self):
        self.assertTrue(es_sellada(self.raiz / "data" / "sealed" / "final.csv", self.raiz))
        self.assertTrue(es_sellada(self.raiz / "data", self.raiz))
        self.assertTrue(es_sellada(self.raiz, self.raiz))
        self.assertFalse(es_sellada(self.raiz / "data" / "raw", self.raiz))

    def test_hash_se_niega_a_tocar_sellados(self):
        with self.assertRaises(AccesoSelladoError):
            sha256_archivo(self.raiz / "data" / "sealed" / "final.csv", self.raiz)
        with self.assertRaises(AccesoSelladoError):
            sha256_carpeta(self.raiz / "data", self.raiz)

    def test_ejecutar_se_niega_con_ruta_sellada(self):
        with self.assertRaises(AccesoSelladoError):
            ejecutar(["cat", "data\\Sealed\\final.csv"], nombre="x", version_sqx="N/A", raiz=self.raiz)
        self.assertEqual(registro.leer(self.raiz), [])


class TestHash(ConRaizTemporal):
    def test_hash_carpeta_estable_y_sensible(self):
        carpeta = self.raiz / "data" / "raw"
        h1 = sha256_carpeta(carpeta, self.raiz)
        self.assertEqual(h1, sha256_carpeta(carpeta, self.raiz))
        (carpeta / "precios.csv").write_text("t,c\n1,11\n")
        self.assertNotEqual(h1, sha256_carpeta(carpeta, self.raiz))


class TestRegistro(ConRaizTemporal):
    def test_cadena_y_campos(self):
        datos = str(self.raiz / "data" / "raw" / "precios.csv")
        e1 = self.registrar(datos=[datos], semilla=7, costes={"spread": 0.3})
        e2 = self.registrar(estado="FALLIDO")
        self.assertEqual((e1["n"], e2["n"]), (1, 2))
        self.assertEqual(e2["hash_anterior"], e1["hash"])
        self.assertEqual(e1["datos"][Path(datos).as_posix()], sha256_archivo(datos, self.raiz))
        for campo in ("fecha_utc", "comando", "version_sqx", "codigo", "semilla", "costes", "resultado"):
            self.assertIn(campo, e1)
        self.assertEqual(registro.verificar(self.raiz), [])

    def test_detecta_alteracion_y_borrado(self):
        for _ in range(3):
            self.registrar()
        ruta = registro.archivo_registro(self.raiz)
        lineas = ruta.read_text(encoding="utf-8").splitlines()

        alterada = json.loads(lineas[1])
        alterada["resultado"] = {"x": 999}
        ruta.write_text("\n".join([lineas[0], json.dumps(alterada), lineas[2]]) + "\n", encoding="utf-8")
        self.assertTrue(registro.verificar(self.raiz))
        with self.assertRaises(RuntimeError):
            self.registrar()

        ruta.write_text("\n".join([lineas[0], lineas[2]]) + "\n", encoding="utf-8")
        self.assertTrue(registro.verificar(self.raiz))

    def test_estado_invalido(self):
        with self.assertRaises(ValueError):
            self.registrar(estado="BUENISIMO")


class TestEjecutar(ConRaizTemporal):
    def test_ok_guarda_evidencia(self):
        e = ejecutar([sys.executable, "-c", "print('hola sqx')"], nombre="eco",
                     version_sqx="N/A", raiz=self.raiz)
        self.assertEqual(e["estado"], "OK")
        evidencia = self.raiz / e["resultado"]["evidencia"]
        self.assertIn("hola sqx", evidencia.read_text(encoding="utf-8"))
        self.assertEqual(e["resultado"]["sha256_evidencia"], sha256_archivo(evidencia, self.raiz))

    def test_fallos_tambien_se_registran(self):
        e1 = ejecutar([sys.executable, "-c", "import sys; sys.exit(3)"], nombre="falla",
                      version_sqx="N/A", raiz=self.raiz)
        e2 = ejecutar(["no_existe_este_programa_xyz"], nombre="inexistente",
                      version_sqx="N/A", raiz=self.raiz)
        e3 = ejecutar([sys.executable, "-c", "import time; time.sleep(5)"], nombre="lento",
                      version_sqx="N/A", timeout=0.5, raiz=self.raiz)
        self.assertEqual([e["estado"] for e in (e1, e2, e3)], ["FALLIDO"] * 3)
        self.assertEqual(e1["resultado"]["codigo_salida"], 3)
        self.assertIn("tiempo máximo", e3["resultado"]["incidencia"])
        self.assertEqual(len(registro.leer(self.raiz)), 3)

    def test_cli(self):
        env = dict(os.environ, LAB_RAIZ=str(self.raiz), PYTHONPATH=str(SRC))
        r = subprocess.run(
            [sys.executable, "-m", "lab", "ejecutar", "--nombre", "cli", "--version-sqx", "N/A",
             "--semilla", "1", "--", sys.executable, "-c", "print(42)"],
            capture_output=True, text=True, env=env,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        r = subprocess.run([sys.executable, "-m", "lab", "verificar"],
                           capture_output=True, text=True, env=env)
        self.assertIn("1 entradas", r.stdout)

    def test_su_propia_evidencia_no_ensucia_el_codigo(self):
        git = ["git", "-c", "user.name=prueba", "-c", "user.email=prueba@example.invalid"]
        subprocess.run(["git", "init", "-q"], cwd=self.raiz, check=True)
        subprocess.run(git + ["add", "."], cwd=self.raiz, check=True)
        subprocess.run(git + ["commit", "-qm", "inicial"], cwd=self.raiz, check=True)
        e = ejecutar([sys.executable, "-c", "print(1)"], nombre="limpio", version_sqx="N/A", raiz=self.raiz)
        self.assertFalse(e["codigo"]["sucio"])
        subprocess.run(git + ["add", "."], cwd=self.raiz, check=True)
        subprocess.run(git + ["commit", "-qm", "evidencia"], cwd=self.raiz, check=True)
        (self.raiz / "data" / "raw" / "precios.csv").write_text("t,c\n1,99\n")
        e = ejecutar([sys.executable, "-c", "print(1)"], nombre="sucio", version_sqx="N/A", raiz=self.raiz)
        self.assertTrue(e["codigo"]["sucio"])


class TestPrivacidad(ConRaizTemporal):
    SALIDA = "print('Hardware ID: CAC3C722FAFD'); print('x -- Licenser -- L: 01234567'); print('a@b.com')"

    def test_ejecutar_redacta_y_guarda_el_original_aparte(self):
        script = self.raiz / "imprime.py"
        script.write_text(self.SALIDA)
        e = ejecutar([sys.executable, str(script)], nombre="priv", version_sqx="N/A", raiz=self.raiz)
        r = e["resultado"]
        publica = (self.raiz / r["evidencia"]).read_bytes()
        privada = (self.raiz / r["evidencia_privada"]).read_bytes()
        self.assertNotIn(b"CAC3C722FAFD", publica)
        self.assertNotIn(b"01234567", publica)
        self.assertNotIn(b"a@b.com", publica)
        self.assertIn(b"[REDACTADO:hardware_id]", publica)
        self.assertIn(b"CAC3C722FAFD", privada)
        self.assertEqual(r["redacciones"], {"hardware_id": 1, "licencia": 1, "email": 1})
        self.assertTrue(r["evidencia_privada"].startswith("h0/evidencias_privadas/"))
        self.assertEqual(r["sha256_evidencia_privada"], sha256_archivo(self.raiz / r["evidencia_privada"], self.raiz))

    def test_se_niega_si_el_comando_lleva_datos_privados(self):
        with self.assertRaises(ValueError):
            ejecutar([sys.executable, "-c", self.SALIDA], nombre="x", version_sqx="N/A", raiz=self.raiz)
        self.assertEqual(registro.leer(self.raiz), [])

    def test_sin_datos_privados_no_hay_copia_privada(self):
        e = ejecutar([sys.executable, "-c", "print(1)"], nombre="limpia", version_sqx="N/A", raiz=self.raiz)
        self.assertEqual(e["resultado"]["redacciones"], {})
        self.assertIsNone(e["resultado"]["evidencia_privada"])
        self.assertFalse((self.raiz / "h0" / "evidencias_privadas").exists())

    def test_redactar_evidencia_ya_escrita(self):
        from lab.ejecutar import redactar_evidencia
        vieja = self.raiz / "h0" / "evidencias" / "vieja.txt"
        vieja.parent.mkdir(parents=True)
        vieja.write_bytes(b"Hardware ID: ABCDEF12\r\nresto\r\n")
        e = redactar_evidencia("h0/evidencias/vieja.txt", version_sqx="N/A", raiz=self.raiz)
        r = e["resultado"]
        self.assertFalse(vieja.exists())
        self.assertEqual(r["evidencia"], "h0/evidencias/vieja.redactada.txt")
        self.assertEqual((self.raiz / r["evidencia"]).read_bytes(), b"Hardware ID: [REDACTADO:hardware_id]\r\nresto\r\n")
        self.assertEqual((self.raiz / r["evidencia_privada"]).read_bytes(), b"Hardware ID: ABCDEF12\r\nresto\r\n")
        with self.assertRaises(ValueError):
            redactar_evidencia("h0/evidencias/vieja.redactada.txt", version_sqx="N/A", raiz=self.raiz)


class TestGuardian(unittest.TestCase):
    def test_autotest_del_hook(self):
        hook = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "guardian.py"
        r = subprocess.run([sys.executable, str(hook), "--autotest"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_hook_bloquea_por_stdin(self):
        hook = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "guardian.py"
        evento = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "data/sealed/a.csv"}})
        env = {k: v for k, v in os.environ.items() if k != "LAB_PROTOCOLO_SELLADO"}
        r = subprocess.run([sys.executable, str(hook)], input=evento, capture_output=True,
                           text=True, env=env)
        self.assertEqual(r.returncode, 2)
        self.assertIn("SELLADOS", r.stderr)


if __name__ == "__main__":
    unittest.main()
