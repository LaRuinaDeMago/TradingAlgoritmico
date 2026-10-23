"""B21 (plan h0/b21_plan_archivo_banco.md): archivo de un banco de SQX fuera de SQX, con hash archivo a archivo.

Un banco del Builder es una carpeta de archivos .sqx (user/projects/Builder/databanks/<banco>/). Se copia byte a byte
con Python (sin pasar por SQX), se hace un manifiesto (nombre, bytes, SHA-256) del origen y de la copia y se comparan.
También compara dos exportaciones CSV de un banco (`-databank action=export`) como multiconjunto de filas.

Uso (desde la raíz, por el ejecutor con registro):
  python -I h0/configs/b21_archivo.py manifiesto CARPETA SALIDA.json
  python -I h0/configs/b21_archivo.py copiar ORIGEN DESTINO          (DESTINO no debe existir; escribe DESTINO.json)
  python -I h0/configs/b21_archivo.py retirar BANCO DESTINO   (copia verificada y, si es idéntica, vacía BANCO)
  python -I h0/configs/b21_archivo.py reponer COPIA BANCO_VACIO   (restauración: copia la copia en el banco vacío)
  python -I h0/configs/b21_archivo.py conservadas ANTES.json CARPETA (¿siguen todas las de ANTES, idénticas?)
  python -I h0/configs/b21_archivo.py contenido CARPETA_A CARPETA_B  (¿están todas las de A en B con el mismo CONTENIDO?)
  python -I h0/configs/b21_archivo.py csv A.csv B.csv
Sale con código 1 si una comprobación falla.
"""

import collections
import hashlib
import json
import shutil
import sys
import zipfile
from pathlib import Path


def _sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def manifiesto(carpeta: str | Path) -> dict[str, dict]:
    carpeta = Path(carpeta)
    if not carpeta.is_dir():
        sys.exit(f"PARADA: {carpeta} no es una carpeta")
    if any(p.is_dir() for p in carpeta.iterdir()):
        sys.exit(f"PARADA: {carpeta} tiene subcarpetas; un banco no debería tenerlas")
    return {p.name: {"bytes": p.stat().st_size, "sha256": _sha256(p)}
            for p in sorted(carpeta.iterdir()) if p.suffix == ".sqx"}


def _sha256_contenido(ruta: Path) -> str:
    """Hash del CONTENIDO de un .sqx (un zip): nombre y bytes de cada archivo interno, sin fechas ni compresión.
    SQX reescribe el zip en cada arranque con la fecha del momento (B21, registro n.º 225), así que el hash del archivo
    cambia aunque la estrategia sea la misma."""
    h = hashlib.sha256()
    with zipfile.ZipFile(ruta) as z:
        for nombre in sorted(z.namelist()):
            h.update(nombre.encode("utf-8") + b"\0" + hashlib.sha256(z.read(nombre)).digest())
    return h.hexdigest()


def manifiesto_contenido(carpeta: str | Path) -> dict[str, dict]:
    carpeta = Path(carpeta)
    m = manifiesto(carpeta)
    return {n: {"contenido": _sha256_contenido(carpeta / n)} for n in m}


def comparar(a: dict, b: dict) -> dict[str, list[str]]:
    return {"faltan": sorted(set(a) - set(b)), "sobran": sorted(set(b) - set(a)),
            "distintos": sorted(n for n in set(a) & set(b) if a[n] != b[n])}


def conservadas(antes: dict, despues: dict) -> bool:
    """Todas las de antes siguen, byte a byte; puede haber nuevas."""
    r = comparar(antes, despues)
    return not r["faltan"] and not r["distintos"]


def copiar(origen: str | Path, destino: str | Path) -> dict:
    origen, destino = Path(origen), Path(destino)
    if destino.exists():
        sys.exit(f"PARADA: {destino} ya existe; no se sobrescribe nada")
    m_origen = manifiesto(origen)
    destino.mkdir(parents=True)
    for nombre in m_origen:
        shutil.copy2(origen / nombre, destino / nombre)
    m_destino = manifiesto(destino)
    m_origen_despues = manifiesto(origen)  # el origen no debe cambiar mientras se copia
    return {"n": len(m_origen), "bytes": sum(e["bytes"] for e in m_origen.values()),
            "comparacion": comparar(m_origen, m_destino),
            "origen_estable": m_origen == m_origen_despues, "manifiesto": m_origen}


def retirar(origen: str | Path, destino: str | Path) -> dict:
    """Saca un banco de SQX (con SQX cerrado): copia verificada a DESTINO y, solo si es idéntica, quita los .sqx del
    origen. B21-bis: un banco que no cabe en memoria lo borra SQX al salir; uno que no está en la carpeta no se carga."""
    r = copiar(origen, destino)
    if any(r["comparacion"].values()) or not r["origen_estable"]:
        sys.exit(f"PARADA: la copia en {destino} no es idéntica; no se quita nada del origen")
    for nombre in r["manifiesto"]:
        (Path(origen) / nombre).unlink()
    r["quedan"] = len(manifiesto(origen))
    return r


