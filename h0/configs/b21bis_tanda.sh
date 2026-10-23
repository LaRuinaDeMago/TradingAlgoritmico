#!/bin/sh
# B21-bis (plan h0/b21_plan_archivo_banco.md, enmienda escrita antes; A24 aprobado por Diego el 2026-10-23):
# 1 memoria de sqcli a 8 GiB · 2 lectura completa de la copia en Builder/H0_archivo · 3 sacarla otra vez de SQX ·
# 4 plantilla de trabajo con capacidad 100.000 y generación de 50 · 5 restaurar el Builder.
# Se para en el primer criterio que falle y en cuanto una evidencia de SQX diga "failed" o "Memory usage".
# Uso: sh h0/configs/b21bis_tanda.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
LAB="C:/StrategyQuantX145/user/lab_h0"
B21="$LAB/b21"
COPIA="$B21/archivo_Results"
RES="C:/StrategyQuantX145/user/projects/Builder/databanks/Results"
ARCH="C:/StrategyQuantX145/user/projects/Builder/databanks/H0_archivo"
CONFIG="C:/StrategyQuantX145/sqcli.config"
B17_ANTERIOR="$LAB/b17/Results_despues_v3_real.csv"
COSTES='{"spread_pips": 2, "deslizamiento_pips": 1, "comision": "ninguna", "swap": "desactivado", "motor": "MetaTrader4", "nota": "B21-bis: los de la calibracion de B17; decision 0002"}'
paso() {
  confirmar
  if PYTHONPATH=src python -m lab ejecutar --timeout 1800 "$@" > "$B21/ultima_entrada.json"; then rc=0; else rc=$?; fi
  resumen < "$B21/ultima_entrada.json"; confirmar; return $rc
}
py() { paso --version-sqx N/A "$@"; }
sq() {
  paso --version-sqx "145.3191-dev" "$@"
  EV=$(python -I -c "import json,sys; print(json.load(open(sys.argv[1], encoding='utf-8'))['resultado']['evidencia'])" "$B21/ultima_entrada.json")
  if grep -q -i -E "failed|memory usage" "$EV"; then echo "PARADA: $EV contiene 'failed' o 'Memory usage'"; grep -i -E "failed|memory usage" "$EV"; exit 1; fi
  echo "  sin 'failed' ni 'Memory usage' en $EV"
}
# La evidencia de la última entrada tiene que contener el texto exacto; si no, se para la tanda.
exige() {
  EV=$(python -I -c "import json,sys; print(json.load(open(sys.argv[1], encoding='utf-8'))['resultado']['evidencia'])" "$B21/ultima_entrada.json")
  if grep -q -F "$1" "$EV"; then echo "  cumple: '$1'"; else echo "PARADA: $EV no contiene '$1'"; exit 1; fi
}
bloques() {
  for b in Settings/Data Settings/WhatToBuild Settings/Rankings Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement; do
    printf "  %s: " "$b"; python -I h0/configs/comparar_bloque.py "$1" "$2" "$b" | tail -1
  done
}

echo "== Comprobaciones previas"
if tasklist | grep -i -E "java|strategyquant|sqcli"; then echo "PARADA: SQX parece abierto; ciérralo y repite"; exit 1; fi
for d in "$ARCH"; do n=$(ls "$d" | grep -c "\.sqx$" || true); [ "$n" = 0 ] || { echo "PARADA: $d tiene $n .sqx"; exit 1; }; done
n=$(ls "$RES" | grep -c "\.sqx$"); [ "$n" = 7003 ] || { echo "PARADA: Results tiene $n .sqx, no 7003"; exit 1; }
echo "  SQX cerrado; H0_archivo 0; Results 7003"
# Muestra la memoria de sqcli.exe cada 2 s mientras dura la tanda (para C23); se para al salir, también si hay PARADA.
rm -f "$B21/fin_muestreo"
trap 'touch "$B21/fin_muestreo"' EXIT
( while [ ! -e "$B21/fin_muestreo" ]; do tasklist /FI "IMAGENAME eq sqcli.exe" /FO CSV /NH 2>/dev/null | grep -i sqcli | sed "s/^/$(date +%H:%M:%S),/" >> "$B21/memoria_sqcli.csv"; sleep 2; done ) &

