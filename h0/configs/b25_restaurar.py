"""B25 (memoria experimental): prueba de restauración de una entrada del registro.

Rehace el comando de una entrada desde un **clon limpio** en el commit registrado, con los archivos de entrada donde
estén (su sitio original o una copia de seguridad, cambiando el prefijo de la ruta), y comprueba:
  1. que el clon está en el commit registrado y sin cambios;
  2. el SHA-256 de cada archivo de entrada que tiene hash en el registro;
  3. qué archivos lee el comando **sin** hash registrado (agujeros de la memoria experimental);
  4. que la salida es **byte a byte** la guardada en la evidencia (el ejecutor guarda los bytes tal cual).

Uso (desde la raíz del repositorio, por el ejecutor con registro):
  python -I h0/configs/b25_restaurar.py REGISTRO N CLON EVIDENCIAS [ORIGEN=DESTINO ...]
Sale con 0 solo si 1, 2 y 4 se cumplen; los agujeros de 3 se informan siempre.
"""

import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path

INICIO, FIN = b"\n=== STDOUT ===\n", b"\n=== STDERR ===\n"


def leer_entrada(registro: str | Path, n: int) -> dict:
    for linea in Path(registro).read_text(encoding="utf-8").splitlines():
        if linea.strip():
            e = json.loads(linea)
            if e.get("n") == n:
                return e
    sys.exit(f"PARADA: no hay entrada n.º {n} en {registro}")


def salida_registrada(evidencia: str | Path) -> bytes:
    datos = Path(evidencia).read_bytes()
    i = datos.find(INICIO)
    j = datos.find(FIN, i + len(INICIO))
    if i < 0 or j < 0:
        sys.exit(f"PARADA: {evidencia} no tiene las marcas de STDOUT y STDERR del ejecutor")
    return datos[i + len(INICIO):j]


def remapear(ruta: str, cambios: list[tuple[str, str]]) -> str:
    for origen, destino in cambios:
        if ruta.startswith(origen):
            return destino + ruta[len(origen):]
    return ruta


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def resolver(ruta: str, clon: Path, cambios: list[tuple[str, str]]) -> Path:
    p = Path(remapear(ruta, cambios))
    return p if p.is_absolute() else clon / p


def restaurar(registro, n: int, clon, evidencias, cambios: list[tuple[str, str]]) -> dict:
    clon = Path(clon)
    e = leer_entrada(registro, n)
    commit = subprocess.run(["git", "-C", str(clon), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cambios_git = subprocess.run(["git", "-C", str(clon), "status", "--porcelain"], capture_output=True,
                                 text=True).stdout.strip()
    hashes = {}
    for ruta, esperado in sorted(e["datos"].items()):
        p = resolver(ruta, clon, cambios)
        hashes[ruta] = "falta" if not p.is_file() else ("igual" if sha256(p) == esperado else "distinto")
    fichas = shlex.split(e["comando"])
    con_hash = set(e["datos"])
    sin_hash = sorted(t for t in fichas[1:] if "/" in t and Path(t).suffix and t not in con_hash)
    proceso = subprocess.run([remapear(t, cambios) for t in fichas], cwd=clon, capture_output=True,
                             stdin=subprocess.DEVNULL)
    registrada = salida_registrada(Path(evidencias) / Path(e["resultado"]["evidencia"]).name)
    return {"n": n, "commit_registrado": e["codigo"]["commit"], "commit_clon": commit,
            "clon_limpio": cambios_git == "", "hashes": hashes, "sin_hash": sin_hash,
            "codigo_salida": proceso.returncode, "salida_igual": proceso.stdout == registrada,
            "bytes": [len(registrada), len(proceso.stdout)]}


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(__doc__)
        return 2
    cambios = [tuple(c.split("=", 1)) for c in argv[4:]]
    r = restaurar(argv[0], int(argv[1]), argv[2], argv[3], cambios)
    commit_ok = r["commit_clon"] == r["commit_registrado"] and r["clon_limpio"]
    hashes_ok = all(v == "igual" for v in r["hashes"].values())
    print(f"entrada n.º {r['n']}: commit registrado {r['commit_registrado'][:10]}, clon {r['commit_clon'][:10]}, "
          f"clon limpio {r['clon_limpio']} -> {'OK' if commit_ok else 'FALLO'}")
    for ruta, estado in r["hashes"].items():
        print(f"  hash {estado}: {ruta}")
    print(f"archivos leídos SIN hash registrado: {len(r['sin_hash'])}")
    for ruta in r["sin_hash"]:
        print(f"  sin hash: {ruta}")
    print(f"salida: {r['bytes'][0]} bytes registrados, {r['bytes'][1]} ahora, código {r['codigo_salida']}; "
          f"byte a byte igual: {r['salida_igual']}")
    ok = commit_ok and hashes_ok and r["salida_igual"] and r["codigo_salida"] == 0
    print("RESTAURACIÓN " + ("OK" if ok else "FALLIDA"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
