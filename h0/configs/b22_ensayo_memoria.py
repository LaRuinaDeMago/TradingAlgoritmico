"""Ensayo: ¿sobrevive un proceso que reserva memoria por pasos? Anota cada paso en un archivo (con flush)."""
import ctypes
import sys
import time

salida = sys.argv[1]
bloques = []


def anotar(texto):
    with open(salida, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {texto}\n")


# ¿está en un trabajo (job object) de Windows?
en_job = ctypes.c_int(0)
ctypes.windll.kernel32.IsProcessInJob(ctypes.windll.kernel32.GetCurrentProcess(), None, ctypes.byref(en_job))
anotar(f"inicio; en_job={bool(en_job.value)}")
for i in range(1, 9):
    bloques.append(bytearray(256 * 1024 * 1024))  # 256 MiB, tocados (bytearray los pone a cero)
    anotar(f"reservados {i * 256} MiB")
    time.sleep(2)
time.sleep(20)
anotar("FIN sin morir")
