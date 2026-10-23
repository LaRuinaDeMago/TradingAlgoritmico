"""A25 paso 3 (h0/a25_plan_vaciar_results.md, criterio N): ¿los .sqx de una carpeta son exactamente los nombres de un
manifiesto de b21_archivo.py? Uso: python -I h0/configs/a25_nombres_m3.py MANIFIESTO.json CARPETA. Código 1 si no."""
import json
import sys
from pathlib import Path

manifiesto = set(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
carpeta = {p.name for p in Path(sys.argv[2]).glob("*.sqx")}
faltan, sobran = sorted(manifiesto - carpeta), sorted(carpeta - manifiesto)
print(f"manifiesto: {len(manifiesto)}; carpeta: {len(carpeta)}; faltan: {len(faltan)} {faltan[:5]}; "
      f"sobran: {len(sobran)} {sobran[:5]} -> {'OK' if not faltan and not sobran else 'FALLO'}")
sys.exit(0 if not faltan and not sobran else 1)
