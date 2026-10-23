#!/bin/sh
# B21-bis, criterio B2c (plan h0/b21_plan_archivo_banco.md, escrito antes): restauración por archivos y recuento sin
# carrera. Con SQX cerrado se repone la copia en la carpeta vacía de Builder/H0_archivo; una orden count sola; contenido;
# y se retira otra vez. Uso: sh h0/configs/b21c_tanda.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
LAB="C:/StrategyQuantX145/user/lab_h0"
B21="$LAB/b21"
COPIA="$B21/archivo_Results"
ARCH="C:/StrategyQuantX145/user/projects/Builder/databanks/H0_archivo"
RES="C:/StrategyQuantX145/user/projects/Builder/databanks/Results"
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
  if grep -q -i -E "failed|memory usage" "$EV"; then echo "PARADA: $EV contiene 'failed' o 'Memory usage'"; grep -i -E "failed|memory usage" "$EV"; exit 1; fi
  echo "  sin 'failed' ni 'Memory usage' en $EV"
}
exige() {
  EV=$(evidencia)
  if grep -q -F "$1" "$EV"; then echo "  cumple: '$1'"; else echo "PARADA: $EV no contiene '$1'"; exit 1; fi
}

echo "== Comprobaciones previas"
if tasklist | grep -i -E "java|strategyquant|sqcli"; then echo "PARADA: SQX parece abierto; ciérralo y repite"; exit 1; fi
n=$(ls "$ARCH" | grep -c "\.sqx$" || true); [ "$n" = 0 ] || { echo "PARADA: H0_archivo tiene $n .sqx"; exit 1; }
[ -e "$B21/H0_archivo_ter" ] && { echo "PARADA: $B21/H0_archivo_ter ya existe"; exit 1; }
grep -q -- "-Xmx8g" C:/StrategyQuantX145/sqcli.config || { echo "PARADA: sqcli.config sin -Xmx8g"; exit 1; }
echo "  SQX cerrado; H0_archivo 0; sqcli con 8 GiB"

echo "== B2c: reponer, contar sin carga en el mismo proceso, contenido, retirar"
py --nombre b21c_reponer --datos "$COPIA" --descripcion "B21-bis B2c: reponer la copia en la carpeta vacia de Builder/H0_archivo con SQX cerrado (restauracion por archivos)" \
  -- python -I h0/configs/b21_archivo.py reponer "$COPIA" "$ARCH"
exige "repuestas 7003"
sq --nombre b21c_contar --descripcion "B21-bis B2c: count de Builder/H0_archivo solo, sin load en el mismo proceso (se esperan 7003; control: 6747 con load en el mismo proceso, n.248)" \
  -- "$SQ" -databank action=count project=Builder name=H0_archivo
exige "Loaded 7003 strategies to databank H0_archivo"
exige "Records: 7003"
py --nombre b21c_contenido --descripcion "B21-bis B2c: contenido de la copia presente en H0_archivo tras el arranque de SQX (7003)" \
  -- python -I h0/configs/b21_archivo.py contenido "$COPIA" "$ARCH"
py --nombre b21c_retirar --descripcion "B21-bis B2c: retirar otra vez H0_archivo a lab_h0/b21/H0_archivo_ter (copia verificada antes de quitar)" \
  -- python -I h0/configs/b21_archivo.py retirar "$ARCH" "$B21/H0_archivo_ter"
n=$(ls "$ARCH" | grep -c "\.sqx$" || true); echo "  H0_archivo al final: $n .sqx"; [ "$n" = 0 ] || exit 1
n=$(ls "$RES" | grep -c "\.sqx$"); echo "  Results al final: $n .sqx"
git status --short
echo "== Fin de B2c"
