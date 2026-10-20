"""Prepara la plantilla mínima del Retester para la tarea 4 de H0 (decisión 0002: datos quemados).

Uso:  python -I h0/configs/preparar_retester_usdchf.py ORIGEN.cfx DESTINO.cfx

Mismos datos y costes que la plantilla del Builder (preparar_builder_usdchf.py), para que el backtest
repetido sea comparable con el de la generación. Sin filtros (no se descarta ninguna estrategia) y
sin comprobaciones cruzadas: la de fábrica repetiría el backtest con EURUSD y quemaría otro mercado.
Cada elemento tocado debe existir exactamente las veces esperadas; si no, se detiene sin escribir.
"""

import sys
import xml.etree.ElementTree as ET
import zipfile

SIMBOLO, DESDE, HASTA, MARCO = "USDCHF_M1_dukas", "2023.01.01", "2024.10.30", "H1"
SPREAD_PIPS, DESLIZAMIENTO_PIPS = "2", "1"


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
    if raiz.tag != "Task" or raiz.get("type") != "Retest":
        sys.exit("La raíz no es <Task type='Retest'>")

    cambios = []

    def fijar(elemento, atributo, valor, descripcion):
        cambios.append(f"{descripcion}: {atributo} {elemento.get(atributo)!r} -> {valor!r}")
        elemento.set(atributo, valor)

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
    # La plantilla de fábrica del Retester no trae <Swap> (la del Builder sí, desactivado). Sin él podría aplicarse
    # el swap del instrumento, que para USDCHF viene activado: se añade el mismo elemento que en el Builder.
    swaps = setup.findall("Swap")
    if not swaps:
        ET.SubElement(setup, "Swap", {"use": "false", "type": "money", "long": "0", "short": "0",
                                      "tripleSwapOn": "WEDNESDAY"})
        cambios.append("Costes (swap): se añade <Swap use='false' ...> igual que en el Builder")
    else:
        fijar(unico(raiz, "Settings/Data/Setups/Setup/Swap"), "use", "false", "Costes (swap)")

    for condicion in raiz.findall("Settings/Rankings/Conditions/Condition"):
        fijar(condicion, "use", "false", "Filtro del banco")

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
