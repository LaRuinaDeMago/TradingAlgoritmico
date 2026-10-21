"""Plantilla del Builder para B17: la de H0 (preparar_builder_usdchf.py: generación aleatoria, mismos costes, sin
filtros ni cross checks) cambiando solo el símbolo, el inicio (margen de calentamiento de B1), el número de
estrategias y un tramo fuera de muestra con el formato documentado en
docs/custom-projects/task-settings/shared-sections.md de la instalación: <Range dateFrom= dateTo= type="oos"/>.

Uso:  python -I h0/configs/b17_preparar_builder.py ORIGEN.cfx DESTINO.cfx SIMBOLO N [SPREAD DESLIZAMIENTO]

SPREAD y DESLIZAMIENTO (pips) solo para la v3 sin costes; sin ellos, los de H0 (2 y 1).
"""

import io
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import preparar_builder_usdchf as base  # noqa: E402

DESDE = "2023.02.01"  # un mes de margen tras el primer dato importado (B1-bis)
OOS_DESDE, OOS_HASTA = "2024.04.01", "2024.10.30"  # últimos 7 de 21 meses
# v2: capacidad del banco. Con la de fábrica (1000) SQX desaloja las de peor fitness (Ret/DD dentro de muestra) cuando
# el banco se llena: la primera ejecución de B17 quedó mezclada y seleccionada (registro n.º 181).
CAPACIDAD = "100000"


def main(origen: str, destino: str, simbolo: str, n: str, spread: str | None = None, desliz: str | None = None) -> None:
    base.SIMBOLO, base.DESDE, base.ESTRATEGIAS = simbolo, DESDE, n
    if spread is not None:
        base.SPREAD_PIPS, base.DESLIZAMIENTO_PIPS = spread, desliz
    intermedio = io.BytesIO()
    base.main(origen, intermedio)
    with zipfile.ZipFile(intermedio) as z:
        raiz = ET.fromstring(z.read("config.xml"))
    oos = raiz.findall("Settings/Data/OutOfSample")
    if len(oos) != 1 or list(oos[0]):
        sys.exit("Se esperaba un único <OutOfSample> vacío; no se escribe nada.")
    ET.SubElement(oos[0], "Range", {"dateFrom": OOS_DESDE, "dateTo": OOS_HASTA, "type": "oos"})
    print(f"Fuera de muestra: se añade <Range dateFrom={OOS_DESDE!r} dateTo={OOS_HASTA!r} type='oos'>")
    capacidad = raiz.findall("Settings/Rankings/MaxStrategies")
    if len(capacidad) != 1:
        sys.exit("Se esperaba un único <MaxStrategies>; no se escribe nada.")
    print(f"Capacidad del banco: MaxStrategies {capacidad[0].text!r} -> {CAPACIDAD!r}")
    capacidad[0].text = CAPACIDAD
    with zipfile.ZipFile(destino, "x", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("config.xml", ET.tostring(raiz, encoding="unicode"))


if __name__ == "__main__":
    main(*sys.argv[1:7])
