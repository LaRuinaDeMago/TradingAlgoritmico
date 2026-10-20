#!/bin/sh
# Tarea 7 de H0: experimento completo de principio a fin, medido. Datos quemados (decisión 0002), familia H0-proceso.
#   foto de Builder/Results -> fase A (generar, restaurar Builder) -> copiar las nuevas -> fase B (operaciones,
#   backtest de reproducción en Retester/H0_T7, restaurar Retester) -> comparar operaciones.
# Cada paso pasa por `lab ejecutar` (evidencia + registro) y se confirma en git antes del siguiente.
# Uso (desde la raíz del repositorio, con la interfaz de SQX cerrada):  sh h0/configs/t7_experimento.sh MENSAJE_COMMIT
set -e
MSG="$1"
SQ="C:/StrategyQuantX145/sqcli.exe"
LAB="C:/StrategyQuantX145/user/lab_h0"
RESULTS="C:/StrategyQuantX145/user/projects/Builder/databanks/Results"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "decision 0002"}'
DATOS="C:/StrategyQuantX145/user/data/History/USDCHF_M1_dukas"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['duracion_s'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" "$@" | resumen; }

T0=$(python -I -c "import time; print(time.time())")
confirmar
lab --nombre t7v3_foto --timeout 120 --descripcion "Tarea 7 H0: nombres y tamanos de Builder/Results antes de generar" \
  -- python -I h0/configs/t7_seleccionar_nuevas.py foto "$RESULTS" "$LAB/t7/antes.json"
confirmar
lab --nombre t7v3_fase_a --timeout 1800 --datos "$DATOS" h0/configs/t7_fase_a.txt h0/configs/Builder_H0_USDCHF_minimo.cfx --costes "$COSTES" \
  --descripcion "Tarea 7 H0, fase A (un arranque): cargar plantilla minima, generar en Builder/Results, restaurar Builder" \
  -- "$SQ" -run "file=$LAB/t7_fase_a.txt"
confirmar
lab --nombre t7v3_seleccionar --timeout 120 --descripcion "Tarea 7 H0: copiar a t7/estrategias solo las 10 estrategias nuevas de Builder/Results" \
  -- python -I h0/configs/t7_seleccionar_nuevas.py copiar "$RESULTS" "$LAB/t7/antes.json" "$LAB/t7/estrategias" 10
confirmar
lab --nombre t7v3_fase_b --timeout 1800 --datos "$DATOS" h0/configs/t7_fase_b.txt h0/configs/Retester_H0_T7.cfx --costes "$COSTES" \
  --descripcion "Tarea 7 H0, fase B (un arranque): operaciones de la generacion, backtest de reproduccion en Retester/H0_T7, operaciones, restaurar Retester" \
  -- "$SQ" -run "file=$LAB/t7_fase_b.txt"
confirmar
lab --nombre t7v3_comparar --timeout 120 --descripcion "Tarea 7 H0: comparar operaciones de la generacion y del backtest de reproduccion" \
  -- python -I h0/configs/comparar_operaciones.py "$LAB/t7/ops_generacion" "$LAB/t7/ops_retest" || true
confirmar
python -I -c "import time,sys; print(f'TIEMPO TOTAL DE PRINCIPIO A FIN: {time.time()-float(sys.argv[1]):.1f} s')" "$T0"
