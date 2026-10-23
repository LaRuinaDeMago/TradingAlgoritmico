"""B21, diagnóstico (sin criterio): ¿cómo cambian los bloques SQStats de settings.xml entre dos versiones de una
estrategia? Distingue tres explicaciones: mismo contenido reordenado (mismos bytes en otro orden), cambio de tipo de
dato (cambia la longitud o aparecen marcadores de tipo distintos) o valores distintos.

Uso: python -I h0/configs/b21_diag_sqstats.py ESTRATEGIA_A.sqx ESTRATEGIA_B.sqx
"""

import base64
import collections
import re
import sys
import zipfile

PATRON = re.compile(r'<SQStats version="(\d+)" e="b64">([A-Za-z0-9+/=]+)<')


def bloques(ruta: str) -> list[tuple[str, bytes]]:
    x = zipfile.ZipFile(ruta).read("settings.xml").decode("utf-8")
    return [(v, base64.b64decode(b)) for v, b in PATRON.findall(x)]


a, b = bloques(sys.argv[1]), bloques(sys.argv[2])
print(f"bloques SQStats: {len(a)} y {len(b)}")
for i, ((va, xa), (vb, xb)) in enumerate(zip(a, b)):
    distintos = sum(1 for p, q in zip(xa, xb) if p != q)
    mismos_bytes = collections.Counter(xa) == collections.Counter(xb)
    print(f"  bloque {i}: versión {va}/{vb}; bytes {len(xa)}/{len(xb)}; posiciones distintas {distintos}; "
          f"mismos bytes en otro orden: {mismos_bytes}")
    if distintos and i == 0:
        j = next(k for k, (p, q) in enumerate(zip(xa, xb)) if p != q)
        print(f"    primera diferencia en el byte {j}:")
        print(f"    A: {xa[max(0, j - 24):j + 40].hex(' ')}")
        print(f"    B: {xb[max(0, j - 24):j + 40].hex(' ')}")
        print(f"    A texto: {xa[max(0, j - 24):j + 40]!r}")
        print(f"    B texto: {xb[max(0, j - 24):j + 40]!r}")
