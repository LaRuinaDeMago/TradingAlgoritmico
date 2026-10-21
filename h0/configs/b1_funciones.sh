#!/bin/sh
# Funciones para B1 (plan h0/b1_plan_integridad.md). Se cargan con: . h0/configs/b1_funciones.sh MENSAJE_COMMIT
# Igual que las tandas de la tarea 4: commit antes de cada ejecución (si no, el registro marca "sucio") y todo comando
# de SQX por el ejecutor con registro.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="$1"
SQ="C:/StrategyQuantX145/sqcli.exe"
B1="C:/StrategyQuantX145/user/lab_h0/b1"
DATOS="C:/StrategyQuantX145/user/data/History/USDCHF_M1_dukas"
# Formato de comparación fijado en el plan
FORMATO="format=Custom"
CABECERA="cHeader=Date,Time,Open,High,Low,Close,Volume"
CFORMAT="cFormat=[Date:yyyy.MM.dd],[Time:HH:mm:ss],[Open],[High],[Low],[Close],[Volume]"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], 'sucio' if e['codigo']['sucio'] else 'limpio', r.get('codigo_salida'), r.get('duracion_s'), r.get('evidencia'))"; }
lab() { confirmar; PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 900 "$@" | resumen; confirmar; }
