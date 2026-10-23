#!/bin/sh
# B21 (plan h0/b21_plan_archivo_banco.md): archivo de Builder/Results fuera de SQX, lectura de la copia en
# Builder/H0_archivo y prueba de no desalojo con una plantilla de trabajo de capacidad 100.000. Se para en el primer
# criterio que falle (salvo el control negativo, que TIENE que fallar).
# Uso: sh h0/configs/b21_tanda.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
LAB="C:/StrategyQuantX145/user/lab_h0"
B21="$LAB/b21"
RES="C:/StrategyQuantX145/user/projects/Builder/databanks/Results"
ARCH="C:/StrategyQuantX145/user/projects/Builder/databanks/H0_archivo"
B17_ULTIMO="$LAB/b17/Results_despues_v3_nulo2.csv"
B17_ANTERIOR="$LAB/b17/Results_despues_v3_real.csv"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "B21: los de la calibracion de B17; decision 0002"}'
# Igual que lab(), pero devuelve el código del ejecutor (2 si FALLIDO) para que set -e pare la tanda.
paso() {
  confirmar
  if PYTHONPATH=src python -m lab ejecutar --timeout 900 "$@" > "$B21/ultima_entrada.json"; then rc=0; else rc=$?; fi
  resumen < "$B21/ultima_entrada.json"; confirmar; return $rc
}
py() { paso --version-sqx N/A "$@"; }
sq() { paso --version-sqx "145.3191-dev" "$@"; }
bloques() {
  for b in Settings/Data Settings/WhatToBuild Settings/Rankings Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement; do
    printf "  %s: " "$b"; python -I h0/configs/comparar_bloque.py "$1" "$2" "$b" | tail -1
  done
}

echo "== Paso 0: SQX cerrado y manifiesto M0"
if tasklist | grep -i -E "java|strategyquant"; then echo "PARADA: SQX parece abierto; ciérralo y repite"; exit 1; fi
[ -e "$B21" ] && { echo "PARADA: $B21 ya existe; no se sobrescribe nada"; exit 1; }
mkdir -p "$B21"
cp h0/configs/b21_cargar_y_contar.txt h0/configs/Builder_original_145.3191.cfx "$B21/"
py --nombre b21_p0_manifiesto_M0 --datos "$RES" --descripcion "B21 paso 0 (A0): manifiesto M0 de Builder/Results (se esperan 7003 .sqx)" \
  -- python -I h0/configs/b21_archivo.py manifiesto "$RES" "$B21/M0_Results.json"

echo "== Paso 1: recuento y exportación de Results"
sq --nombre b21_p1_contar_results --descripcion "B21 paso 1 (A1): contar Builder/Results (se esperan 7003)" \
  -- "$SQ" -databank action=count project=Builder name=Results
sq --nombre b21_p1_exportar_results --descripcion "B21 paso 1: exportar Builder/Results a CSV" \
  -- "$SQ" -databank action=export project=Builder name=Results "file=$B21/Results_B21.csv"
py --nombre b21_p1_comparar_con_b17 --datos "$B21/Results_B21.csv" "$B17_ULTIMO" \
  --descripcion "B21 paso 1 (A2): el CSV de hoy frente al ultimo de B17 (21-10); se esperan 7003 filas IGUALES" \
  -- python -I h0/configs/b21_archivo.py csv "$B21/Results_B21.csv" "$B17_ULTIMO"

echo "== Paso 2: copia byte a byte fuera de SQX"
py --nombre b21_p2_copiar --datos "$RES" --descripcion "B21 paso 2 (A3): copiar Builder/Results a lab_h0/b21/archivo_Results con manifiesto" \
  -- python -I h0/configs/b21_archivo.py copiar "$RES" "$B21/archivo_Results"

echo "== Paso 3: lectura de la copia por SQX en Builder/H0_archivo"
py --nombre b21_p3_h0archivo_vacio --descripcion "B21 paso 3: H0_archivo antes de cargar (se espera 0 .sqx)" \
  -- python -I h0/configs/b21_archivo.py manifiesto "$ARCH" "$B21/H0_archivo_antes.json"
sq --nombre b21_p3_cargar_copia --datos "$B21/archivo_Results" "$B21/b21_cargar_y_contar.txt" \
  --descripcion "B21 paso 3 (A4): cargar la copia en Builder/H0_archivo, sincronizar y contar en el mismo proceso (se esperan 7003)" \
  -- "$SQ" -run "file=$B21/b21_cargar_y_contar.txt"
py --nombre b21_p3_h0archivo_manifiesto --descripcion "B21 paso 3 (A4): .sqx en la carpeta de H0_archivo (se esperan 7003)" \
  -- python -I h0/configs/b21_archivo.py manifiesto "$ARCH" "$B21/H0_archivo_despues.json"
sq --nombre b21_p3_exportar_h0archivo --descripcion "B21 paso 3: exportar Builder/H0_archivo a CSV" \
  -- "$SQ" -databank action=export project=Builder name=H0_archivo "file=$B21/H0_archivo_B21.csv"
