"""B17: análisis del control negativo de la búsqueda (plan h0/b17_plan_control_negativo.md). Todo fijado antes de ver
datos: el embudo de filtros F, las pruebas y las reglas de decisión del plan.

Uso:  python -I h0/configs/b17_analizar.py N REAL_ANTES.csv REAL_DESPUES.csv NULO1_ANTES.csv NULO1_DESPUES.csv \
          [NULO2_ANTES.csv NULO2_DESPUES.csv ...]

Cada par ANTES/DESPUÉS son exportaciones del banco Builder/Results (`-databank action=export`) antes y después de la
generación de ese brazo; las estrategias del brazo son las filas cuyo nombre no estaba antes. Se detiene si no son
exactamente N. Solo biblioteca estándar (sin numpy: asunto A18).
"""

import csv
import io
import json
import math
import random
import statistics
import sys
from pathlib import Path

COL = {"nombre": "Strategy Name", "ops_is": "# of trades (IS)", "pf_is": "Profit factor (IS)",
       "retdd_is": "Ret/DD Ratio (IS)", "sharpe_is": "Sharpe Ratio (IS)", "neto_is": "Net profit (IS)",
       "ops_oos": "# of trades (OOS)", "pf_oos": "Profit factor (OOS)", "neto_oos": "Net profit (OOS)",
       "sharpe_oos": "Sharpe Ratio (OOS)"}


def pasa_is(e: dict) -> bool:
    """Embudo F, etapa dentro de muestra (fijado en el plan)."""
    return e["ops_is"] >= 100 and e["pf_is"] >= 1.20 and e["retdd_is"] >= 2.0


def pasa_oos(e: dict) -> bool:
    """Embudo F, etapa fuera de muestra (fijado en el plan)."""
    return e["ops_oos"] >= 20 and e["neto_oos"] > 0 and e["pf_oos"] >= 1.10


def leer(ruta: str | Path) -> list[dict]:
    texto = Path(ruta).read_bytes().decode("utf-8-sig")
    filas = list(csv.DictReader(io.StringIO(texto), delimiter=";"))
    salida = []
    for f in filas:
        e = {"nombre": f[COL["nombre"]]}
        for clave, columna in COL.items():
            if clave != "nombre":
                e[clave] = float(f[columna] or 0)
        salida.append(e)
    return salida


# v2.1: SQX genera con 7 hilos y al parar puede entrar alguna más de las pedidas (registro n.º 191: 1001 de 1000).
# Se usan TODAS las nuevas (quitar alguna exigiría elegir cuál); se admite un exceso de hasta un hilo por núcleo.
EXCESO_MAXIMO = 7


def nuevas(antes: str, despues: str, n: int) -> list[dict]:
    viejas = {e["nombre"] for e in leer(antes)}
    todas = leer(despues)
    if not viejas <= {e["nombre"] for e in todas}:
        sys.exit(f"PARADA: falta alguna estrategia de antes en {despues}")
    sel = [e for e in todas if e["nombre"] not in viejas]
    if not n <= len(sel) <= n + EXCESO_MAXIMO:
        sys.exit(f"PARADA: {despues} tiene {len(sel)} estrategias nuevas y se esperaban entre {n} y {n + EXCESO_MAXIMO}")
    return sel


def fisher_una_cola(a: int, b: int, c: int, d: int) -> float:
    """P(X >= a) en la hipergeométrica: ¿el brazo real (a pasan, b no) supera al nulo (c pasan, d no)?"""
    n1, k, total = a + b, a + c, a + b + c + d
    den = math.comb(total, n1)
    return sum(math.comb(k, x) * math.comb(total - k, n1 - x) for x in range(a, min(k, n1) + 1)) / den


def rangos(x: list[float]) -> list[float]:
    orden = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and x[orden[j + 1]] == x[orden[i]]:
            j += 1
        for k in range(i, j + 1):
            r[orden[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x: list[float], y: list[float]) -> float:
    rx, ry = rangos(x), rangos(y)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def spearman_permutacion(x, y, veces=2000, semilla=17) -> tuple[float, float]:
    """rho y p de dos colas por permutación (semilla fija: el análisis es repetible)."""
    rho = spearman(x, y)
    r, yy, extremos = random.Random(semilla), list(y), 0
    for _ in range(veces):
        r.shuffle(yy)
        extremos += abs(spearman(x, yy)) >= abs(rho)
    return rho, (extremos + 1) / (veces + 1)


def resumen_brazo(es: list[dict]) -> dict:
    pis = [e for e in es if pasa_is(e)]
    pf = [e for e in pis if pasa_oos(e)]
    activas = [e for e in es if e["ops_is"] >= 30 and e["ops_oos"] >= 10]
    rho, p = spearman_permutacion([e["sharpe_is"] for e in activas], [e["sharpe_oos"] for e in activas]) \
        if len(activas) >= 10 else (None, None)
    decil = sorted(es, key=lambda e: e["retdd_is"], reverse=True)[:max(1, len(es) // 10)]
    mejor = max(es, key=lambda e: e["sharpe_is"])
    return {
        "estrategias": len(es), "pasan_F_IS": len(pis), "pasan_F_completo": len(pf),
        "tasa_F_completo": round(len(pf) / len(es), 4),
        "tasa_OOS_entre_las_que_pasan_IS": round(len(pf) / len(pis), 4) if pis else None,
        "activas_para_spearman": len(activas), "spearman_sharpe_IS_OOS": rho and round(rho, 4),
        "p_spearman": p and round(p, 4),
        "mediana_neto_OOS_decil_superior_RetDD_IS": round(statistics.median(e["neto_oos"] for e in decil), 2),
        "mediana_operaciones_IS": statistics.median(e["ops_is"] for e in es),
        "mejor_sharpe_IS": {k: mejor[k] for k in ("nombre", "sharpe_is", "retdd_is", "pf_is", "sharpe_oos",
                                                  "neto_oos")},
    }


def main(argv: list[str]) -> int:
    n = int(argv[0])
    pares = [(argv[i], argv[i + 1]) for i in range(1, len(argv), 2)]
    brazos = [nuevas(a, d, n) for a, d in pares]
    nombres = ["real"] + [f"nulo{k}" for k in range(1, len(brazos))]
    res = {nom: resumen_brazo(es) for nom, es in zip(nombres, brazos)}
    a, n_real = res["real"]["pasan_F_completo"], res["real"]["estrategias"]
    c = sum(res[nom]["pasan_F_completo"] for nom in nombres[1:])
    nulos = sum(res[nom]["estrategias"] for nom in nombres[1:])
    res["prueba_T1_fisher_real_mayor_que_nulo"] = {"real_pasan": a, "real_no": n_real - a, "nulo_pasan": c,
                                                    "nulo_no": nulos - c,
                                                    "p_una_cola": round(fisher_una_cola(a, n_real - a, c, nulos - c), 6)}
    cota = 2 / math.sqrt(max(1, min(res[nom]["activas_para_spearman"] for nom in nombres[1:])))
    res["comprobacion_S_nulos_sin_persistencia"] = {
        "cota_aprox_95": round(cota, 4),
        "cumple": all(res[nom]["p_spearman"] is not None and res[nom]["p_spearman"] >= 0.01 for nom in nombres[1:])}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
