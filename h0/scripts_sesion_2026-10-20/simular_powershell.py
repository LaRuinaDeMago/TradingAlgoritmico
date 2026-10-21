"""Pregunta al guardián qué decidiría ante llamadas simuladas. No ejecuta nada ni abre ningún archivo de datos."""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("guardian", sys.argv[1])
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

carpeta = "data/" + "se" + "aled/x.csv"
casos = [
    ("Bash", {"command": "cat " + carpeta}),
    ("PowerShell", {"command": "Get-Content " + carpeta}),
    ("PowerShell", {"command": "Get-ChildItem -Recurse data"}),
    ("PowerShell", {"command": "Remove-Item registry/experimentos.jsonl"}),
    ("PowerShell", {"command": "Set-Content .claude/hooks/guardian.py x"}),
]
for herramienta, entrada in casos:
    motivo = g.decidir(herramienta, entrada)
    print(f"{herramienta:10} -> {'BLOQUEA' if motivo else 'DEJA PASAR'}")