def reponer(copia: str | Path, banco: str | Path) -> dict:
    """Restauración (con SQX cerrado): copia los .sqx de una copia de archivo en la carpeta VACÍA de un banco y comprueba
    que quedan byte a byte iguales. Al arrancar, SQX sincroniza el banco desde sus archivos (B21-bis, B2c)."""
    copia, banco = Path(copia), Path(banco)
    if not banco.is_dir() or any(banco.glob("*.sqx")):
        sys.exit(f"PARADA: {banco} no es una carpeta de banco vacía; no se repone nada")
    m_copia = manifiesto(copia)
    for nombre in m_copia:
        shutil.copy2(copia / nombre, banco / nombre)
    return {"n": len(m_copia), "comparacion": comparar(m_copia, manifiesto(banco))}


def _filas_csv(ruta: str | Path) -> tuple[str, list[str]]:
    lineas = [l for l in Path(ruta).read_bytes().decode("utf-8-sig").splitlines() if l.strip()]
    return lineas[0], lineas[1:]


def comparar_csv(a: str | Path, b: str | Path) -> dict:
    cab_a, filas_a = _filas_csv(a)
    cab_b, filas_b = _filas_csv(b)
    ca, cb = collections.Counter(filas_a), collections.Counter(filas_b)
    return {"iguales": cab_a == cab_b and ca == cb, "misma_cabecera": cab_a == cab_b,
            "filas": [len(filas_a), len(filas_b)],
            "solo_en_a": sum((ca - cb).values()), "solo_en_b": sum((cb - ca).values())}


def _resumen(r: dict) -> str:
    return ", ".join(f"{k} {len(v)}" for k, v in r.items())


def main(argv: list[str]) -> int:
    orden = argv[0] if argv else ""
    if orden == "manifiesto" and len(argv) == 3:
        m = manifiesto(argv[1])
        Path(argv[2]).write_text(json.dumps(m, indent=0, sort_keys=True), encoding="utf-8")
        print(f"manifiesto: {len(m)} archivos .sqx, {sum(e['bytes'] for e in m.values())} bytes -> {argv[2]}")
        print(f"sha256 del manifiesto: {_sha256(Path(argv[2]))}")
        return 0
    if orden == "copiar" and len(argv) == 3:
        r = copiar(argv[1], argv[2])
        salida = Path(argv[2]).with_suffix(".json")
        salida.write_text(json.dumps(r["manifiesto"], indent=0, sort_keys=True), encoding="utf-8")
        ok = not any(r["comparacion"].values()) and r["origen_estable"]
        print(f"copiados {r['n']} archivos .sqx, {r['bytes']} bytes; {_resumen(r['comparacion'])}; "
              f"origen estable: {r['origen_estable']} -> {'OK' if ok else 'FALLO'}")
        print(f"manifiesto del origen: {salida} (sha256 {_sha256(salida)})")
        return 0 if ok else 1
    if orden == "retirar" and len(argv) == 3:
        r = retirar(argv[1], argv[2])
        salida = Path(argv[2]).with_suffix(".json")
        salida.write_text(json.dumps(r["manifiesto"], indent=0, sort_keys=True), encoding="utf-8")
        print(f"retiradas {r['n']} ({r['bytes']} bytes) a {argv[2]}, copia idéntica; quedan en el origen {r['quedan']} "
              f"-> {'OK' if r['quedan'] == 0 else 'FALLO'}")
        print(f"manifiesto: {salida} (sha256 {_sha256(salida)})")
        return 0 if r["quedan"] == 0 else 1
    if orden == "reponer" and len(argv) == 3:
        r = reponer(argv[1], argv[2])
        ok = not any(r["comparacion"].values())
        print(f"repuestas {r['n']} en {argv[2]}; {_resumen(r['comparacion'])} -> {'OK' if ok else 'FALLO'}")
        return 0 if ok else 1
    if orden == "conservadas" and len(argv) == 3:
        antes = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        ahora = manifiesto(argv[2])
        r = comparar(antes, ahora)
        ok = conservadas(antes, ahora)
        print(f"antes {len(antes)}, ahora {len(ahora)}; {_resumen(r)} -> {'OK' if ok else 'FALLO'}")
        return 0 if ok else 1
    if orden == "contenido" and len(argv) == 3:
        a, b = manifiesto_contenido(argv[1]), manifiesto_contenido(argv[2])
        r = comparar(a, b)
        ok = conservadas(a, b)
        print(f"contenido: A {len(a)}, B {len(b)}; {_resumen(r)} -> {'OK (todas las de A en B, mismo contenido)' if ok else 'FALLO'}")
        for clave in ("faltan", "distintos"):
            if r[clave]:
                print(f"  {clave} (primeras 5): {r[clave][:5]}")
        return 0 if ok else 1
    if orden == "csv" and len(argv) == 3:
        r = comparar_csv(argv[1], argv[2])
        print(f"filas {r['filas'][0]} y {r['filas'][1]}; misma cabecera: {r['misma_cabecera']}; solo en A "
              f"{r['solo_en_a']}, solo en B {r['solo_en_b']} -> {'IGUALES' if r['iguales'] else 'DISTINTOS'}")
        return 0 if r["iguales"] else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
