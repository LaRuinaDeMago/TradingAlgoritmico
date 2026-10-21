#!/bin/sh
# Tarea 2 de H0: ¿bloquea la prueba What If y Walk-Forward Optimization? Control positivo: MC Manipulation.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
CMP="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/comparar_bloque.py"
SQ="C:/StrategyQuantX145/sqcli.exe"
LAB="C:/StrategyQuantX145/user/lab_h0"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "decision 0002"}'
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['duracion_s'], r['incidencia'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" "$@" | resumen; }

confirmar
lab --nombre t2_loadconfig --timeout 300 --datos h0/configs/Retester_H0_USDCHF_t2_comprobaciones.cfx \
  --descripcion "Tarea 2 H0: cargar en Retester la plantilla con What If, Walk-Forward Optimization y MC Manipulation (control) activas" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$LAB/Retester_H0_USDCHF_t2_comprobaciones.cfx"
confirmar
lab --nombre t2_verificar_carga --timeout 300 --descripcion "Tarea 2 H0: comprobar la carga" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$LAB/Retester_tras_t2.cfx"
confirmar
printf "Comprobacion de la carga (CrossChecks): "
python -I "$CMP" h0/configs/Retester_H0_USDCHF_t2_comprobaciones.cfx "$LAB/Retester_tras_t2.cfx" Settings/CrossChecks | tail -1
lab --nombre t2_start --timeout 2400 --datos "C:/StrategyQuantX145/user/data/History/USDCHF_M1_dukas" --costes "$COSTES" \
  --descripcion "Tarea 2 H0: Retester con What If, Walk-Forward Optimization y MC Manipulation sobre las 10 estrategias de H0_USDCHF" \
  -- "$SQ" -project action=start name=Retester
confirmar
lab --nombre t2_guardar --timeout 300 --descripcion "Tarea 2 H0: guardar las estrategias tras las comprobaciones" \
  -- "$SQ" -databank action=save project=Retester name=H0_USDCHF "folder=$LAB/t2"
confirmar
lab --nombre t2_exportar_csv --timeout 300 --descripcion "Tarea 2 H0: exportar el banco H0_USDCHF a CSV tras las comprobaciones" \
  -- "$SQ" -databank action=export project=Retester name=H0_USDCHF "file=$LAB/t2_Results.csv"
confirmar
git status --short
