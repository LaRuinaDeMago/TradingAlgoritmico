#!/bin/sh
# Tareas 3e y 3f de H0: código MT4 y MT5 por CLI, con ruta absoluta. Commit antes de cada ejecución.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
SQ="C:/StrategyQuantX145/sqcli.exe"
T3="C:/Users/SERVILAB/Documents/TRADING ALGORITMICO/h0/evidencias_privadas/t3"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['duracion_s'], r['evidencia'])"; }

confirmar
PYTHONPATH=src python -m lab ejecutar --nombre t3e_sourcecode_mt4_c --version-sqx "145.3191-dev" --timeout 300 \
  --descripcion "Tarea 3e H0: -sourcecode engine=MetaTrader4 con ruta absoluta (el n.28 mostro que las relativas se resuelven desde la carpeta de SQX)" \
  -- "$SQ" -sourcecode action=generate engine=MetaTrader4 "s=$T3/estrategias/Strategy 0.15.sqx" "o=$T3/codigo/Strategy_0.15.mq4" | resumen || true
confirmar
PYTHONPATH=src python -m lab ejecutar --nombre t3f_sourcecode_mt5 --version-sqx "145.3191-dev" --timeout 300 \
  --descripcion "Tarea 3f H0: -sourcecode engine=MetaTrader5 (mismo patron que MT4; carpeta internal/extend/Code/MetaTrader5)" \
  -- "$SQ" -sourcecode action=generate engine=MetaTrader5 "s=$T3/estrategias/Strategy 0.15.sqx" "o=$T3/codigo/Strategy_0.15.mq5" | resumen || true
confirmar
git status --short
