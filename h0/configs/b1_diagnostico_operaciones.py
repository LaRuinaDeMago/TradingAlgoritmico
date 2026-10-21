"""B1, DIAGNÓSTICO del criterio A5 (no lo sustituye): ¿las diferencias de operaciones entre el símbolo original y el
importado se explican por el calentamiento de indicadores al principio de la ventana?

Uso:  python -I h0/configs/b1_diagnostico_operaciones.py CARPETA_A CARPETA_B

Compara cada operación sin el número de orden (columna 0), sin el nombre del símbolo (1) y sin el saldo acumulado (9),
que arrastra las operaciones anteriores. Para cada estrategia da las comunes, las que solo están en un lado y la
apertura más tardía de una operación no común: si todas caen al principio, la diferencia es de calentamiento.
"""

import csv
import io
import json
import sys
from pathlib import Path

IGNORAR = {0, 1, 9}


def operaciones(ruta: Path) -> list[tuple[str, ...]]:
    filas = list(csv.reader(io.StringIO(ruta.read_bytes().decode("utf-8-sig")), delimiter=";"))
    return [tuple(v for i, v in enumerate(f) if i not in IGNORAR) for f in filas[1:] if f]


def main(a: str, b: str) -> int:
    resumen = {}
    for ruta_a in sorted(Path(a).glob("*.csv")):
        oa, ob = operaciones(ruta_a), operaciones(Path(b) / ruta_a.name)
        comunes = set(oa) & set(ob)
        solo_a, solo_b = [o for o in oa if o not in comunes], [o for o in ob if o not in comunes]
        no_comunes = solo_a + solo_b
        # orden: la tupla empieza por (tipo, apertura, ...); la apertura es el índice 1
        ultima_no_comun = max((o[1] for o in no_comunes), default=None)
        posteriores_a = [o for o in oa if ultima_no_comun is None or o[1] > ultima_no_comun]
        posteriores_b = [o for o in ob if ultima_no_comun is None or o[1] > ultima_no_comun]
        resumen[ruta_a.name] = {
            "operaciones_a": len(oa), "operaciones_b": len(ob), "comunes": len(comunes),
            "solo_a": len(solo_a), "solo_b": len(solo_b),
            "apertura_mas_tardia_no_comun": ultima_no_comun,
            "tras_esa_fecha_identicas": posteriores_a == posteriores_b,
            "operaciones_tras_esa_fecha": len(posteriores_a),
        }
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
