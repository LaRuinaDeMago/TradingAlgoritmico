"""B17, primera ejecución (inválida): diagnostica el desalojo del banco Builder/Results (capacidad MaxStrategies = 1000,
fitness Ret/DD dentro de muestra). Solo nombres y recuentos: NO mira ninguna métrica de los brazos.

Uso:  python -I h0/configs/b17_diagnostico_desalojo.py CARPETA_B17 CARPETA_COPIAS [CARPETA_COPIAS ...]

CARPETA_COPIAS: carpetas con .sqx guardados antes (p. ej. h0/evidencias/t3_salidas/estrategias) para ver qué
estrategias de H0 desalojadas tienen copia por nombre (indicio, no prueba: SQX reutiliza nombres).
"""

import csv
import io
import json
import sys
from pathlib import Path


def nombres(ruta: Path) -> set[str]:
    texto = ruta.read_bytes().decode("utf-8-sig")
    return {f["Strategy Name"] for f in csv.DictReader(io.StringIO(texto), delimiter=";")}


def main(carpeta: str, *copias: str) -> int:
    b = Path(carpeta)
    etapas = ["cal", "real", "nulo1", "nulo2"]
    antes = {e: nombres(b / f"Results_antes_{e}.csv") for e in etapas}
    despues = {e: nombres(b / f"Results_despues_{e}.csv") for e in etapas}
    h0 = antes["cal"]
    con_copia = set()
    for c in copias:
        con_copia |= {p.stem for p in Path(c).glob("*.sqx")}
    perdidas_h0 = sorted(h0 - despues["nulo2"])
    res = {
        "capacidad_y_fitness": "MaxStrategies=1000; FitnessCriteria Ranking=ReturnDDRatio (IS)",
        "por_etapa": {e: {"antes": len(antes[e]), "despues": len(despues[e]), "nuevas_que_entraron": len(despues[e] - antes[e]),
                          "desalojadas": len(antes[e] - despues[e])} for e in etapas},
        "estrategias_H0_al_empezar": len(h0),
        "estrategias_H0_desalojadas": len(perdidas_h0),
        "desalojadas_H0_con_copia_por_nombre": sorted(set(perdidas_h0) & con_copia),
        "desalojadas_H0_sin_copia_por_nombre": sorted(set(perdidas_h0) - con_copia),
    }
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
