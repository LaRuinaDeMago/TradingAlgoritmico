"""B20, diagnóstico (sin criterio): ¿qué tienen los casos en que SQX da Ret/DD = 10,0 o PF = 5,0 exactos?
Uso: python -I h0/configs/b20_diagnostico_exactos.py EXPORTACION.csv"""

import collections
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b20_recorte_metricas as b20  # noqa: E402

filas = b20.leer(sys.argv[1])
for m, tope in b20.TOPES.items():
    exactos = [e for e in filas if e[f"{m}_sqx"] == tope]
    calc = [b20.recalcular(e)[m] for e in exactos]
    print(f"== {m} = {tope} exacto: {len(exactos)} casos; por tramo {dict(collections.Counter(e['tramo'] for e in exactos))}")
    print(f"   operaciones: mín {min(e['operaciones'] for e in exactos):.0f}, mediana "
          f"{statistics.median(e['operaciones'] for e in exactos):.0f}, máx {max(e['operaciones'] for e in exactos):.0f}")
    print(f"   drawdown = 0: {sum(1 for e in exactos if e['dd'] == 0)}; pérdida media = 0: "
          f"{sum(1 for e in exactos if e['pierde'] == 0)}; beneficio neto <= 0: {sum(1 for e in exactos if e['neto'] <= 0)}")
    validos = [c for c in calc if c is not None]
    print(f"   recalculado: {len(validos)} con valor; sin valor (división por cero) {len(calc) - len(validos)}")
    if validos:
        print(f"   recalculado mín {min(validos):.3f}, mediana {statistics.median(validos):.3f}, máx {max(validos):.3f}")
    print(f"   cerca del tope (±5 %) sin ser exactos: "
          f"{sum(1 for e in filas if e[f'{m}_sqx'] != tope and abs(e[f'{m}_sqx'] - tope) <= 0.05 * tope)}")
