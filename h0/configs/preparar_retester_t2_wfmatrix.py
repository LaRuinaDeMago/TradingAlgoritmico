"""Tarea 2 de H0, experimento discriminante: solo Walk-Forward Matrix.

Uso:  python -I h0/configs/preparar_retester_t2_wfmatrix.py ORIGEN.cfx DESTINO.cfx
      (ORIGEN = Retester_H0_USDCHF_t2_comprobaciones.cfx)

En la primera prueba (registros n.57–61) What If y Walk-Forward Optimization dejaron carpetas de resultados
vacías (0 bytes), sin ningún mensaje en los logs. Puede ser el bloqueo de la licencia de prueba o una
configuración insuficiente. La Walk-Forward Matrix usa el mismo motor de walk-forward y, según la
documentación de la instalación, NO está bloqueada en "Special Trial": si ella sí deja resultados con
contenido, el vacío del WFO se debe a la licencia; si también sale vacía, es la configuración (INCONCLUSO).

Mismo modo que el WFO de la primera prueba (type=0, simulado) y MaxTests=20; sin condiciones de aceptación.
"""

import sys
import xml.etree.ElementTree as ET
import zipfile


def unico(raiz, ruta):
    encontrados = raiz.findall(ruta)
    if len(encontrados) != 1:
        sys.exit(f"Se esperaba exactamente un {ruta} y hay {len(encontrados)}; no se escribe nada.")
    return encontrados[0]


def main(origen: str, destino: str) -> None:
    with zipfile.ZipFile(origen) as z:
        raiz = ET.fromstring(z.read("config.xml"))
    if unico(raiz, "Settings/Data/Setups/Setup/Chart").get("symbol") != "USDCHF_M1_dukas":
        sys.exit("El origen no usa los datos quemados (decisión 0002)")

    cambios = []

    def fijar(elemento, atributo, valor, descripcion):
        cambios.append(f"{descripcion}: {atributo} {elemento.get(atributo)!r} -> {valor!r}")
        elemento.set(atributo, valor)

    comprobaciones = unico(raiz, "Settings/CrossChecks")
    fijar(comprobaciones, "use", "true", "Comprobaciones cruzadas")
    for c in comprobaciones:
        fijar(c, "use", "true" if c.tag == "WalkForwardMatrix" else "false", c.tag)
    for condicion in raiz.findall("Settings/CrossChecks/WalkForwardMatrix/AcceptanceSettings/Conditions/Condition"):
        fijar(condicion, "use", "false", "WalkForwardMatrix (condición de aceptación)")
    fijar(unico(raiz, "Settings/CrossChecks/WalkForwardMatrix/Settings/WalkForward"), "type", "0",
          "WalkForwardMatrix (modo)")
    maximo = unico(raiz, "Settings/CrossChecks/WalkForwardMatrix/Settings/MaxTests")
    cambios.append(f"WalkForwardMatrix: MaxTests {maximo.text!r} -> '20'")
    maximo.text = "20"

    with zipfile.ZipFile(destino, "x", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("config.xml", ET.tostring(raiz, encoding="unicode"))
    print("\n".join(cambios))


if __name__ == "__main__":
    main(*sys.argv[1:3])
