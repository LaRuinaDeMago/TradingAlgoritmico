#!/bin/sh
# Tarea 4 de H0: control negativo (spread 3 en vez de 2). Si el Retester recalcula, las operaciones deben cambiar.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
CMP="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/comparar_bloque.py"
SQ="C:/StrategyQuantX145/sqcli.exe"
LAB="C:/StrategyQuantX145/user/lab_h0"
COSTES='{"spread_pips": 3, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "CONTROL NEGATIVO: spread distinto a proposito; decision 0002"}'
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['duracion_s'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 1200 "$@" | resumen; }

confirmar
lab --nombre t4_control_loadconfig --datos h0/configs/Retester_H0_USDCHF_control_spread3.cfx \
  --descripcion "Tarea 4 H0, control negativo: cargar en Retester la plantilla identica salvo spread 3 (en vez de 2)" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$LAB/Retester_H0_USDCHF_control_spread3.cfx"
confirmar
lab --nombre t4_control_verificar_carga --descripcion "Tarea 4 H0, control negativo: comprobar la carga" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$LAB/Retester_tras_control.cfx"
confirmar
printf "Comprobacion de la carga (plantilla de control frente a lo leido): "
python -I "$CMP" h0/configs/Retester_H0_USDCHF_control_spread3.cfx "$LAB/Retester_tras_control.cfx" Settings/Data | tail -1
lab --nombre t4_control_start --datos "C:/StrategyQuantX145/user/data/History/USDCHF_M1_dukas" --costes "$COSTES" \
  --descripcion "Tarea 4 H0, control negativo: backtest con spread 3 de las mismas 10 estrategias" \
  -- "$SQ" -project action=start name=Retester
confirmar
lab --nombre t4_control_guardar --descripcion "Tarea 4 H0, control negativo: guardar estrategias" \
  -- "$SQ" -databank action=save project=Retester name=H0_USDCHF "folder=$LAB/control"
confirmar
lab --nombre t4_control_operaciones --descripcion "Tarea 4 H0, control negativo: operaciones a CSV" \
  -- "$SQ" -tools action=orderstocsv "file=$LAB/control" "output=$LAB/ops_control"
confirmar
git status --short
