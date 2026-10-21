#!/bin/sh
# Tarea 4 de H0: preparar el Retester (banco propio, plantilla mínima, estrategias). Commit antes de cada ejecución.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
CMP="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/comparar_bloque.py"
SQ="C:/StrategyQuantX145/sqcli.exe"
LAB="/c/StrategyQuantX145/user/lab_h0"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['evidencia'])"; }
lab() { PYTHONPATH=src python -m lab ejecutar --version-sqx "145.3191-dev" --timeout 300 "$@" | resumen; }

# Archivos de intercambio dentro de la carpeta de SQX (rutas relativas, sin el usuario de Windows)
mkdir -p "$LAB/estrategias"
python -I -c "import shutil,glob,os,sys
shutil.copyfile('h0/configs/Retester_H0_USDCHF_minimo.cfx', sys.argv[1]+'/Retester_H0_USDCHF_minimo.cfx')
for f in glob.glob('h0/evidencias/t3_salidas/estrategias/*.sqx'): shutil.copyfile(f, sys.argv[1]+'/estrategias/'+os.path.basename(f))
print('copiados', len(os.listdir(sys.argv[1]+'/estrategias')))" "C:/StrategyQuantX145/user/lab_h0"

confirmar
lab --nombre t4_retester_crear_banco --descripcion "Tarea 4 H0: crear un banco propio H0_USDCHF en Retester (el banco Results tiene 7 estrategias de ejemplo de SQX que no se tocan)" \
  -- "$SQ" -databank action=create project=Retester name=H0_USDCHF
confirmar
lab --nombre t4_retester_loadconfig --datos h0/configs/Retester_H0_USDCHF_minimo.cfx \
  --descripcion "Tarea 4 H0: cargar la plantilla minima (decision 0002, banco H0_USDCHF) en Retester" \
  -- "$SQ" -project action=loadconfig name=Retester file=user/lab_h0/Retester_H0_USDCHF_minimo.cfx
confirmar
lab --nombre t4_retester_verificar_carga --descripcion "Tarea 4 H0: comprobar la carga exportando otra vez la configuracion de Retester" \
  -- "$SQ" -project action=saveconfig name=Retester file=user/lab_h0/Retester_tras_carga.cfx
confirmar
for b in Settings/Data Settings/Databanks Settings/CrossChecks Settings/Options Settings/RiskMoneyManagement; do
  printf "%s: " "$b"; python -I "$CMP" h0/configs/Retester_H0_USDCHF_minimo.cfx "C:/StrategyQuantX145/user/lab_h0/Retester_tras_carga.cfx" "$b" | tail -1
done
lab --nombre t4_retester_cargar_estrategias --datos h0/evidencias/t3_salidas/estrategias \
  --descripcion "Tarea 4 H0: cargar en Retester/H0_USDCHF las 10 estrategias exportadas en el registro n.24" \
  -- "$SQ" -databank action=load project=Retester name=H0_USDCHF folder=user/lab_h0/estrategias
confirmar
lab --nombre t4_retester_contar --descripcion "Tarea 4 H0: contar las estrategias de Retester/H0_USDCHF tras cargarlas" \
  -- "$SQ" -databank action=count project=Retester name=H0_USDCHF
confirmar
git status --short