echo "== Paso 1 (B1): memoria de sqcli a 8 GiB"
py --nombre b21bis_p1_subir_memoria --datos "$CONFIG" \
  --descripcion "B21-bis paso 1 (A24, aprobado por Diego): guardar sqcli.config original en lab_h0/b21 y anadir option -Xmx8g" \
  -- python -I h0/configs/b21_memoria.py subir "$CONFIG" "$B21/sqcli.config.original" 8g
exige "intactas al principio: True"
exige "[b'option -Xmx8g']"
py --nombre b21bis_p1_medir_heap --datos "$CONFIG" --descripcion "B21-bis paso 1 (B1): memoria maxima de Java con el sqcli.config nuevo (se esperan 8,00 GiB)" \
  -- python -I h0/configs/b21_heap.py
exige "sqcli.config: opciones ['-Xms4g', '-Xmx8g'] -> MaxHeapSize 8.00 GiB"

echo "== Paso 2 (B2): lectura completa de la copia por SQX"
sq --nombre b21bis_p2_cargar_copia --datos "$COPIA" "$B21/b21_cargar_y_contar.txt" \
  --descripcion "B21-bis paso 2 (B2): cargar la copia en Builder/H0_archivo, sincronizar y contar con 8 GiB (se esperan 7003; repite la carga del n.230)" \
  -- "$SQ" -run "file=$B21/b21_cargar_y_contar.txt"
py --nombre b21bis_p2_h0archivo_manifiesto --descripcion "B21-bis paso 2 (B2): .sqx en H0_archivo (se esperan 7003)" \
  -- python -I h0/configs/b21_archivo.py manifiesto "$ARCH" "$B21/H0_archivo_bis.json"
sq --nombre b21bis_p2_exportar_h0archivo --descripcion "B21-bis paso 2 (B2): exportar H0_archivo con 14006 estrategias en el proyecto (fallo del n.232 con 4 GiB)" \
  -- "$SQ" -databank action=export project=Builder name=H0_archivo "file=$B21/H0_archivo_bis.csv"
py --nombre b21bis_p2_comparar_csv --datos "$B21/H0_archivo_bis.csv" "$B21/Results_B21.csv" \
  --descripcion "B21-bis paso 2 (B2): CSV de H0_archivo frente al de Results; se esperan 7003 filas IGUALES" \
  -- python -I h0/configs/b21_archivo.py csv "$B21/H0_archivo_bis.csv" "$B21/Results_B21.csv"
py --nombre b21bis_p2_control_negativo --datos "$B21/H0_archivo_bis.csv" "$B17_ANTERIOR" \
  --descripcion "B21-bis paso 2 (control negativo de B2): frente a un estado anterior de B17; se espera DISTINTOS (el registro lo marcara FALLIDO)" \
  -- python -I h0/configs/b21_archivo.py csv "$B21/H0_archivo_bis.csv" "$B17_ANTERIOR" || echo "  (control negativo: falló como debía)"
py --nombre b21bis_p2_contenido_h0archivo --descripcion "B21-bis paso 2 (B2): contenido de la copia presente en H0_archivo (7003)" \
  -- python -I h0/configs/b21_archivo.py contenido "$COPIA" "$ARCH"
py --nombre b21bis_p2_contenido_results --descripcion "B21-bis paso 2 (B2): contenido de la copia presente en Results (7003)" \
  -- python -I h0/configs/b21_archivo.py contenido "$COPIA" "$RES"

echo "== Paso 3 (B3): sacar otra vez H0_archivo de SQX"
py --nombre b21bis_p3_retirar_h0archivo --descripcion "B21-bis paso 3 (B3): retirar las 7003 de H0_archivo a lab_h0/b21/H0_archivo_bis (copia verificada antes de quitar)" \
  -- python -I h0/configs/b21_archivo.py retirar "$ARCH" "$B21/H0_archivo_bis"

