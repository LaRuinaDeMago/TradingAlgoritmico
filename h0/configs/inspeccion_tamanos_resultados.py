"""Para cada .sqx de una carpeta: tamaño total y número de archivos por carpeta de resultados (Results/<x>/...).
Uso: python -I tamanos_resultados.py CARPETA"""
import collections
import sys
import zipfile
from pathlib import Path

total = collections.defaultdict(lambda: [0, 0, 0])  # carpeta -> [archivos, bytes, estrategias con >0 bytes]
for f in sorted(Path(sys.argv[1]).iterdir()):
    if f.suffix != ".sqx":
        continue
    por_carpeta = collections.defaultdict(int)
    for i in zipfile.ZipFile(f).infolist():
        if i.filename.startswith("Results/"):
            carpeta = i.filename.split("/")[1]
            por_carpeta[carpeta] += i.file_size
            total[carpeta][0] += 1
            total[carpeta][1] += i.file_size
    for carpeta, b in por_carpeta.items():
        total[carpeta][2] += b > 0
    print(f"{f.stem:14s} " + " | ".join(f"{k}: {v} B" for k, v in sorted(por_carpeta.items())))
print("\nResumen por carpeta de resultados (archivos, bytes, estrategias con contenido):")
for k, (n, b, con) in sorted(total.items()):
    print(f"  {k:40s} {n:5d} archivos {b:10d} bytes  {con}/10 con contenido")
