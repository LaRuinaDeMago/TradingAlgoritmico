#!/bin/sh
# Tarea 7 de H0: dejar vacío Builder/Results moviendo sus 30 estrategias (todas H0-proceso) a H0_archivo. No se borra nada.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
SQ="C:/StrategyQuantX145/sqcli.exe"
confirmar() {
  git add -A h0/evidencias registry h0/configs
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 300 "$@" | resumen; }

python -I -c "import shutil; shutil.copyfile('h0/configs/t7_archivar_results.txt','C:/StrategyQuantX145/user/lab_h0/t7_archivar_results.txt')"
confirmar
lab --nombre t7_crear_archivo --descripcion "Tarea 7 H0: crear el banco H0_archivo en Builder (arranque propio, para que exista antes de usarlo)" \
  -- "$SQ" -databank action=create project=Builder name=H0_archivo
confirmar
lab --nombre t7_archivar_results --datos h0/configs/t7_archivar_results.txt \
  --descripcion "Tarea 7 H0: mover las 30 estrategias de Builder/Results (todas H0-proceso: n.23, 72, 74) a H0_archivo; no se borra nada" \
  -- "$SQ" -run file=C:/StrategyQuantX145/user/lab_h0/t7_archivar_results.txt
confirmar
for b in Results H0_archivo; do echo "disco Builder/$b: $(ls "/c/StrategyQuantX145/user/projects/Builder/databanks/$b" | wc -l) archivos"; done
git status --short
