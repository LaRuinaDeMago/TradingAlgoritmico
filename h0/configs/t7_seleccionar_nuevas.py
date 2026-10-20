"""Tarea 7 de H0: el Builder siempre escribe en su banco Results (registros n.72–75), que ya tiene estrategias de
pruebas anteriores. Este script separa las de la generación actual sin mover ni borrar nada en SQX.

Uso:
  python -I h0/configs/t7_seleccionar_nuevas.py foto BANCO LISTA            # antes de generar: guarda los nombres
  python -I h0/configs/t7_seleccionar_nuevas.py copiar BANCO LISTA DESTINO N  # después: copia las nuevas a DESTINO

'copiar' se detiene sin copiar nada si las nuevas no son exactamente N, si alguna de antes ha desaparecido o
cambiado de tamaño, o si DESTINO no está vacío.
"""

import json
import shutil
import sys
from pathlib import Path


def foto(banco: Path) -> dict[str, int]:
    return {p.name: p.stat().st_size for p in banco.iterdir() if p.suffix == ".sqx"}


def main(orden: str, banco: str, lista: str, destino: str = "", n: str = "0") -> None:
    banco_p, lista_p = Path(banco), Path(lista)
    if orden == "foto":
        f = foto(banco_p)
        lista_p.write_text(json.dumps(f, indent=1, sort_keys=True), encoding="utf-8")
        print(f"{len(f)} estrategias antes de generar")
        return
    antes, ahora = json.loads(lista_p.read_text(encoding="utf-8")), foto(banco_p)
    desaparecidas = sorted(set(antes) - set(ahora))
    if desaparecidas:
        sys.exit(f"Han desaparecido estrategias de antes: {desaparecidas}")
    # El tamaño de las de antes puede cambiar porque SQX reescribe el banco al salir: se informa, no se detiene.
    cambiadas = sorted(k for k in antes if antes[k] != ahora[k])
    nuevas = sorted(set(ahora) - set(antes))
    if len(nuevas) != int(n):
        sys.exit(f"Se esperaban {n} estrategias nuevas y hay {len(nuevas)}: {nuevas}")
    destino_p = Path(destino)
    if any(destino_p.iterdir()):
        sys.exit(f"{destino_p} no está vacío")
    for nombre in nuevas:
        shutil.copyfile(banco_p / nombre, destino_p / nombre)
    print(f"antes: {len(antes)}; ahora: {len(ahora)}; nuevas copiadas: {len(nuevas)}; de antes con otro tamaño: {len(cambiadas)}")
    print("nuevas:", ", ".join(nuevas))


if __name__ == "__main__":
    main(*sys.argv[1:6])
