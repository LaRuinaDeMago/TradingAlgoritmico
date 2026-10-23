#!/bin/sh
# Diagnóstico de la parada de B2c (n.º 268), sin criterio y sin arrancar SQX. Uso: sh h0/configs/b21c_diagnostico.sh MSG
. h0/configs/b1_funciones.sh "$1"
B21="C:/StrategyQuantX145/user/lab_h0/b21"
DB="C:/StrategyQuantX145/user/projects/Builder/databanks"
py() { confirmar; PYTHONPATH=src python -m lab ejecutar --version-sqx N/A --timeout 1800 "$@" | resumen; confirmar; }
py --nombre b21c_diag_h0archivo --descripcion "B2c diagnostico: que archivo interno cambia entre la copia y H0_archivo tras reponer y arrancar SQX" \
  -- python -I h0/configs/b21_diag_contenido.py "$B21/archivo_Results" "$DB/H0_archivo"
py --nombre b21c_diag_results --descripcion "B2c diagnostico (control): copia frente a Results (en el n.261 el contenido era igual)" \
  -- python -I h0/configs/b21_diag_contenido.py "$B21/archivo_Results" "$DB/Results"
py --nombre b21c_diag_h0archivo_bis --descripcion "B2c diagnostico (control): copia frente a lo retirado en B2 (n.255; contenido igual en el n.253)" \
  -- python -I h0/configs/b21_diag_contenido.py "$B21/archivo_Results" "$B21/H0_archivo_bis"
py --nombre b21c_diag_copia_intacta --descripcion "B2c diagnostico: la copia, byte a byte, igual a su manifiesto" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/archivo_Results.json" "$B21/archivo_Results"
git status --short
