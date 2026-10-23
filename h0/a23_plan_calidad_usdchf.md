# A23: calidad de USDCHF 2003–2024 antes de usarlo en la calibración (plan con criterios previos)

**Por qué:** Diego aprobó A23 (2026-10-23): ampliar los datos quemados de USDCHF de 22 meses a 2003–2024 solo para la
calibración de la fase 1, **después** de comprobar que los años añadidos son comparables en calidad (condición de la
revisión 18: huecos, spread, cambios de convención horaria, volumen). Con datos peores, el embudo se calibraría con
ruido que no existe en los datos de investigación. **Qué decisión cambia:** el tramo de años que entra en la
calibración. **Límite de tiempo:** 2 h.

## Ensayos en seco (hechos antes de escribir esto)

- n.º 291: pedir enero de 2003 devuelve **una sola vela, fuera del rango** (2003.05.05 03:00). **Trampa de SQX:** si el
  rango pedido no tiene datos, exporta la primera vela disponible. → Toda exportación se comprueba contra su rango.
- n.º 292: mayo de 2003 sale con 27.180 velas, del lunes 2003.05.05 03:00 al viernes 2003.05.30 23:59, dentro del
  rango. Los datos empiezan el **2003-05-05**, no en 2003-01. Los días laborables traen 1.440 minutos (se rellenan los
  minutos sin cotización): las **velas planas** son el indicador de cotización ausente. Hay huecos reales (el
  2003-05-27 solo tiene 180 minutos).

## Datos y herramienta

- `USDCHF_M1_dukas`, exportación M1 `2003.01.01 → 2024.10.30` con la orden de B1 (n.º 96) a `lab_h0\a23\E_total`.
- Referencia: la ventana ya usada en H0, B1 y B17, **2023.01.01 → 2024.10.30** (0002).
- Analizador `h0/configs/a23_calidad.py`, con errores sembrados en `tests/test_a23_calidad.py` (duplicado, OHLC
  incoherente, día sin datos, huecos, velas planas, convención horaria desplazada 1 h, salto de precio; los datos
  limpios pasan todos; el salto del SNB del 2015-01-15 es la única excepción, fijada de antemano).
- Spread: las velas M1 no lo traen → **INCONCLUSO** desde estos datos; la calibración usa costes fijos declarados.

## Criterios por año (frente a la referencia R)

| # | Criterio |
|---|---|
| C0 | La exportación está dentro del rango pedido (primera vela ≥ 2003.05.05, última ≤ 2024.10.30) y el recuento es razonable (> 7 millones de velas) |
| C1 | Integridad: 0 velas desordenadas o duplicadas, 0 OHLC incoherentes, 0 precios no positivos |
| C2 | Cobertura de minutos de lunes a viernes ≥ 0,9 × la de R |
| C3 | Huecos de más de 60 min dentro de la semana, por 52 semanas ≤ máx(10; 3 × los de R) |
| C4 | Velas planas (O=H=L=C) ≤ máx(3 × las de R; las de R + 0,05) |
| C5 | Apertura y cierre semanal más frecuentes iguales a los de R (misma convención horaria) |
| C6 | 0 movimientos de más del 2 % en ≤ 5 min, salvo el 2015-01-15 (SNB) |
| VOL | Informativo: mediana de volumen entre 0,1 y 10 veces la de R; si no, la calibración no usa indicadores de volumen en esos años |

**Veredicto:** el **tramo utilizable** es el de años contiguos más largo que termina en 2024 y pasa C1–C6 (2003 y 2024
son años parciales y se evalúan con sus días). Si es 2003–2024, A23 se aplica tal cual. Si es más corto, la calibración
usa ese tramo y se dice. Si tiene menos de 5 años, la ventana corta de la 0002 queda solo como exploratoria y las
conclusiones de la fase 1 se limitan (revisión 18). Los umbrales no se cambian después de ver los resultados (regla 8);
si un año falla por un motivo que el plan no previó, se diagnostica aparte y se registra como cambio de proceso.
