"""Reproduce cifras de Bailey, Borwein, López de Prado y Zhu (2014), "Pseudo-Mathematics and Financial Charlatanism",
y las aplica a nuestro reparto de datos (decisión 0003). No forma parte del motor (regla C10). Solo biblioteca estándar.

Ec. 2.4: E[max_N] ≈ (1-γ)·Z⁻¹[1-1/N] + γ·Z⁻¹[1-1/(N·e)], Sharpe anualizado con 1 año de datos y Sharpe real 0.
Ec. 3.1: con y años, E[max_N] se divide por √y.  Ec. 3.2 (MinBTL): y ≈ (E[max_N] a 1 año / objetivo)².
Cota superior citada: √(2·ln N).
"""

from math import e, log, sqrt
from statistics import NormalDist

Z = NormalDist()
GAMMA = 0.5772156649


def max_esperado(n: int) -> float:
    return (1 - GAMMA) * Z.inv_cdf(1 - 1 / n) + GAMMA * Z.inv_cdf(1 - 1 / (n * e))


def min_btl(n: int, objetivo: float = 1.0) -> float:
    return (max_esperado(n) / objetivo) ** 2


def n_maximo(anios: float, objetivo: float = 1.0) -> int:
    """Mayor N independiente tal que el máximo esperado (Sharpe real 0) no supera el objetivo con esos años."""
    n = 2
    while max_esperado(n + 1) / sqrt(anios) <= objetivo:
        n += 1
    return n


def main() -> None:
    print("Cifras del paper:")
    print(f"  N=10, 1 año: máximo esperado = {max_esperado(10):.2f} (paper: 1,57)")
    print(f"  MinBTL para N=45 y objetivo 1: {min_btl(45):.2f} años (paper: 5 años -> no más de 45)")
    print(f"  MinBTL para N=7 y objetivo 1:  {min_btl(7):.2f} años (paper: 2 años -> 7)")
    print(f"  N=128 (7 parámetros binarios): máximo esperado = {max_esperado(128):.2f} (paper: más de 2,6)")
    print(f"  Cota √(2·ln N) para N=10: {sqrt(2 * log(10)):.2f} (mayor que 1,57, como debe ser)")
    print("Aplicado a nuestro reparto (Sharpe real 0, objetivo: que el mejor no pase de Sharpe 1 por azar):")
    for anios, nombre in ((7, "bloque de investigación (7 años)"), (2, "bloque sellado (~24 meses)")):
        print(f"  {nombre}: como mucho {n_maximo(anios)} configuraciones INDEPENDIENTES")
    for n in (2000, 10000, 100000):
        print(f"  Con N={n} independientes en 7 años, el mejor tendría por azar Sharpe ≈ {max_esperado(n) / sqrt(7):.2f}")


if __name__ == "__main__":
    main()
