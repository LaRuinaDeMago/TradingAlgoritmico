import json
import sys

lineas = open(sys.argv[1], encoding="utf-8").read().splitlines()
for l in lineas[-5:]:
    d = json.loads(l)
    print({k: str(v)[:110] for k, v in d.items() if k not in ("hash_prev", "hash", "salida")})
