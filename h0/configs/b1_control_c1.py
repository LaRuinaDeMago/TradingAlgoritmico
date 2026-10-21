"""B1, control negativo C1 con el archivo real: siembra en copias de E_A los cinco errores del plan y comprueba que el
comparador detecta cada uno, y que E_A frente a sí misma da 0 diferencias.

Uso:  python -I h0/configs/b1_control_c1.py E_A.csv CARPETA_COPIAS
Devuelve 0 solo si se detectan los cinco errores y la copia sin tocar sale idéntica.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from b1_comparar_velas import comparar, leer  # noqa: E402


def mover(linea: str, delta: timedelta) -> str:
    f = linea.split(",")
    t = datetime.strptime(f"{f[0]} {f[1]}", "%Y.%m.%d %H:%M:%S") + delta
    return ",".join([t.strftime("%Y.%m.%d"), t.strftime("%H:%M:%S")] + f[2:])


def sembrar(lineas: list[str]) -> dict[str, tuple[list[str], str]]:
    """Cada caso: (líneas de la copia, contador del comparador que debe dejar de ser 0 o valor esperado)."""
    cab, filas = lineas[0], lineas[1:]
    precio = filas[3000].split(",")
    precio[5] = f"{float(precio[5]) + 0.00001:.5f}"
    return {
        "sin_tocar": ([cab] + filas, "identicas"),
        "vela_eliminada": ([cab] + filas[:1000] + filas[1001:], "ausentes_en_b"),
        "vela_duplicada": ([cab] + filas[:2000] + [filas[2000]] + filas[2000:], "duplicadas_b"),
        "precio_mas_un_punto": ([cab] + filas[:3000] + [",".join(precio)] + filas[3001:], "valores_distintos"),
        "una_vela_mas_un_minuto": ([cab] + filas[:4000] + [mover(filas[4000], timedelta(minutes=1))] + filas[4001:],
                                   "ausentes_en_b"),
        "todo_mas_una_hora": ([cab] + [mover(x, timedelta(hours=1)) for x in filas], "desplazamiento_global_min"),
    }


def main(ruta_a: str, carpeta: str) -> int:
    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)
    lineas = Path(ruta_a).read_text(encoding="utf-8").splitlines()
    a = leer(ruta_a)
    resultado, todo_bien = {}, True
    for nombre, (copia, clave) in sembrar(lineas).items():
        ruta = destino / f"{nombre}.csv"
        ruta.write_text("\n".join(copia) + "\n", encoding="utf-8")
        r = comparar(a, leer(ruta))
        if nombre == "sin_tocar":
            ok = r["identicas"]
        elif clave == "desplazamiento_global_min":
            ok = (not r["identicas"]) and r[clave] == 60
        else:
            ok = (not r["identicas"]) and bool(r[clave])
        todo_bien &= ok
        resultado[nombre] = {"detectado_como_se_espera": ok, "identicas": r["identicas"], clave: r[clave],
                             "ausentes": r["ausentes_en_b"], "sobrantes": r["sobrantes_en_b"],
                             "duplicadas": r["duplicadas_b"], "valores": r["valores_distintos"]}
    print(json.dumps(resultado, ensure_ascii=False, indent=1))
    return 0 if todo_bien else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
