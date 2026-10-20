"""Busca dónde guarda SQX los resultados de walk-forward / What If dentro de un .sqx.
Uso: python -I buscar_wf.py SQX_SIN SQX_WFO SQX_WFM"""
import re
import sys
import zipfile

etiquetas = ("sin comprobaciones", "WFO + WhatIf + MC", "WF Matrix")
zips = [zipfile.ZipFile(p) for p in sys.argv[1:4]]
nombres = sorted(set().union(*(z.namelist() for z in zips)))
print("Tamaño de las entradas que no son Results/:")
for n in nombres:
    if n.startswith("Results/"):
        continue
    tam = [z.getinfo(n).file_size if n in z.namelist() else None for z in zips]
    print(f"  {n:28s} " + "  ".join(f"{e}={t}" for e, t in zip(etiquetas, tam)))

print("\nMenciones en strategy_Portfolio.xml y settings.xml:")
patron = re.compile(rb"(WalkForward|WhatIf|CrossCheck_|WF: |Trial|trial)[^<>\"]{0,60}")
for e, z in zip(etiquetas, zips):
    for n in ("strategy_Portfolio.xml", "settings.xml"):
        d = z.read(n)
        hallazgos = sorted({m.group(0)[:70] for m in patron.finditer(d)})
        print(f"  [{e}] {n}: {len(hallazgos)} distintas")
        for h in hallazgos[:12]:
            print("      ", h.decode("utf-8", "replace"))
