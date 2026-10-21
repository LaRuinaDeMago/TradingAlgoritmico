"""B17: serie M1 sintética SIN ventaja a partir de una exportación real (control negativo de la búsqueda).

Uso:  python -I h0/configs/b17_sintetico.py E_A.csv SALIDA_MT4.csv SEMILLA
      (escribe también SALIDA_MT4.custom.csv, en el formato de comparación de B1)

Entrada: formato Custom de B1 (cabecera Date,Time,Open,High,Low,Close,Volume). Salida: "MetaTrader4 bar format" sin
cabecera (yyyy.MM.dd,HH:mm,O,H,L,C,V), el que `sqcli -data action=import` acepta (B1, registro n.º 102).

Método: cada vela t ≥ 1 se descompone en su forma u_t = (salto desde el cierre anterior, máximo, mínimo y cierre
relativos a su apertura, en logaritmos; volumen). Las formas se barajan con la semilla y se recompone la serie con las
mismas horas. Al salto se le resta la media del rendimiento por vela, para que la deriva total sea cero: no queda
tendencia ni dependencia temporal que explotar, y el reparto de movimientos por vela es exactamente el real.
Coherencia OHLC: máximo, mínimo y cierre son relativos a la apertura de su vela y el redondeo es monótono, así que
H ≥ max(O, C) y L ≤ min(O, C) se conservan.
"""

import math
import random
import sys
from datetime import datetime
from pathlib import Path

DECIMALES = 5


def leer(ruta: str | Path) -> list[tuple[datetime, float, float, float, float, str]]:
    lineas = Path(ruta).read_text(encoding="utf-8").splitlines()
    if lineas[0].strip() != "Date,Time,Open,High,Low,Close,Volume":
        raise ValueError(f"{ruta}: cabecera inesperada {lineas[0]!r}")
    velas = []
    for linea in lineas[1:]:
        if not linea:
            continue
        d, t, o, h, l, c, v = linea.split(",")
        velas.append((datetime.strptime(f"{d} {t}", "%Y.%m.%d %H:%M:%S"), float(o), float(h), float(l), float(c), v))
    return velas


def formas(velas) -> list[tuple[float, float, float, float, str]]:
    return [(math.log(o / velas[i - 1][4]), math.log(h / o), math.log(l / o), math.log(c / o), v)
            for i, (_, o, h, l, c, v) in enumerate(velas) if i > 0]


def sintetizar(velas, semilla: int):
    """Devuelve velas sintéticas con las mismas horas, formas barajadas y deriva cero."""
    piezas = formas(velas)
    media = sum(g + c for g, _, _, c, _ in piezas) / len(piezas)
    random.Random(semilla).shuffle(piezas)
    salida = [velas[0]]
    cierre = velas[0][4]
    for (momento, *_), (g, h, l, c, v) in zip(velas[1:], piezas):
        o = cierre * math.exp(g - media)
        cierre = o * math.exp(c)
        salida.append((momento, o, o * math.exp(h), o * math.exp(l), cierre, v))
    return salida


def escribir_mt4(velas, ruta: str | Path) -> None:
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        for momento, o, h, l, c, v in velas:
            precios = ",".join(f"{x:.{DECIMALES}f}" for x in (o, h, l, c))
            f.write(f"{momento:%Y.%m.%d},{momento:%H:%M},{precios},{v}\n")


def escribir_custom(velas, ruta: str | Path) -> None:
    """Misma serie en el formato de comparación de B1, para comprobar la importación con b1_comparar_velas.py."""
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write("Date,Time,Open,High,Low,Close,Volume\n")
        for momento, o, h, l, c, v in velas:
            precios = ",".join(f"{x:.{DECIMALES}f}" for x in (o, h, l, c))
            f.write(f"{momento:%Y.%m.%d},{momento:%H:%M:%S},{precios},{v}\n")


def main(entrada: str, salida: str, semilla: str) -> None:
    velas = leer(entrada)
    sint = sintetizar(velas, int(semilla))
    escribir_mt4(sint, salida)
    escribir_custom(sint, Path(salida).with_suffix(".custom.csv"))
    deriva = math.log(sint[-1][4] / sint[0][4])
    print(f"velas: {len(sint)} · semilla: {semilla} · cierre inicial {sint[0][4]:.5f} · final {sint[-1][4]:.5f} · "
          f"deriva log total (debe ser ~0 salvo la primera vela): {deriva:.6f}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
