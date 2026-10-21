#!/bin/sh
# B1-bis (h0/b1_resultados.md): mismo backtest con inicio 2023.02.01 (un mes de margen de calentamiento) con el símbolo
# original y con el importado. Criterio A5-bis fijado antes de ejecutar. Al final se restaura el Retester.
# Uso: sh h0/configs/b1bis.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "los de la tarea 4; decision 0002"}'
bloques() {
  for b in Settings/Data Settings/Databanks Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement Settings/Rankings; do
    printf "  %s: " "$b"; python -I h0/configs/comparar_bloque.py "$1" "$2" "$b" | tail -1
  done
}
for S in USDCHF_M1_dukas USDCHF_B1; do
  cp "h0/configs/Retester_B1bis_$S.cfx" "$B1/"
  lab --nombre "b1bis_loadconfig_$S" --datos "h0/configs/Retester_B1bis_$S.cfx" \
    --descripcion "B1-bis: cargar la plantilla con inicio 2023.02.01 y simbolo $S" \
    -- "$SQ" -project action=loadconfig name=Retester "file=$B1/Retester_B1bis_$S.cfx"
  lab --nombre "b1bis_verificar_$S" --descripcion "B1-bis: comprobar la carga de la plantilla $S" \
    -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_tras_carga_bis_$S.cfx"
  bloques "h0/configs/Retester_B1bis_$S.cfx" "$B1/Retester_tras_carga_bis_$S.cfx"
  if [ "$S" = USDCHF_M1_dukas ]; then D="$DATOS"; else D="C:/StrategyQuantX145/user/data/History/USDCHF_B1"; fi
  lab --nombre "b1bis_retest_$S" --datos "$D" "h0/configs/Retester_B1bis_$S.cfx" --costes "$COSTES" \
    --descripcion "B1-bis: backtest de las 10 estrategias de Retester/H0_B1 con $S desde 2023.02.01" \
    -- "$SQ" -project action=start name=Retester
  lab --nombre "b1bis_guardar_$S" --descripcion "B1-bis: guardar las estrategias del backtest con $S" \
    -- "$SQ" -databank action=save project=Retester name=H0_B1 "folder=$B1/retest_bis_$S"
  lab --nombre "b1bis_operaciones_$S" --descripcion "B1-bis: operaciones del backtest con $S a CSV" \
    -- "$SQ" -tools action=orderstocsv "file=$B1/retest_bis_$S" "output=$B1/ops_bis_$S"
done
lab --nombre b1bis_restaurar --datos h0/configs/Retester_original_145.3191.cfx \
  --descripcion "B1-bis: restaurar la configuracion original del Retester" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$B1/Retester_original_145.3191.cfx"
lab --nombre b1bis_verificar_restauracion --descripcion "B1-bis: comprobar la restauracion del Retester" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_tras_b1bis.cfx"
bloques h0/configs/Retester_original_145.3191.cfx "$B1/Retester_tras_b1bis.cfx"
PYTHONPATH=src python -m lab ejecutar --nombre b1bis_a5bis_comparar --version-sqx N/A --datos h0/configs/b1_diagnostico_operaciones.py \
  --descripcion "B1-bis criterio A5-bis: operaciones con USDCHF_M1_dukas frente a USDCHF_B1, ambos desde 2023.02.01" \
  -- python -I h0/configs/b1_diagnostico_operaciones.py "$B1/ops_bis_USDCHF_M1_dukas" "$B1/ops_bis_USDCHF_B1" | resumen
confirmar
git status --short
