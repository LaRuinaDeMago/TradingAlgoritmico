"""Extrae de settings.xml (dentro de un .sqx) los elementos de resultados de WF y What If, para ver si tienen contenido.
Uso: python -I extraer_wf.py SQX"""
import sys
import xml.etree.ElementTree as ET
import zipfile

raiz = ET.fromstring(zipfile.ZipFile(sys.argv[1]).read("settings.xml"))
padres = {h: p for p in raiz.iter() for h in p}


def ruta(e):
    partes = []
    while e is not None:
        partes.append(e.tag)
        e = padres.get(e)
    return "/".join(reversed(partes))


for etiqueta in ("WalkForwardResult", "WalkForwardPeriod"):
    elementos = list(raiz.iter(etiqueta))
    print(f"== {etiqueta}: {len(elementos)} elementos")
    for e in elementos[:3]:
        print("   ruta:", ruta(e))
        print("   ", ET.tostring(e, encoding="unicode")[:700].replace("\n", " "))

print("== Resultados cuyo nombre o clave menciona CrossCheck_WhatIf o 'WF:'")
vistos = 0
for e in raiz.iter():
    valores = " ".join([e.tag, *e.attrib.values()])
    if "CrossCheck_WhatIf" in valores or "WF: " in valores:
        hijos = len(list(e))
        texto = ET.tostring(e, encoding="unicode")
        print(f"   {ruta(e)} {dict(list(e.attrib.items())[:4])} hijos={hijos} tamaño_xml={len(texto)}")
        vistos += 1
        if vistos >= 8:
            break
