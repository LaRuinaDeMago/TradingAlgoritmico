"""A24 (aprobado por Diego el 2026-10-23): memoria máxima de Java de sqcli. `sqcli.config` trae `-Xms4g` sin `-Xmx`
(4 GiB de máximo, registro n.º 238); la interfaz (`StrategyQuantX.config`) trae `-Xmx8g`. Se añade una sola línea
`option -Xmx<valor>` al final, con el salto de línea que ya usa el archivo, tras guardar el original byte a byte.

Uso:  python -I h0/configs/b21_memoria.py subir CONFIG COPIA_DEL_ORIGINAL 8g
      python -I h0/configs/b21_memoria.py restaurar CONFIG COPIA_DEL_ORIGINAL
"""

import hashlib
import sys
from pathlib import Path


def subir(config: str | Path, copia: str | Path, valor: str) -> None:
    config, copia = Path(config), Path(copia)
    original = config.read_bytes()
    if b"-Xmx" in original:
        sys.exit(f"PARADA: {config} ya tiene -Xmx; no se toca nada")
    if copia.exists():
        if copia.read_bytes() != original:  # repetir solo vale si la copia guardada es el archivo vigente
            sys.exit(f"PARADA: {copia} ya existe y no es igual a {config}; no se sobrescribe")
    else:
        copia.parent.mkdir(parents=True, exist_ok=True)
        copia.write_bytes(original)
    if copia.read_bytes() != original:
        sys.exit("PARADA: la copia del original no es idéntica; no se toca la configuración")
    # El sqcli.config real mezcla CRLF y LF (registro n.º 244): la línea nueva usa el salto de la última línea, y si
    # el archivo no acaba en salto, se añade uno (CRLF si el archivo usa alguno).
    if original.endswith(b"\n"):
        base, salto = original, (b"\r\n" if original.endswith(b"\r\n") else b"\n")
    else:
        salto = b"\r\n" if b"\r\n" in original else b"\n"
        base = original + salto
    config.write_bytes(base + f"option -Xmx{valor}".encode("ascii") + salto)


def restaurar(config: str | Path, copia: str | Path) -> None:
    Path(config).write_bytes(Path(copia).read_bytes())


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    if argv[:1] == ["subir"] and len(argv) == 4:
        subir(argv[1], argv[2], argv[3])
    elif argv[:1] == ["restaurar"] and len(argv) == 3:
        restaurar(argv[1], argv[2])
    else:
        print(__doc__)
        return 2
    config, copia = Path(argv[1]), Path(argv[2])
    antes = copia.read_bytes().splitlines()
    ahora = config.read_bytes().splitlines()
    print(f"original: {copia} sha256 {_sha(copia)}")
    print(f"vigente:  {config} sha256 {_sha(config)}")
    print(f"lineas originales {len(antes)}, vigentes {len(ahora)}; "
          f"las originales intactas al principio: {ahora[:len(antes)] == antes}; añadidas: {ahora[len(antes):]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
