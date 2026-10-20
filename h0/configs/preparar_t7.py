"""Tarea 7 de H0: plantillas del experimento completo, con bancos propios para no mezclar con pruebas anteriores.

Uso:  python -I h0/configs/preparar_t7.py BUILDER_MINIMO.cfx RETESTER_MINIMO.cfx DESTINO_BUILDER.cfx DESTINO_RETESTER.cfx

Parte de las plantillas mínimas ya usadas y comprobadas (datos quemados de la decisión 0002) y cambia solo
los bancos: el Builder escribe sus resultados en H0_T7 (en vez de Results, que ya tiene 10 estrategias de la
tarea 3a: una parada "a las 10 estrategias" podría cumplirse sin generar nada) y el Retester lee y escribe en
H0_T7. Cada elemento tocado debe existir; si no, se detiene sin escribir nada.
"""

import sys
import xml.etree.ElementTree as ET
import zipfile

BANCO = "H0_T7"


def leer(cfx):
    with zipfile.ZipFile(cfx) as z:
        return ET.fromstring(z.read("config.xml"))


def escribir(raiz, destino):
    with zipfile.ZipFile(destino, "x", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("config.xml", ET.tostring(raiz, encoding="unicode"))


def main(builder, retester, destino_builder, destino_retester):
    b, r = leer(builder), leer(retester)
    for raiz, tipo in ((b, "Build"), (r, "Retest")):
        if raiz.get("type") != tipo or raiz.find("Settings/Data/Setups/Setup/Chart").get("symbol") != "USDCHF_M1_dukas":
            sys.exit(f"La plantilla {tipo} no es la mínima con los datos quemados")

    salidas = [d for d in b.findall("Settings/Databanks/Databank") if d.get("name") == "Output" and d.get("value") == "Results"]
    if len(salidas) != 1:
        sys.exit(f"Se esperaba un banco de salida 'Results' en el Builder y hay {len(salidas)}")
    print(f"Builder: banco de salida 'Results' -> {BANCO!r}")
    salidas[0].set("value", BANCO)

    bancos = r.findall("Settings/Databanks/Databank")
    if len(bancos) != 2:
        sys.exit(f"Se esperaban 2 bancos en el Retester y hay {len(bancos)}")
    for d in bancos:
        print(f"Retester: banco {d.get('name')} {d.get('value')!r} -> {BANCO!r}")
        d.set("value", BANCO)

    escribir(b, destino_builder)
    escribir(r, destino_retester)


if __name__ == "__main__":
    main(*sys.argv[1:5])
