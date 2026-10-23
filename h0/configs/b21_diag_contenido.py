"""B21-bis, diagnóstico de B2c (sin criterio): ¿qué archivo interno de los .sqx cambia entre dos carpetas, y en qué?

Uso: python -I h0/configs/b21_diag_contenido.py CARPETA_A CARPETA_B
Cuenta, para cada nombre de archivo interno, en cuántas estrategias difiere, y muestra las primeras diferencias de
texto de una estrategia de ejemplo.
"""

import collections
import difflib
import hashlib
import sys
import zipfile
from pathlib import Path


def entradas(ruta: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(ruta) as z:
        return {n: z.read(n) for n in z.namelist()}


def tipo(nombre: str) -> str:
    """Agrupa las rutas internas que llevan el nombre del símbolo (Results/Main: X/dailyEquity.bin)."""
    return nombre.split("/")[-1] if "/" in nombre else nombre


a, b = Path(sys.argv[1]), Path(sys.argv[2])
nombres = sorted(p.name for p in a.glob("*.sqx") if (b / p.name).exists())
difieren = collections.Counter()
solo_a, solo_b = collections.Counter(), collections.Counter()
ejemplo = None
for n in nombres:
    ea, eb = entradas(a / n), entradas(b / n)
    for k in set(ea) | set(eb):
        if k not in eb:
            solo_a[tipo(k)] += 1
        elif k not in ea:
            solo_b[tipo(k)] += 1
        elif hashlib.sha256(ea[k]).digest() != hashlib.sha256(eb[k]).digest():
            difieren[tipo(k)] += 1
            if ejemplo is None and k.endswith((".xml", ".txt", ".MF")):
                ejemplo = (n, k, ea[k], eb[k])
print(f"estrategias comparadas: {len(nombres)}")
print(f"archivos internos que difieren (nombre: n.º de estrategias): {dict(difieren)}")
print(f"solo en A: {dict(solo_a)}; solo en B: {dict(solo_b)}")
if ejemplo:
    n, k, xa, xb = ejemplo
    print(f"== ejemplo: {n} / {k} ({len(xa)} y {len(xb)} bytes)")
    la = xa.decode("utf-8", "replace").splitlines()
    lb = xb.decode("utf-8", "replace").splitlines()
    diff = [l for l in difflib.unified_diff(la, lb, "A", "B", n=0, lineterm="") if not l.startswith(("---", "+++"))]
    print(f"líneas distintas: {sum(1 for l in diff if l[:1] in '+-')}")
    # Las líneas son muy largas (un XML por línea): se muestran los tramos distintos con su contexto.
    sa, sb = xa.decode("utf-8", "replace"), xb.decode("utf-8", "replace")
    tramos = [op for op in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes() if op[0] != "equal"]
    print(f"tramos distintos: {len(tramos)}")
    for _, i1, i2, j1, j2 in tramos[:12]:
        print(f"  A[{i1}:{i2}] {sa[max(0, i1 - 120):i2 + 40]!r}")
        print(f"  B[{j1}:{j2}] {sb[max(0, j1 - 120):j2 + 40]!r}")
