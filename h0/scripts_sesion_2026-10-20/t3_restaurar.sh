#!/bin/sh
# Restaurar la configuración original del Builder y comprobar que ha vuelto.
set -e
cd "/c/Users/SERVILAB/Documents/TRADING ALGORITMICO"
MSG="C:/Users/SERVILAB/AppData/Local/Temp/claude/C--Users-SERVILAB-Documents-TRADING-ALGORITMICO/d914ede8-622c-4b77-803f-a011d49f2c75/scratchpad/msg_reg.txt"
SQ="C:/StrategyQuantX145/sqcli.exe"
REPO="C:/Users/SERVILAB/Documents/TRADING ALGORITMICO"
confirmar() {
  git add -A h0/evidencias registry
  git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q -F "$MSG" || true
}
resumen() { python -I -c "import json,sys; e=json.load(sys.stdin); r=e['resultado']; print(e['n'], e['estado'], e['codigo']['sucio'], r['evidencia'])"; }

PYTHONPATH=src python -m lab ejecutar --nombre t3_builder_restaurar --version-sqx "145.3191-dev" --timeout 180 \
  --datos h0/configs/Builder_original_145.3191.cfx \
  --descripcion "Tarea 3 H0: dejar Builder como estaba, cargando su configuracion original con -project action=loadconfig" \
  -- "$SQ" -project action=loadconfig name=Builder "file=$REPO/h0/configs/Builder_original_145.3191.cfx" | resumen
confirmar
PYTHONPATH=src python -m lab ejecutar --nombre t3_builder_verificar_restauracion --version-sqx "145.3191-dev" --timeout 180 \
  --descripcion "Tarea 3 H0: comprobar la restauracion exportando otra vez la configuracion de Builder" \
  -- "$SQ" -project action=saveconfig name=Builder "file=$REPO/h0/evidencias_privadas/cfx/Builder_tras_restaurar.cfx" | resumen
confirmar
python -I -c "
import zipfile, sys, xml.etree.ElementTree as ET
def plano(f):
    r = ET.fromstring(zipfile.ZipFile(f).read('config.xml')); out=[]
    def rec(e, ruta):
        out.append((ruta, tuple(sorted(e.attrib.items())), (e.text or '').strip()))
        for i,h in enumerate(e):
            if h.tag != 'Resources': rec(h, f'{ruta}/{h.tag}[{i}]')
    rec(r, r.tag); return out
a, b = plano(sys.argv[1]), plano(sys.argv[2])
print('elementos (sin Resources):', len(a), len(b), '| diferencias:', sum(x!=y for x,y in zip(a,b)) + abs(len(a)-len(b)))
" h0/configs/Builder_original_145.3191.cfx h0/evidencias_privadas/cfx/Builder_tras_restaurar.cfx
git status --short
