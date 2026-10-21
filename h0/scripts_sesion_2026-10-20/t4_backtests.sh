#!/bin/sh
# Tarea 4 (y 3b) de H0: dos backtests independientes del Retester sobre las mismas 10 estrategias.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
SQ="C:/StrategyQuantX145/sqcli.exe"
LAB="C:/StrategyQuantX145/user/lab_h0"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "mismos que la generacion (n.23); decision 0002"}'
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['duracion_s'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 1200 "$@" | resumen; }

for k in 1 2; do
  confirmar
  lab --nombre "t4_retest_${k}_start" --datos "C:/StrategyQuantX145/user/data/History/USDCHF_M1_dukas" h0/configs/Retester_H0_USDCHF_minimo.cfx --costes "$COSTES" \
    --descripcion "Tarea 3b/4 H0: backtest $k de 2 de las 10 estrategias de Retester/H0_USDCHF con -project action=start name=Retester (decision 0002)" \
    -- "$SQ" -project action=start name=Retester
  confirmar
  lab --nombre "t4_retest_${k}_guardar" --descripcion "Tarea 4 H0: guardar las estrategias del backtest $k en una carpeta propia" \
    -- "$SQ" -databank action=save project=Retester name=H0_USDCHF "folder=$LAB/retest$k"
  confirmar
  lab --nombre "t4_retest_${k}_operaciones" --descripcion "Tarea 4 H0: operaciones del backtest $k a CSV" \
    -- "$SQ" -tools action=orderstocsv "file=$LAB/retest$k" "output=$LAB/ops$k"
done
confirmar
git status --short
