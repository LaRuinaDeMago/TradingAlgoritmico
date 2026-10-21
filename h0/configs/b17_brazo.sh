#!/bin/sh
# B17 (plan h0/b17_plan_control_negativo.md): genera un brazo. Exporta Builder/Results antes, carga y comprueba la
# plantilla del símbolo, genera N estrategias y exporta Results después. Las nuevas se separan en el análisis por nombre.
# Uso: sh h0/configs/b17_brazo.sh MENSAJE_COMMIT ETIQUETA SIMBOLO N
. h0/configs/b1_funciones.sh "$1"
ETQ="$2"; S="$3"; N="$4"
B17="C:/StrategyQuantX145/user/lab_h0/b17"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "los de H0; decision 0002"}'
python -I h0/configs/b17_preparar_builder.py h0/configs/Builder_original_145.3191.cfx "$B17/Builder_B17_$ETQ.cfx" "$S" "$N" | tail -1
lab --nombre "b17_${ETQ}_banco_antes" --descripcion "B17 $ETQ: exportar Builder/Results antes de generar" \
  -- "$SQ" -databank action=export project=Builder name=Results "file=$B17/Results_antes_$ETQ.csv"
lab --nombre "b17_${ETQ}_loadconfig" --datos "$B17/Builder_B17_$ETQ.cfx" \
  --descripcion "B17 $ETQ: cargar la plantilla del Builder ($S, N=$N, OOS 2024.04.01-2024.10.30)" \
  -- "$SQ" -project action=loadconfig name=Builder "file=$B17/Builder_B17_$ETQ.cfx"
lab --nombre "b17_${ETQ}_verificar" --descripcion "B17 $ETQ: comprobar la carga de la plantilla" \
  -- "$SQ" -project action=saveconfig name=Builder "file=$B17/Builder_tras_carga_$ETQ.cfx"
for b in Settings/Data Settings/WhatToBuild Settings/Rankings Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement; do
  printf "  %s: " "$b"; python -I h0/configs/comparar_bloque.py "$B17/Builder_B17_$ETQ.cfx" "$B17/Builder_tras_carga_$ETQ.cfx" "$b" | tail -1
done
lab --nombre "b17_${ETQ}_generar" --datos "C:/StrategyQuantX145/user/data/History/$S" "$B17/Builder_B17_$ETQ.cfx" --costes "$COSTES" \
  --descripcion "B17 $ETQ: generacion aleatoria de $N estrategias con $S (sin filtros: se guardan todas)" \
  -- "$SQ" -project action=start name=Builder
lab --nombre "b17_${ETQ}_banco_despues" --descripcion "B17 $ETQ: exportar Builder/Results despues de generar" \
  -- "$SQ" -databank action=export project=Builder name=Results "file=$B17/Results_despues_$ETQ.csv"
git status --short
