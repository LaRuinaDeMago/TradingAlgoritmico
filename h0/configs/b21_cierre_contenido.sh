#!/bin/sh
# B21, últimas comprobaciones de contenido (sin criterio nuevo): ¿vuelve settings.xml a coincidir tras otro arranque?
# Uso: sh h0/configs/b21_cierre_contenido.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
B21="C:/StrategyQuantX145/user/lab_h0/b21"
RES="C:/StrategyQuantX145/user/projects/Builder/databanks/Results"
py() { confirmar; PYTHONPATH=src python -m lab ejecutar --version-sqx N/A --timeout 1800 "$@" | resumen; confirmar; }
py --nombre b21_cierre_contenido_results --descripcion "B21: contenido de la copia frente a Results tras el arranque del n.274 (en el n.270 settings.xml difería en las 7003)" \
  -- python -I h0/configs/b21_archivo.py contenido "$B21/archivo_Results" "$RES"
py --nombre b21_cierre_contenido_ter --descripcion "B21: contenido de la copia frente a lo retirado tras B2c (H0_archivo_ter)" \
  -- python -I h0/configs/b21_archivo.py contenido "$B21/archivo_Results" "$B21/H0_archivo_ter"
git status --short
