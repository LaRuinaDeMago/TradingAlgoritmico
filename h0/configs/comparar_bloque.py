"""Compara un bloque de dos plantillas .cfx elemento a elemento (atributos y texto), ignorando espacios.
Uso: python -I comparar_bloque.py A.cfx B.cfx RUTA (p. ej. Settings/Data)"""
import sys
import xml.etree.ElementTree as ET
import zipfile


def plano(cfx, ruta):
    raiz = ET.fromstring(zipfile.ZipFile(cfx).read("config.xml"))
    bloque = raiz.find(ruta)
    salida = []

    def recorrer(e, p):
        salida.append((p, tuple(sorted(e.attrib.items())), (e.text or "").strip()))
        for i, h in enumerate(e):
            recorrer(h, f"{p}/{h.tag}[{i}]")

    recorrer(bloque, ruta)
    return salida


a, b = plano(sys.argv[1], sys.argv[3]), plano(sys.argv[2], sys.argv[3])
print("elementos", len(a), len(b))
for x, y in zip(a, b):
    if x != y:
        print(" A:", x)
        print(" B:", y)
print("diferencias:", sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b)))
