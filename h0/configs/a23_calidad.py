"""A23 (plan h0/a23_plan_calidad_usdchf.md): calidad de una exportación M1 de SQX, año a año, frente a una ventana de
referencia. Lee el CSV de `-data action=export ... format=Custom` (Date,Time,Open,High,Low,Close,Volume) en streaming.

Por año calcula: velas, desorden o duplicados, velas OHLC incoherentes, precios no positivos, cobertura de minutos de
lunes a viernes, huecos de más de 60 min dentro de la semana, velas planas (O=H=L=C), volumen cero y mediana de
volumen, apertura y cierre semanal más frecuentes (convención horaria) y saltos de un minuto de más del 2 %.
Después aplica los criterios C1–C6 del plan a cada año frente a la referencia.

Uso: python -I h0/configs/a23_calidad.py EXPORT.csv REF_DESDE REF_HASTA SALIDA.json   (fechas yyyy.mm.dd, inclusivas)
Sale con código 0 si el análisis se completa (el veredicto va en la salida, no en el código).
"""

import collections
import json
import math
import statistics
import sys
from datetime import date, datetime, timedelta

HUECO_MIN = 60          # minutos: un hueco mayor dentro de la semana se cuenta
SALTO = 0.02            # 2 % en un minuto
EXCEPCIONES_SALTO = {date(2015, 1, 15)}  # SNB retira el suelo del EURCHF: salto real conocido
MINUTOS_SEMANA = 5 * 1440


def _nuevo() -> dict:
    return {"velas": 0, "desorden": 0, "incoherentes": 0, "no_positivos": 0, "planas": 0, "vol_cero": 0,
            "huecos": 0, "saltos": [], "aperturas": collections.Counter(), "cierres": collections.Counter(),
            "dias": set(), "_vol": [], "primero": None, "ultimo": None}


def leer(filas, ref_desde: date, ref_hasta: date) -> dict:
    """filas: iterable de listas [fecha, hora, o, h, l, c, v] (sin cabecera). Devuelve estadísticas por año y de la
    referencia (clave 'ref')."""
    años: dict = collections.defaultdict(_nuevo)
    anterior = None  # (instante, cierre)
    for f in filas:
        t = datetime.strptime(f[0] + " " + f[1], "%Y.%m.%d %H:%M:%S")
        o, h, l, c, v = (float(x) for x in f[2:7])
        destinos = [años[t.year]] + ([años["ref"]] if ref_desde <= t.date() <= ref_hasta else [])
        for a in destinos:
            a["velas"] += 1
            if min(o, h, l, c) <= 0:
                a["no_positivos"] += 1
            if h < max(o, c) or l > min(o, c) or h < l:
                a["incoherentes"] += 1
            if o == h == l == c:
                a["planas"] += 1
            if v == 0:
                a["vol_cero"] += 1
            if t.weekday() < 5:
                a["dias"].add(t.date())
            a["primero"] = a["primero"] or t.date()
            a["ultimo"] = t.date()
            if len(a["_vol"]) < 2_000_000:
                a["_vol"].append(v)
        if anterior is not None:
            t0, c0 = anterior
            dt = (t - t0).total_seconds() / 60
            mismo_ref = ref_desde <= t0.date() <= ref_hasta and ref_desde <= t.date() <= ref_hasta
            dest = [años[t.year]] + ([años["ref"]] if mismo_ref else [])
            for a in dest:
                if dt <= 0:
                    a["desorden"] += 1
                elif dt >= 24 * 60 and (t.weekday() < t0.weekday() or (t - t0).days >= 7 or t0.weekday() >= 4):
                    a["aperturas"][(t.weekday(), t.strftime("%H:%M"))] += 1   # tras un fin de semana
                    a["cierres"][(t0.weekday(), t0.strftime("%H:%M"))] += 1
                elif dt > HUECO_MIN:
                    a["huecos"] += 1
                if dt > 0 and dt <= 5 and c0 > 0 and abs(math.log(c / c0)) > SALTO and t.date() not in EXCEPCIONES_SALTO:
                    a["saltos"].append(t.strftime("%Y.%m.%d %H:%M"))
        anterior = (t, c)
    return {k: _cerrar(v) for k, v in años.items()}


