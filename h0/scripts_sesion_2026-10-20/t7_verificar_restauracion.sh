#!/bin/sh
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
CMP="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/comparar_bloque.py"
SQ="C:/StrategyQuantX145/sqcli.exe"
LAB="C:/StrategyQuantX145/user/lab_h0"
confirmar() { git add -A h0/evidencias registry; git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true; }
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); print(e['n'], e['estado'], e['codigo']['sucio'])"; }
confirmar
for p in Builder Retester; do
  PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 300 --nombre "t7v3_verificar_restauracion_$p" \
    --descripcion "Tarea 7 H0: comprobar que $p quedo con su configuracion original tras el experimento" \
    -- "$SQ" -project action=saveconfig name=$p "file=$LAB/${p}_tras_t7.cfx" | resumen
  confirmar
  for b in Settings/Options Settings/RiskMoneyManagement Settings/Data Settings/Rankings Settings/CrossChecks Settings/Databanks; do
    printf "  %s %s: " $p $b; python -I "$CMP" "h0/configs/${p}_original_145.3191.cfx" "$LAB/${p}_tras_t7.cfx" $b | tail -1
  done
done
