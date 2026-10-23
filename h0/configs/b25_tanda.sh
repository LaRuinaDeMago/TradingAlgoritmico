#!/bin/sh
# B25 (plan h0/b25_plan_restauracion.md): restauración del análisis de B17 v3 (n.º 221) desde clones de GitHub.
# Uso: sh h0/configs/b25_tanda.sh MENSAJE_COMMIT CARPETA_DE_TRABAJO
. h0/configs/b1_funciones.sh "$1"
TRABAJO="$2"
URL="https://github.com/LaRuinaDeMago/TradingAlgoritmico.git"
RAMA="claude/proyecto-2026-fps66g"
[ -e "$TRABAJO/clon_head" ] && { echo "PARADA: $TRABAJO/clon_head ya existe"; exit 1; }
git clone -q --branch "$RAMA" "$URL" "$TRABAJO/clon_head"
git clone -q "$TRABAJO/clon_head" "$TRABAJO/clon_221"
git -C "$TRABAJO/clon_221" -c advice.detachedHead=false checkout -q 65e9a572f508f9f1318201b6910f2aa4bb9dc93b
echo "clon de GitHub en $(git -C "$TRABAJO/clon_head" rev-parse --short HEAD); clon de código en $(git -C "$TRABAJO/clon_221" rev-parse --short HEAD)"
confirmar
PYTHONPATH=src python -m lab ejecutar --version-sqx N/A --timeout 600 --nombre b25_restaurar_b17v3 \
  --datos "$TRABAJO/clon_head/registry/experimentos.jsonl" \
  --descripcion "B25: restauracion del analisis de B17 v3 (n.221) desde clones de GitHub y datos en lab_h0/b17 (R1 commit, R2 hashes, R3 salida byte a byte)" \
  -- python -I h0/configs/b25_restaurar.py "$TRABAJO/clon_head/registry/experimentos.jsonl" 221 "$TRABAJO/clon_221" "$TRABAJO/clon_head/h0/evidencias" | resumen
confirmar
git status --short
