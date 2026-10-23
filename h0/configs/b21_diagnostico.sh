#!/bin/sh
# B21, diagnóstico tras la parada en A5 (registro n.º 233). Solo Python y la JVM de SQX con -version: no arranca SQX
# ni toca ningún banco. Uso: sh h0/configs/b21_diagnostico.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
LAB="C:/StrategyQuantX145/user/lab_h0"
B21="$LAB/b21"
RES="C:/StrategyQuantX145/user/projects/Builder/databanks/Results"
ARCH="C:/StrategyQuantX145/user/projects/Builder/databanks/H0_archivo"
py() { lab_py "$@"; }
lab_py() {
  confirmar
  if PYTHONPATH=src python -m lab ejecutar --timeout 900 --version-sqx N/A "$@" > "$B21/ultima_entrada.json"; then rc=0; else rc=$?; fi
  resumen < "$B21/ultima_entrada.json"; confirmar; return 0
}
py --nombre b21_d1_results_bytes --descripcion "B21 diagnostico 1: Builder/Results frente a M0 byte a byte tras los arranques de SQX (se espera que SQX haya reescrito los zip)" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/M0_Results.json" "$RES"
py --nombre b21_d2_copia_intacta --descripcion "B21 diagnostico 2: la copia lab_h0/b21/archivo_Results frente a su propio manifiesto (no la toca SQX)" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/archivo_Results.json" "$B21/archivo_Results"
py --nombre b21_d3_contenido_results --descripcion "B21 diagnostico 3: contenido (archivos internos, sin fechas) de la copia frente a Builder/Results" \
  -- python -I h0/configs/b21_archivo.py contenido "$B21/archivo_Results" "$RES"
py --nombre b21_d4_contenido_h0archivo --descripcion "B21 diagnostico 4: contenido de las 6406 de H0_archivo frente a la copia (que las cargadas sean iguales)" \
  -- python -I h0/configs/b21_archivo.py contenido "$ARCH" "$B21/archivo_Results"
py --nombre b21_d5_heap_sqcli --datos "C:/StrategyQuantX145/sqcli.config" "C:/StrategyQuantX145/StrategyQuantX.config" \
  --descripcion "B21 diagnostico 5: memoria maxima de Java con las opciones de sqcli.config (-Xms4g, sin -Xmx) frente a la interfaz (-Xmx8g)" \
  -- python -I h0/configs/b21_heap.py
git status --short
