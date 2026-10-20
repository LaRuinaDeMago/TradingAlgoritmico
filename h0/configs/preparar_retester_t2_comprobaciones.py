"""Tarea 2 de H0: ¿la licencia de prueba bloquea What If y Walk-Forward Optimization?

Uso:  python -I h0/configs/preparar_retester_t2_comprobaciones.py ORIGEN.cfx DESTINO.cfx
      (ORIGEN = Retester_H0_USDCHF_minimo.cfx: datos quemados de la decisión 0002, banco H0_USDCHF)

Según la documentación de la instalación (docs/overview/snippets/cross-checks.md), con una licencia
"Special Trial" What If, Sequential Optimization y Walk-Forward Optimization llaman a
checkSpecialTrialLimitation() y quedan desactivadas. Sequential Optimization no está en la plantilla del
Retester y queda fuera de esta prueba.

Se activan solo:
- WhatIf, con el escenario ByDays (todos los días marcados: no cambia las operaciones, es barato).
- WalkForwardOptimization, en modo simulado (type=0, el más rápido) y con MaxTests=20.
- MonteCarloManipulation como CONTROL POSITIVO (no está marcada como bloqueada): si tampoco deja
  resultados, el problema no es la licencia sino que las comprobaciones no se ejecutan.
Todas las condiciones de aceptación de esas comprobaciones se desactivan: nada puede "suspender",
así que ninguna estrategia puede descartarse ni borrarse del banco.
"""

import sys
import xml.etree.ElementTree as ET
import zipfile

ACTIVAS = ("WhatIf", "WalkForwardOptimization", "MonteCarloManipulation")


def unico(raiz, ruta):
    encontrados = raiz.findall(ruta)
    if len(encontrados) != 1:
        sys.exit(f"Se esperaba exactamente un {ruta} y hay {len(encontrados)}; no se escribe nada.")
    return encontrados[0]


def main(origen: str, destino: str) -> None:
    with zipfile.ZipFile(origen) as z:
        raiz = ET.fromstring(z.read("config.xml"))
    if raiz.tag != "Task" or raiz.get("type") != "Retest":
        sys.exit("La raíz no es <Task type='Retest'>")
    if unico(raiz, "Settings/Data/Setups/Setup/Chart").get("symbol") != "USDCHF_M1_dukas":
        sys.exit("El origen no usa los datos quemados (decisión 0002)")

    cambios = []

    def fijar(elemento, atributo, valor, descripcion):
        cambios.append(f"{descripcion}: {atributo} {elemento.get(atributo)!r} -> {valor!r}")
        elemento.set(atributo, valor)

    comprobaciones = unico(raiz, "Settings/CrossChecks")
    fijar(comprobaciones, "use", "true", "Comprobaciones cruzadas")
    for c in comprobaciones:
        fijar(c, "use", "true" if c.tag in ACTIVAS else "false", c.tag)
        if c.tag in ACTIVAS:
            for condicion in c.findall("AcceptanceSettings/Conditions/Condition"):
                fijar(condicion, "use", "false", f"{c.tag} (condición de aceptación)")

    for metodo in raiz.findall("Settings/CrossChecks/WhatIf/Settings/Methods/Method"):
        fijar(metodo, "use", "true" if metodo.get("type") == "ByDays" else "false", f"WhatIf ({metodo.get('type')})")
    dias = raiz.findall("Settings/CrossChecks/WhatIf/Settings/Methods/Method[@type='ByDays']/Params/Param")
    if len(dias) != 7 or any((p.text or "").strip() != "true" for p in dias):
        sys.exit("El escenario ByDays no tiene los 7 días marcados; no se escribe nada.")

    fijar(unico(raiz, "Settings/CrossChecks/WalkForwardOptimization/Settings/WalkForward"), "type", "0",
          "WalkForwardOptimization (modo)")
    maximo = unico(raiz, "Settings/CrossChecks/WalkForwardOptimization/Settings/MaxTests")
    cambios.append(f"WalkForwardOptimization: MaxTests {maximo.text!r} -> '20'")
    maximo.text = "20"

    with zipfile.ZipFile(destino, "x", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("config.xml", ET.tostring(raiz, encoding="unicode"))
    print("\n".join(cambios))


if __name__ == "__main__":
    main(*sys.argv[1:3])
