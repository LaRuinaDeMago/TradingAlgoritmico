"""Lista las entradas de los .sqx (zip) de una carpeta y resume las carpetas de resultados.
Uso: python -I inspeccionar_sqx.py CARPETA_ANTES CARPETA_DESPUES NOMBRE_EJEMPLO"""
import collections
import sys
import zipfile
from pathlib import Path

antes, despues, ejemplo = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
for etiqueta, carpeta in (("ANTES (tarea 4, sin comprobaciones)", antes), ("DESPUÉS (tarea 2, con comprobaciones)", despues)):
    print(f"{ejemplo} - {etiqueta}:")
    for n in sorted(zipfile.ZipFile(carpeta / ejemplo).namelist()):
        print("   ", n)

resumen = collections.Counter()
for f in sorted(despues.iterdir()):
    if f.suffix == ".sqx":
        for n in zipfile.ZipFile(f).namelist():
            if n.startswith("Results/"):
                resumen[n.split("/")[1]] += 1
print("Carpetas de resultados en todas las estrategias de DESPUÉS:")
for k, v in sorted(resumen.items()):
    print(f"   {v:3d} entradas  {k}")