py --nombre b21_p3_comparar_csv --datos "$B21/H0_archivo_B21.csv" "$B21/Results_B21.csv" \
  --descripcion "B21 paso 3 (A5): CSV de H0_archivo frente al de Results; se esperan IGUALES" \
  -- python -I h0/configs/b21_archivo.py csv "$B21/H0_archivo_B21.csv" "$B21/Results_B21.csv"
py --nombre b21_p3_control_negativo --datos "$B21/H0_archivo_B21.csv" "$B17_ANTERIOR" \
  --descripcion "B21 paso 3 (control negativo de A5): frente a un estado anterior de B17; se espera DISTINTOS (el registro lo marcara FALLIDO)" \
  -- python -I h0/configs/b21_archivo.py csv "$B21/H0_archivo_B21.csv" "$B17_ANTERIOR" || echo "  (control negativo: falló como debía)"
py --nombre b21_p3_results_intacto --descripcion "B21 paso 3 (A5b): Builder/Results sigue identico a M0" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/M0_Results.json" "$RES"
py --nombre b21_p3_diag_bytes_h0archivo --descripcion "B21 paso 3 (diagnostico, sin criterio): .sqx de H0_archivo frente a la copia, byte a byte" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/M0_Results.json" "$ARCH" || echo "  (diagnóstico: SQX reescribe los archivos al cargar)"

echo "== Paso 4: plantilla de trabajo con capacidad 100000 y generación de prueba"
python -I h0/configs/b17_preparar_builder.py h0/configs/Builder_original_145.3191.cfx "$B21/Builder_B21_capacidad.cfx" USDCHF_B1 50 | grep -E "Capacidad|spread|slippage"
sq --nombre b21_p4_loadconfig --datos "$B21/Builder_B21_capacidad.cfx" \
  --descripcion "B21 paso 4: cargar la plantilla de trabajo (USDCHF_B1, aleatoria, N=50, capacidad 100000)" \
  -- "$SQ" -project action=loadconfig name=Builder "file=$B21/Builder_B21_capacidad.cfx"
sq --nombre b21_p4_verificar --descripcion "B21 paso 4: comprobar la carga de la plantilla de trabajo" \
  -- "$SQ" -project action=saveconfig name=Builder "file=$B21/Builder_tras_carga_B21.cfx"
bloques "$B21/Builder_B21_capacidad.cfx" "$B21/Builder_tras_carga_B21.cfx"
sq --nombre b21_p4_generar --datos "C:/StrategyQuantX145/user/data/History/USDCHF_B1" "$B21/Builder_B21_capacidad.cfx" --costes "$COSTES" \
  --descripcion "B21 paso 4: generacion aleatoria de 50 estrategias con USDCHF_B1 con Results lleno (7003) y capacidad 100000" \
  -- "$SQ" -project action=start name=Builder
sq --nombre b21_p4_exportar_despues --descripcion "B21 paso 4: exportar Builder/Results tras generar" \
  -- "$SQ" -databank action=export project=Builder name=Results "file=$B21/Results_B21_despues.csv"
py --nombre b21_p4_nuevas --datos "$B21/Results_B21.csv" "$B21/Results_B21_despues.csv" \
  --descripcion "B21 paso 4 (A6): entre 50 y 57 nuevas y ninguna de antes falta" \
  -- python -I -c "import sys; sys.path.insert(0, 'h0/configs'); import b17_analizar as ba; print('nuevas:', len(ba.nuevas(sys.argv[1], sys.argv[2], 50)), '- ninguna de antes falta')" "$B21/Results_B21.csv" "$B21/Results_B21_despues.csv"
py --nombre b21_p4_conservadas --descripcion "B21 paso 4 (A7): las 7003 de M0 siguen en Results byte a byte" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/M0_Results.json" "$RES"
py --nombre b21_p4_copia_intacta --descripcion "B21 paso 4 (A8): la copia de lab_h0/b21/archivo_Results sigue identica a M0" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/M0_Results.json" "$B21/archivo_Results"

echo "== Paso 5: restaurar el Builder"
sq --nombre b21_p5_restaurar --datos "$B21/Builder_original_145.3191.cfx" --descripcion "B21 paso 5: restaurar la configuracion original del Builder" \
  -- "$SQ" -project action=loadconfig name=Builder "file=$B21/Builder_original_145.3191.cfx"
sq --nombre b21_p5_verificar --descripcion "B21 paso 5 (A9): exportar la configuracion restaurada del Builder" \
  -- "$SQ" -project action=saveconfig name=Builder "file=$B21/Builder_tras_b21.cfx"
bloques "$B21/Builder_original_145.3191.cfx" "$B21/Builder_tras_b21.cfx"
py --nombre b21_p5_manifiesto_M3 --descripcion "B21 paso 5: manifiesto final M3 de Builder/Results" \
  -- python -I h0/configs/b21_archivo.py manifiesto "$RES" "$B21/M3_Results.json"
git status --short
echo "== Fin de la tanda B21"
