"""Tarea 2: ¿los resultados de What If y WF tienen contenido real? Tamaños dentro de los .sqx y columnas del CSV.
Uso: python -I inspeccionar_t2.py CARPETA_SQX CSV_BANCO"""
import csv
import sys
import zipfile
from pathlib import Path

carpeta, csv_banco = Path(sys.argv[1]), Path(sys.argv[2])
print("Tamaño (bytes) de los resultados de cada comprobación:")
for f in sorted(carpeta.iterdir()):
    if f.suffix != ".sqx":
        continue
    z = zipfile.ZipFile(f)
    tam = {i.filename.split("/")[1]: i.file_size for i in z.infolist()
           if i.filename.startswith("Results/") and i.filename.endswith("dailyEquity.bin")}
    mc = [i.file_size for i in z.infolist() if "MonteCarloManipulation_Results.xml" in i.filename]
    print(f"  {f.stem:14s} main={tam.get('Main: USDCHF_M1_dukas_LOM_H1')} whatif={tam.get('CrossCheck_WhatIf')} "
          f"wf={tam.get('WF: 10 runs : 20 % OOS')} mc_xml={mc}")

filas = list(csv.reader(open(csv_banco, encoding="utf-8-sig"), delimiter=";"))
cab = filas[0]
print(f"\nCSV del banco: {len(cab)} columnas, {len(filas) - 1} estrategias")
for i, c in enumerate(cab):
    if any(k in c for k in ("WF", "Walk", "What", "MC", "Monte", "OOS")):
        print(f"  [{i}] {c}: {[f[i] for f in filas[1:4]]}")
