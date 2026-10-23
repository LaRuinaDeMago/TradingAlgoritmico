#!/bin/sh
# Tras la parada de B2c (plan h0/b21_plan_archivo_banco.md, escrito antes): ¿cambian las MÉTRICAS que da SQX de las
# estrategias cuyo settings.xml se reserializó? Diagnóstico sin criterio; después se retira H0_archivo como prevé B2c.
# Uso: sh h0/configs/b21c_metricas.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
B21="C:/StrategyQuantX145/user/lab_h0/b21"
ARCH="C:/StrategyQuantX145/user/projects/Builder/databanks/H0_archivo"
paso() {
  confirmar
  if PYTHONPATH=src python -m lab ejecutar --timeout 1800 "$@" > "$B21/ultima_entrada.json"; then rc=0; else rc=$?; fi
  resumen < "$B21/ultima_entrada.json"; confirmar; return $rc
}
evidencia() { python -I -c "import json,sys; print(json.load(open(sys.argv[1], encoding='utf-8'))['resultado']['evidencia'])" "$B21/ultima_entrada.json"; }
py() { paso --version-sqx N/A "$@"; }
sq() {
  paso --version-sqx "145.3191-dev" "$@"
  EV=$(evidencia)
  if grep -q -i -E "failed|memory usage" "$EV"; then echo "PARADA: $EV contiene 'failed' o 'Memory usage'"; exit 1; fi
  echo "  sin 'failed' ni 'Memory usage' en $EV"
}
if tasklist | grep -i -E "java|strategyquant|sqcli"; then echo "PARADA: SQX parece abierto"; exit 1; fi
[ -e "$B21/H0_archivo_ter" ] && { echo "PARADA: $B21/H0_archivo_ter ya existe"; exit 1; }
sq --nombre b21c_exportar_h0archivo --descripcion "Tras B2c (diagnostico): exportar H0_archivo, cuyo settings.xml SQX reserializo, a CSV" \
  -- "$SQ" -databank action=export project=Builder name=H0_archivo "file=$B21/H0_archivo_ter.csv"
py --nombre b21c_metricas_iguales --datos "$B21/H0_archivo_ter.csv" "$B21/Results_B21.csv" \
  --descripcion "Tras B2c (diagnostico): metricas de SQX de H0_archivo frente a Results_B21.csv (antes de la reserializacion)" \
  -- python -I h0/configs/b21_archivo.py csv "$B21/H0_archivo_ter.csv" "$B21/Results_B21.csv" || echo "  (las métricas difieren: ver evidencia)"
py --nombre b21c_retirar --descripcion "B2c: retirar H0_archivo a lab_h0/b21/H0_archivo_ter (copia verificada antes de quitar)" \
  -- python -I h0/configs/b21_archivo.py retirar "$ARCH" "$B21/H0_archivo_ter"
n=$(ls "$ARCH" | grep -c "\.sqx$" || true); echo "  H0_archivo al final: $n .sqx"
git status --short
