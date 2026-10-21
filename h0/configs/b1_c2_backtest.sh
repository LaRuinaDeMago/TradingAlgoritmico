#!/bin/sh
# B1 control C2, ampliación: ¿la zona horaria declarada (solo una etiqueta: las horas no cambian) altera el backtest?
# Mismo procedimiento que b1_paso7.sh con el símbolo USDCHF_B1_TZ (importado con Etc/UCT). Al final se restaura.
# Uso: sh h0/configs/b1_c2_backtest.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
S=USDCHF_B1_TZ
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "los de la tarea 4; decision 0002"}'
bloques() {
  for b in Settings/Data Settings/Databanks Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement Settings/Rankings; do
    printf "  %s: " "$b"; python -I h0/configs/comparar_bloque.py "$1" "$2" "$b" | tail -1
  done
}
cp "h0/configs/Retester_B1_$S.cfx" "$B1/"
lab --nombre "b1_c2_loadconfig_$S" --datos "h0/configs/Retester_B1_$S.cfx" \
  --descripcion "B1 control C2: cargar la plantilla del Retester con $S" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$B1/Retester_B1_$S.cfx"
lab --nombre "b1_c2_verificar_$S" --descripcion "B1 control C2: comprobar la carga de la plantilla $S" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_tras_carga_$S.cfx"
bloques "h0/configs/Retester_B1_$S.cfx" "$B1/Retester_tras_carga_$S.cfx"
lab --nombre "b1_c2_retest_$S" --datos "C:/StrategyQuantX145/user/data/History/$S" "h0/configs/Retester_B1_$S.cfx" --costes "$COSTES" \
  --descripcion "B1 control C2: backtest de las 10 estrategias de Retester/H0_B1 con $S" \
  -- "$SQ" -project action=start name=Retester
lab --nombre "b1_c2_guardar_$S" --descripcion "B1 control C2: guardar las estrategias del backtest con $S" \
  -- "$SQ" -databank action=save project=Retester name=H0_B1 "folder=$B1/retest_$S"
lab --nombre "b1_c2_operaciones_$S" --descripcion "B1 control C2: operaciones del backtest con $S a CSV" \
  -- "$SQ" -tools action=orderstocsv "file=$B1/retest_$S" "output=$B1/ops_$S"
lab --nombre b1_c2_restaurar --datos h0/configs/Retester_original_145.3191.cfx \
  --descripcion "B1 control C2: restaurar la configuracion original del Retester" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$B1/Retester_original_145.3191.cfx"
lab --nombre b1_c2_verificar_restauracion --descripcion "B1 control C2: comprobar la restauracion del Retester" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_tras_c2.cfx"
bloques h0/configs/Retester_original_145.3191.cfx "$B1/Retester_tras_c2.cfx"
git status --short
