"""Prepara la plantilla mínima del Builder para la tarea 3a de H0 (decisión 0002: datos quemados).

Uso:  python -I h0/configs/preparar_builder_usdchf.py ORIGEN.cfx DESTINO.cfx

Parte de la plantilla que exporta `sqcli -project action=saveconfig name=Builder` (un .cfx con un
solo config.xml de raíz <Task>, según docs/custom-projects/cfx-format.md de la instalación de SQX)
y cambia solo lo listado en CAMBIOS. Cada elemento tocado debe existir exactamente las veces
esperadas; si no, se detiene sin escribir nada.

Objetivo: comprobar que el proceso funciona, no buscar estrategias buenas. Por eso no hay filtros
de calidad (no se selecciona nada) y se para en cuanto hay 10 estrategias.
"""

import sys
import xml.etree.ElementTree as ET
import zipfile

SIMBOLO, DESDE, HASTA, MARCO = "USDCHF_M1_dukas", "2023.01.01", "2024.10.30", "H1"
SPREAD_PIPS, DESLIZAMIENTO_PIPS = "2", "1"
ESTRATEGIAS = "10"


def unico(raiz, ruta):
    encontrados = raiz.findall(ruta)
    if len(encontrados) != 1:
        sys.exit(f"Se esperaba exactamente un {ruta} y hay {len(encontrados)}; no se escribe nada.")
    return encontrados[0]


def main(origen: str, destino: str) -> None:
    with zipfile.ZipFile(origen) as z:
        if z.namelist() != ["config.xml"]:
            sys.exit(f"Se esperaba un .cfx con solo config.xml y tiene {z.namelist()}")
        raiz = ET.fromstring(z.read("config.xml"))
    if raiz.tag != "Task" or raiz.get("type") != "Build":
        sys.exit("La raíz no es <Task type='Build'>")

    cambios = []

    def fijar(elemento, atributo, valor, descripcion):
        cambios.append(f"{descripcion}: {atributo} {elemento.get(atributo)!r} -> {valor!r}")
        elemento.set(atributo, valor)

    fijar(unico(raiz, "Settings/WhatToBuild/BuildMode"), "generationType", "random-generation", "Modo de generación")
    setup = unico(raiz, "Settings/Data/Setups/Setup")
    fijar(setup, "dateFrom", DESDE, "Datos")
    fijar(setup, "dateTo", HASTA, "Datos")
    fijar(setup, "slippage", DESLIZAMIENTO_PIPS, "Costes")
    grafico = unico(raiz, "Settings/Data/Setups/Setup/Chart")
    fijar(grafico, "symbol", SIMBOLO, "Datos")
    fijar(grafico, "timeframe", MARCO, "Datos")
    fijar(grafico, "spread", SPREAD_PIPS, "Costes")
    for metodo in raiz.findall("Settings/Data/Setups/Setup/Commissions/Method"):
        fijar(metodo, "use", "true" if metodo.get("type") == "None" else "false", "Costes (comisión)")
    fijar(unico(raiz, "Settings/Data/Setups/Setup/Swap"), "use", "false", "Costes (swap)")

    # Sin filtros de calidad: en H0 no se selecciona nada (familia H0-proceso, decisión 0002).
    for condicion in raiz.findall("Settings/Rankings/Conditions/Condition"):
        fijar(condicion, "use", "false", "Filtro del banco")
    for condicion in raiz.findall("Settings/WhatToBuild/BuildMode/Conditions/Condition"):
        fijar(condicion, "use", "false", "Filtro de población inicial")

    parada = unico(raiz, "Settings/Rankings/StopCondition")
    fijar(parada, "type", "passed-count", "Parada")
    fijar(parada, "passedStrategies", ESTRATEGIAS, "Parada")
    fijar(parada, "restartCount", "0", "Parada")

    fijar(unico(raiz, "Settings/CrossChecks"), "use", "false", "Comprobaciones cruzadas")

    simbolos = unico(raiz, "Settings/Resources/Symbols")
    for s in list(simbolos):
        if s.get("name") != SIMBOLO:
            cambios.append(f"Recursos: se quita la declaración del símbolo {s.get('name')!r}")
            simbolos.remove(s)

    with zipfile.ZipFile(destino, "x", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("config.xml", ET.tostring(raiz, encoding="unicode"))
    print("\n".join(cambios))


if __name__ == "__main__":
    main(*sys.argv[1:3])