def _cerrar(a: dict) -> dict:
    laborables = 0
    if a["primero"]:
        dia = a["primero"]
        while dia <= a["ultimo"]:
            laborables += dia.weekday() < 5
            dia += timedelta(days=1)
    semanas = max(laborables / 5, 1e-9)
    moda = lambda c: list(c.most_common(1)[0][0]) if c else None  # noqa: E731
    return {"velas": a["velas"], "desorden": a["desorden"], "incoherentes": a["incoherentes"],
            "no_positivos": a["no_positivos"], "dias_laborables_con_datos": len(a["dias"]), "dias_laborables_del_tramo": laborables,
            "cobertura": round(a["velas"] / (semanas * MINUTOS_SEMANA), 4) if a["dias"] else 0.0,
            "huecos_por_52_semanas": round(a["huecos"] * 52 / semanas, 2), "huecos": a["huecos"],
            "planas": round(a["planas"] / max(a["velas"], 1), 4), "vol_cero": round(a["vol_cero"] / max(a["velas"], 1), 4),
            "vol_mediana": statistics.median(a["_vol"]) if a["_vol"] else None,
            "apertura_semanal": moda(a["aperturas"]), "cierre_semanal": moda(a["cierres"]),
            "aperturas_distintas": len(a["aperturas"]), "saltos": a["saltos"][:20], "n_saltos": len(a["saltos"])}


def criterios(año: dict, ref: dict) -> dict:
    """C1–C6 del plan (fijados antes de ver los datos completos)."""
    c = {
        "C1_integridad": año["desorden"] == 0 and año["incoherentes"] == 0 and año["no_positivos"] == 0,
        "C2_cobertura": año["cobertura"] >= 0.9 * ref["cobertura"],
        "C3_huecos": año["huecos_por_52_semanas"] <= max(10.0, 3 * ref["huecos_por_52_semanas"]),
        "C4_planas": año["planas"] <= max(3 * ref["planas"], ref["planas"] + 0.05),
        "C5_convencion": año["apertura_semanal"] == ref["apertura_semanal"] and año["cierre_semanal"] == ref["cierre_semanal"],
        "C6_saltos": año["n_saltos"] == 0,
    }
    vm, rm = año["vol_mediana"], ref["vol_mediana"]
    c["VOL_comparable(informativo)"] = bool(vm and rm and 0.1 <= vm / rm <= 10)
    c["pasa"] = all(v for k, v in c.items() if k.startswith("C"))
    return c


def tramo_utilizable(veredictos: dict) -> list[int] | None:
    """El tramo de años contiguos más largo que termina en el último año y pasa todos los criterios."""
    años = sorted(k for k in veredictos if isinstance(k, int))
    tramo = []
    for y in reversed(años):
        if not veredictos[y]["pasa"]:
            break
        tramo.insert(0, y)
    return [tramo[0], tramo[-1]] if tramo else None


def main(argv: list[str]) -> int:
    ruta, desde, hasta, salida = argv
    d = lambda s: datetime.strptime(s, "%Y.%m.%d").date()  # noqa: E731
    with open(ruta, encoding="utf-8") as f:
        next(f)
        stats = leer((linea.rstrip("\n").split(",") for linea in f if linea.strip()), d(desde), d(hasta))
    ref = stats.pop("ref")
    veredictos = {y: criterios(s, ref) for y, s in sorted(stats.items())}
    tramo = tramo_utilizable(veredictos)
    out = {"referencia": {"desde": desde, "hasta": hasta, **ref}, "por_año": stats, "criterios": veredictos,
           "tramo_utilizable": tramo}
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print(f"referencia: cobertura {ref['cobertura']}, huecos/52s {ref['huecos_por_52_semanas']}, planas {ref['planas']}, "
          f"apertura {ref['apertura_semanal']}, cierre {ref['cierre_semanal']}, vol. mediana {ref['vol_mediana']}")
    for y, s in sorted(stats.items()):
        v = veredictos[y]
        fallos = [k for k, ok in v.items() if k.startswith("C") and not ok]
        print(f"{y}: velas {s['velas']}, cob {s['cobertura']}, huecos/52s {s['huecos_por_52_semanas']}, planas "
              f"{s['planas']}, apert {s['apertura_semanal']}, cierre {s['cierre_semanal']}, saltos {s['n_saltos']}, "
              f"vol {s['vol_mediana']} -> {'PASA' if v['pasa'] else 'NO: ' + ','.join(fallos)}")
    print(f"tramo utilizable: {tramo}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