echo "== Paso 4 (B4-B6): plantilla de trabajo con capacidad 100000 y generación de 50"
python -I h0/configs/b17_preparar_builder.py h0/configs/Builder_original_145.3191.cfx "$B21/Builder_B21_capacidad.cfx" USDCHF_B1 50 | grep -E "Capacidad|spread|slippage"
sq --nombre b21bis_p4_loadconfig --datos "$B21/Builder_B21_capacidad.cfx" \
  --descripcion "B21-bis paso 4: cargar la plantilla de trabajo (USDCHF_B1, aleatoria, N=50, capacidad 100000)" \
  -- "$SQ" -project action=loadconfig name=Builder "file=$B21/Builder_B21_capacidad.cfx"
sq --nombre b21bis_p4_verificar --descripcion "B21-bis paso 4: comprobar la carga de la plantilla de trabajo" \
  -- "$SQ" -project action=saveconfig name=Builder "file=$B21/Builder_tras_carga_B21.cfx"
bloques "$B21/Builder_B21_capacidad.cfx" "$B21/Builder_tras_carga_B21.cfx"
sq --nombre b21bis_p4_generar --datos "C:/StrategyQuantX145/user/data/History/USDCHF_B1" "$B21/Builder_B21_capacidad.cfx" --costes "$COSTES" \
  --descripcion "B21-bis paso 4: generacion aleatoria de 50 estrategias con USDCHF_B1 con Results lleno (7003) y capacidad 100000" \
  -- "$SQ" -project action=start name=Builder
sq --nombre b21bis_p4_exportar_despues --descripcion "B21-bis paso 4: exportar Builder/Results tras generar" \
  -- "$SQ" -databank action=export project=Builder name=Results "file=$B21/Results_B21_despues.csv"
py --nombre b21bis_p4_nuevas --datos "$B21/Results_B21.csv" "$B21/Results_B21_despues.csv" \
  --descripcion "B21-bis paso 4 (B4): entre 50 y 57 nuevas y ninguna de antes falta" \
  -- python -I -c "import sys; sys.path.insert(0, 'h0/configs'); import b17_analizar as ba; print('nuevas:', len(ba.nuevas(sys.argv[1], sys.argv[2], 50)), '- ninguna de antes falta')" "$B21/Results_B21.csv" "$B21/Results_B21_despues.csv"
py --nombre b21bis_p4_contenido_results --descripcion "B21-bis paso 4 (B5): contenido de las 7003 de la copia presente en Results tras generar" \
  -- python -I h0/configs/b21_archivo.py contenido "$COPIA" "$RES"
py --nombre b21bis_p4_copia_intacta --descripcion "B21-bis paso 4 (B6): la copia, byte a byte, igual a su manifiesto" \
  -- python -I h0/configs/b21_archivo.py conservadas "$B21/archivo_Results.json" "$COPIA"

echo "== Paso 5 (A9): restaurar el Builder"
sq --nombre b21bis_p5_restaurar --datos "$B21/Builder_original_145.3191.cfx" --descripcion "B21-bis paso 5: restaurar la configuracion original del Builder" \
  -- "$SQ" -project action=loadconfig name=Builder "file=$B21/Builder_original_145.3191.cfx"
sq --nombre b21bis_p5_verificar --descripcion "B21-bis paso 5 (A9): exportar la configuracion restaurada del Builder" \
  -- "$SQ" -project action=saveconfig name=Builder "file=$B21/Builder_tras_b21bis.cfx"
bloques "$B21/Builder_original_145.3191.cfx" "$B21/Builder_tras_b21bis.cfx"
py --nombre b21bis_p5_manifiesto_M3 --descripcion "B21-bis paso 5: manifiesto final M3 de Builder/Results" \
  -- python -I h0/configs/b21_archivo.py manifiesto "$RES" "$B21/M3_Results.json"
git status --short
echo "== Fin de la tanda B21-bis"
