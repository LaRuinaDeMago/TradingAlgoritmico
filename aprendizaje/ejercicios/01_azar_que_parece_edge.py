"""Ejercicio 01: cuando pruebas muchas estrategias sin ventaja, la mejor parece buena.

Genera N estrategias que operan al azar sobre un mercado sin tendencia
(ventaja real = 0 en todas) y muestra el ratio de Sharpe de la mejor.

    python aprendizaje/ejercicios/01_azar_que_parece_edge.py
    python aprendizaje/ejercicios/01_azar_que_parece_edge.py --estrategias 10
    python aprendizaje/ejercicios/01_azar_que_parece_edge.py --estrategias 10000 --anios 2

Solo usa la biblioteca estándar. Con la misma semilla, el resultado es idéntico.
"""

import argparse
import math
import random
import statistics

DIAS_POR_ANIO = 252


def sharpe_anual(rentabilidades):
    media = statistics.fmean(rentabilidades)
    desviacion = statistics.pstdev(rentabilidades)
    return media / desviacion * math.sqrt(DIAS_POR_ANIO)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--estrategias", type=int, default=1000)
    p.add_argument("--anios", type=float, default=5)
    p.add_argument("--semilla", type=int, default=2026)
    a = p.parse_args()

    azar = random.Random(a.semilla)
    dias = int(a.anios * DIAS_POR_ANIO)
    # Mercado sin ventaja para nadie: cada día sube o baja con media 0 y volatilidad 1 %.
    mercado = [azar.gauss(0, 0.01) for _ in range(dias)]

    sharpes = []
    for _ in range(a.estrategias):
        # Cada estrategia decide al azar cada día: comprado (+1) o vendido (-1).
        posiciones = [azar.choice((1, -1)) for _ in range(dias)]
        rentabilidades = [posiciones[i] * mercado[i] for i in range(dias)]
        sharpes.append(sharpe_anual(rentabilidades))

    sharpes.sort()
    mejor = sharpes[-1]
    teorico = math.sqrt(2 * math.log(a.estrategias)) / math.sqrt(a.anios)
    print(f"Estrategias probadas: {a.estrategias} · Periodo: {a.anios} años · Ventaja real: 0")
    print(f"Sharpe medio:          {statistics.fmean(sharpes):+.2f}   (lo esperable: 0)")
    print(f"Sharpe de la MEJOR:    {mejor:+.2f}")
    print(f"Aproximación teórica:  {teorico:+.2f}   (raíz(2·ln N) / raíz(años))")
    print(f"Estrategias con Sharpe > 1: {sum(s > 1 for s in sharpes)}")
    print("\nNinguna tiene ventaja. Si solo enseñas la mejor, parece un sistema excelente.")


if __name__ == "__main__":
    main()
