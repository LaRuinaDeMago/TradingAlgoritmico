#!/bin/sh
# Tarea 2 de H0: experimento discriminante (solo Walk-Forward Matrix) y restauración del Retester.
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
lab --nombre t2_wfm_loadconfig --timeout 300 --datos h0/configs/Retester_H0_USDCHF_t2_wfmatrix.cfx \
  --descripcion "Tarea 2 H0 (discriminante): cargar en Retester la plantilla con solo Walk-Forward Matrix activa" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$LAB/Retester_H0_USDCHF_t2_wfmatrix.cfx"
confirmar
lab --nombre t2_wfm_verificar_carga --timeout 300 --descripcion "Tarea 2 H0 (discriminante): comprobar la carga" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$LAB/Retester_tras_t2_wfm.cfx"
confirmar
printf "Comprobacion de la carga (CrossChecks): "
python -I "$CMP" h0/configs/Retester_H0_USDCHF_t2_wfmatrix.cfx "$LAB/Retester_tras_t2_wfm.cfx" Settings/CrossChecks | tail -1
lab --nombre t2_wfm_start --timeout 2400 --datos "C:/StrategyQuantX145/user/data/History/USDCHF_M1_dukas" --costes "$COSTES" \
  --descripcion "Tarea 2 H0 (discriminante): Retester con solo Walk-Forward Matrix sobre las 10 estrategias de H0_USDCHF" \
  -- "$SQ" -project action=start name=Retester
confirmar
lab --nombre t2_wfm_guardar --timeout 300 --descripcion "Tarea 2 H0 (discriminante): guardar las estrategias tras la WF Matrix" \
  -- "$SQ" -databank action=save project=Retester name=H0_USDCHF "folder=$LAB/t2wfm"
confirmar
lab --nombre t2_retester_restaurar --timeout 300 --datos h0/configs/Retester_original_145.3191.cfx \
  --descripcion "Tarea 2 H0: dejar Retester como estaba (configuracion original)" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$LAB/Retester_original_145.3191.cfx"
confirmar
lab --nombre t2_retester_verificar_restauracion --timeout 300 --descripcion "Tarea 2 H0: comprobar la restauracion de Retester" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$LAB/Retester_tras_restaurar_t2.cfx"
confirmar
for b in Settings/Options Settings/RiskMoneyManagement Settings/Data Settings/Rankings Settings/CrossChecks Settings/Databanks; do
  printf "Restauracion %s: " $b; python -I "$CMP" h0/configs/Retester_original_145.3191.cfx "$LAB/Retester_tras_restaurar_t2.cfx" $b | tail -1
done
git status --short
