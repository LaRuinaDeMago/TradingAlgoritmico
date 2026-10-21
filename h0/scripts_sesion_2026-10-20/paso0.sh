#!/bin/sh
# Paso 0 con registro: cada comando por el ejecutor, con commit antes de cada uno.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG"
}
lab() { PYTHONPATH=src python -m lab "$@" | python -I -c "import json,sys; e=json.load(sys.stdin); print(e['n'], e['estado'], e['codigo']['sucio'], e['resultado']['evidencia'])"; }

confirmar
lab ejecutar --nombre p0_python_version --version-sqx N/A --timeout 60 -- python --version
confirmar
lab ejecutar --nombre p0_unittest --version-sqx N/A --timeout 300 -- python -m unittest discover -s tests -v
confirmar
lab ejecutar --nombre p0_guardian_autotest --version-sqx N/A --timeout 60 -- python .claude/hooks/guardian.py --autotest
confirmar
git log --oneline -1
git status --short
