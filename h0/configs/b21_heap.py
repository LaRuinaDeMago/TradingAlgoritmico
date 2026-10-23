"""B21, diagnóstico 5: memoria máxima (heap) que tiene Java con las opciones de memoria de sqcli.config y con las de la
interfaz (StrategyQuantX.config). Usa la JVM de SQX (j64) con -version: no arranca SQX."""

import re
import subprocess
from pathlib import Path

SQX = Path("C:/StrategyQuantX145")
JAVA = SQX / "j64" / "bin" / "java.exe"


def opciones_memoria(config: Path) -> list[str]:
    return [l.split(None, 1)[1].strip() for l in config.read_text(encoding="utf-8").splitlines()
            if l.startswith("option -Xm")]


for nombre in ("sqcli.config", "StrategyQuantX.config"):
    ops = opciones_memoria(SQX / nombre)
    salida = subprocess.run([str(JAVA), *ops, "-XX:+PrintFlagsFinal", "-version"], capture_output=True, text=True)
    maximo = re.search(r"\bMaxHeapSize\s*=\s*(\d+)", salida.stdout)
    texto = f"{int(maximo.group(1)) / 2**30:.2f} GiB" if maximo else "no encontrado"
    print(f"{nombre}: opciones {ops} -> MaxHeapSize {texto}")
