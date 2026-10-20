"""Reproduce el ejemplo numérico de Bailey y López de Prado (2014), "The Deflated Sharpe Ratio", págs. 9–10.

Objetivo: comprobar que entendemos la ecuación 2 antes de usarla. No forma parte del motor del laboratorio (regla C10).
Solo biblioteca estándar (numpy no está instalado; asunto A18).

Datos del ejemplo (pág. 9): N = 100 pruebas independientes, V[{SR_n}] = 1/2 (anualizado), T = 1250 observaciones
diarias (5 años, 250 por año), asimetría = -3, curtosis = 10, SR seleccionado = 2.5 anualizado.
Resultados del paper (pág. 10): SR_0 ≈ 0.1132 (no anualizado), DSR ≈ 0.9004; con N = 46, DSR ≈ 0.9505;
con rendimientos normales (asimetría 0, curtosis 3), DSR ≈ 0.9505 tras N = 88.
"""

from math import e, sqrt
from statistics import NormalDist

Z = NormalDist()
GAMMA = 0.5772156649  # constante de Euler-Mascheroni


def sr0(varianza_srs: float, n: int) -> float:
    """Máximo esperado del Sharpe entre n pruebas independientes si el Sharpe real es 0 (ecuación 1, con media 0)."""
    return sqrt(varianza_srs) * ((1 - GAMMA) * Z.inv_cdf(1 - 1 / n) + GAMMA * Z.inv_cdf(1 - 1 / (n * e)))


def dsr(sr: float, sr_0: float, t: int, asimetria: float, curtosis: float) -> float:
    """Deflated Sharpe Ratio (ecuación 2): probabilidad de que el Sharpe real supere sr_0."""
    return Z.cdf((sr - sr_0) * sqrt(t - 1) / sqrt(1 - asimetria * sr + (curtosis - 1) / 4 * sr ** 2))


def main() -> None:
    dias = 250
    var_diaria = 0.5 / dias          # V[{SR}] = 1/2 anualizado -> no anualizado
    sr_diario = 2.5 / sqrt(dias)     # SR = 2.5 anualizado -> no anualizado
    t = 1250
    casos = [
        ("Ejemplo base (N=100, asim. -3, curt. 10)", 100, -3, 10, 0.1132, 0.9004),
        ("Mismo con N=46", 46, -3, 10, None, 0.9505),
        ("Rendimientos normales, N=88", 88, 0, 3, None, 0.9505),
    ]
    for nombre, n, g3, g4, sr0_paper, dsr_paper in casos:
        s0 = sr0(var_diaria, n)
        d = dsr(sr_diario, s0, t, g3, g4)
        print(f"{nombre}: SR0={s0:.4f}" + (f" (paper {sr0_paper})" if sr0_paper else "")
              + f" | DSR={d:.4f} (paper {dsr_paper}) | diferencia={abs(d - dsr_paper):.4f}")


if __name__ == "__main__":
    main()
