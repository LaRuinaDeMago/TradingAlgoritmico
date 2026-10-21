#!/bin/sh
# Tarea 2 de H0: inspecciones registradas (la salida de cada script queda como evidencia).
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
LAB="C:/StrategyQuantX145/user/lab_h0"
PY=$(python -I -c "import sys; print(sys.executable)")
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 300 "$@" | resumen; }

confirmar
lab --nombre t2_insp_tamanos_wfo --datos "$LAB/t2" --descripcion "Tarea 2 H0: tamano de las carpetas Results/ tras WFO + What If + MC (n.59)" \
  -- "$PY" -I h0/configs/inspeccion_tamanos_resultados.py "$LAB/t2"
confirmar
lab --nombre t2_insp_tamanos_wfm --datos "$LAB/t2wfm" --descripcion "Tarea 2 H0: tamano de las carpetas Results/ tras WF Matrix (n.64)" \
  -- "$PY" -I h0/configs/inspeccion_tamanos_resultados.py "$LAB/t2wfm"
confirmar
lab --nombre t2_insp_buscar_wf --descripcion "Tarea 2 H0: donde guarda SQX los resultados de WF y What If (sin comprobaciones / WFO / WF Matrix)" \
  -- "$PY" -I h0/configs/inspeccion_buscar_wf.py "$LAB/retest1/Strategy 0.4.sqx" "$LAB/t2/Strategy 0.4.sqx" "$LAB/t2wfm/Strategy 0.4.sqx"
confirmar
lab --nombre t2_insp_extraer_wf --descripcion "Tarea 2 H0: contenido de los resultados de WFO y What If en settings.xml (Strategy 0.4, n.59)" \
  -- "$PY" -I h0/configs/inspeccion_extraer_wf.py "$LAB/t2/Strategy 0.4.sqx"
confirmar
git status --short
