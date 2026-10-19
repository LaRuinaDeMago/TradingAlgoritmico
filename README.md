# Laboratorio de Trading Algorítmico (IA + SQX)

Objetivo: averiguar con evidencia si una estrategia tiene ventaja real o es ruido. "No hay edge" es un resultado válido.

- Reglas y tareas activas: [`CLAUDE.md`](CLAUDE.md)
- Hoja de ruta: [`docs/hoja_de_ruta.md`](docs/hoja_de_ruta.md)
- Fase actual, H0: [`h0/ficha.md`](h0/ficha.md)
- Decisiones: [`docs/decisiones/`](docs/decisiones/)
- Aprendizaje (lecciones, ejercicios, glosario y diario): [`aprendizaje/`](aprendizaje/README.md)

## Puesta en marcha en el PC de SQX (Windows)

Requisitos:
- **Git for Windows** (Claude Code lo usa también para ejecutar los hooks).
- **Python 3.10+** desde python.org, marcando *Add python.exe to PATH*. Ojo: si `python` abre la Microsoft Store,
  no está bien instalado, y el guardián fallaría **sin proteger nada**.
- **Claude Code** (instalador oficial para Windows, en PowerShell: `irm https://claude.ai/install.ps1 | iex`).

```powershell
python --version                              # debe decir 3.10 o superior
git clone -b claude/proyecto-2026-fps66g https://github.com/LaRuinaDeMago/TradingAlgoritmico.git
cd TradingAlgoritmico
pip install -e .                              # o bien: $env:PYTHONPATH = "src"
python -m unittest discover -s tests          # deben pasar todos
python .claude/hooks/guardian.py --autotest   # el guardián debe dar todos "correctos"
```

Después, abrir Claude Code en esta carpeta y comprobar que el guardián bloquea de verdad
(pedirle que lea `data/sealed/prueba.txt`). Si `python` no se encuentra, el hook falla
y **no protege nada**: se arregla antes de seguir (Paso 0 de la ficha H0).

## Comandos del núcleo

```powershell
python -m lab ejecutar --nombre t1_sqcli_ayuda --version-sqx 143.2708 -- "C:\ruta\sqcli.exe" -h
python -m lab registrar --descripcion "..." --comando "MANUAL: ..." --version-sqx 143.2708 --estado INCONCLUSO --resultado "..."
python -m lab hash data/raw/archivo.csv
python -m lab verificar
```

## Estructura

```
data/raw/        datos de origen (no se suben a git; se identifican por su hash)
data/sealed/     datos finales sellados: PROHIBIDO salvo protocolo aprobado
registry/        experimentos y accesos (solo se añade)
h0/              ficha de viabilidad y evidencias
protocols/       protocolos escritos antes de cualquier examen
src/lab/         núcleo Python: rutas protegidas, hashes, registro, ejecutor
tests/           tests del núcleo y del guardián
.claude/         guardián (hook) y permisos de Claude Code
```
