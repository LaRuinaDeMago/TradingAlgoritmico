"""Compara dos carpetas de CSV de operaciones exportadas por `sqcli -tools action=orderstocsv` (tarea 4 de H0).

Uso:  python -I h0/configs/comparar_operaciones.py CARPETA_A CARPETA_B

Para cada estrategia presente en ambas: primero byte a byte; si difiere, fila a fila (separador ';'),
indicando cuántas operaciones tiene cada lado y la primera fila distinta. Devuelve 0 solo si todas
las estrategias de A están en B y son idénticas byte a byte.
"""

import csv
import io
import sys
from pathlib import Path


def filas(contenido: bytes) -> list[list[str]]:
    return list(csv.reader(io.StringIO(contenido.decode("utf-8-sig")), delimiter=";"))


def main(a: str, b: str) -> int:
    archivos_a = {p.name: p for p in Path(a).glob("*.csv")}
    archivos_b = {p.name: p for p in Path(b).glob("*.csv")}
    faltan = sorted(set(archivos_a) ^ set(archivos_b))
    identicas = 0
    for nombre in sorted(set(archivos_a) & set(archivos_b)):
        ca, cb = archivos_a[nombre].read_bytes(), archivos_b[nombre].read_bytes()
        if ca == cb:
            identicas += 1
            print(f"IDÉNTICA  {nombre}: {len(filas(ca)) - 1} operaciones")
            continue
        fa, fb = filas(ca), filas(cb)
        primera = next((i for i, (x, y) in enumerate(zip(fa, fb)) if x != y), min(len(fa), len(fb)))
        print(f"DISTINTA  {nombre}: {len(fa) - 1} frente a {len(fb) - 1} operaciones; primera fila distinta: {primera}")
        if primera < min(len(fa), len(fb)):
            print(f"   A: {fa[primera]}")
            print(f"   B: {fb[primera]}")
    print(f"Resumen: {identicas} idénticas de {len(set(archivos_a) & set(archivos_b))} comparadas; "
          f"solo en una carpeta: {faltan or 'ninguna'}")
    return 0 if identicas == len(archivos_a) and not faltan else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
