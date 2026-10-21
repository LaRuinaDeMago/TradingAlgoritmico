#!/bin/sh
# B1 paso 7 (plan h0/b1_plan_integridad.md): mismo backtest de las 10 estrategias de H0 con el símbolo original
# (USDCHF_M1_dukas) y con el importado (USDCHF_B1); solo cambia el símbolo. Al final se restaura el Retester.
# Uso: sh h0/configs/b1_paso7.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
LAB="C:/StrategyQuantX145/user/lab_h0"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "los de la tarea 4; decision 0002"}'
bloques() {  # compara los bloques de configuración que importan
  for b in Settings/Data Settings/Databanks Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement Settings/Rankings; do
    printf "  %s: " "$b"; python -I h0/configs/comparar_bloque.py "$1" "$2" "$b" | tail -1
  done
}
cp h0/configs/Retester_B1_USDCHF_M1_dukas.cfx h0/configs/Retester_B1_USDCHF_B1.cfx h0/configs/Retester_original_145.3191.cfx h0/configs/b1_cargar_y_contar.txt "$B1/"

echo "== Estado del Retester antes de B1"
lab --nombre b1_p7_retester_antes --descripcion "B1 paso 7: exportar la configuracion del Retester antes de tocarlo" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_antes_b1.cfx"
bloques h0/configs/Retester_original_145.3191.cfx "$B1/Retester_antes_b1.cfx"

echo "== Banco propio y estrategias"
lab --nombre b1_p7_crear_banco --descripcion "B1 paso 7: crear el banco H0_B1 en Retester (no se tocan los bancos existentes)" \
  -- "$SQ" -databank action=create project=Retester name=H0_B1
lab --nombre b1_p7_cargar_estrategias --datos "$LAB/estrategias" \
  --descripcion "B1 paso 7: cargar en Retester/H0_B1 las 10 estrategias de H0 (registro n.24) y contarlas en el mismo proceso" \
  -- "$SQ" -run "file=$B1/b1_cargar_y_contar.txt"

for S in USDCHF_M1_dukas USDCHF_B1; do
  echo "== Backtest con $S"
  lab --nombre "b1_p7_loadconfig_$S" --datos "h0/configs/Retester_B1_$S.cfx" \
    --descripcion "B1 paso 7: cargar la plantilla del Retester con el simbolo $S" \
    -- "$SQ" -project action=loadconfig name=Retester "file=$B1/Retester_B1_$S.cfx"
  lab --nombre "b1_p7_verificar_$S" --descripcion "B1 paso 7: comprobar la carga de la plantilla $S" \
    -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_tras_carga_$S.cfx"
  bloques "h0/configs/Retester_B1_$S.cfx" "$B1/Retester_tras_carga_$S.cfx"
  if [ "$S" = USDCHF_M1_dukas ]; then D="$DATOS"; else D="C:/StrategyQuantX145/user/data/History/USDCHF_B1"; fi
  lab --nombre "b1_p7_retest_$S" --datos "$D" "h0/configs/Retester_B1_$S.cfx" --costes "$COSTES" \
    --descripcion "B1 paso 7: backtest de las 10 estrategias de Retester/H0_B1 con $S" \
    -- "$SQ" -project action=start name=Retester
  lab --nombre "b1_p7_guardar_$S" --descripcion "B1 paso 7: guardar las estrategias del backtest con $S" \
    -- "$SQ" -databank action=save project=Retester name=H0_B1 "folder=$B1/retest_$S"
  lab --nombre "b1_p7_operaciones_$S" --descripcion "B1 paso 7: operaciones del backtest con $S a CSV" \
    -- "$SQ" -tools action=orderstocsv "file=$B1/retest_$S" "output=$B1/ops_$S"
done

echo "== Restaurar el Retester"
lab --nombre b1_p7_restaurar --datos h0/configs/Retester_original_145.3191.cfx \
  --descripcion "B1 paso 7: restaurar la configuracion original del Retester" \
  -- "$SQ" -project action=loadconfig name=Retester "file=$B1/Retester_original_145.3191.cfx"
lab --nombre b1_p7_verificar_restauracion --descripcion "B1 paso 7: comprobar la restauracion del Retester" \
  -- "$SQ" -project action=saveconfig name=Retester "file=$B1/Retester_tras_b1.cfx"
bloques h0/configs/Retester_original_145.3191.cfx "$B1/Retester_tras_b1.cfx"
git status --short
