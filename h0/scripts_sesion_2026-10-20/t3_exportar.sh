#!/bin/sh
# Tareas 3c y 3d de H0: exportaciones por CLI. Cada comando por el ejecutor, con commit antes de cada uno.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
SQ="C:/StrategyQuantX145/sqcli.exe"
OUT="C:/Users/SERVILAB/Documents/TRADING ALGORITMICO/h0/evidencias_privadas/t3"
mkdir -p "h0/evidencias_privadas/t3/estrategias" "h0/evidencias_privadas/t3/operaciones"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['duracion_s'], r['evidencia'], r['redacciones'])"; }

confirmar
PYTHONPATH=src python -m lab ejecutar --nombre t3c_databank_save --version-sqx "145.3191-dev" --timeout 300 \
  --descripcion "Tarea 3c H0: exportar las estrategias de Builder/Results a una carpeta con -databank action=save (sqcli -h, registro n.9)" \
  -- "$SQ" -databank action=save project=Builder name=Results "folder=$OUT/estrategias" | resumen
confirmar
PYTHONPATH=src python -m lab ejecutar --nombre t3d_databank_export_csv --version-sqx "145.3191-dev" --timeout 300 \
  --descripcion "Tarea 3d H0: exportar el banco Builder/Results a CSV con -databank action=export (sqcli -h, registro n.9)" \
  -- "$SQ" -databank action=export project=Builder name=Results "file=$OUT/Results.csv" | resumen
confirmar
PYTHONPATH=src python -m lab ejecutar --nombre t3d_operaciones_csv --version-sqx "145.3191-dev" --timeout 300 \
  --descripcion "Tarea 3d H0: exportar las operaciones de las estrategias guardadas a CSV con -tools action=orderstocsv (sqcli -h, registro n.9)" \
  -- "$SQ" -tools action=orderstocsv "file=$OUT/estrategias" "output=$OUT/operaciones" | resumen
confirmar
git status --short
