# Protocolo de sellado de los datos de Darwinex – reparto antes de ver ningún precio

Estado: BORRADOR
Aprobado por:
Fecha de aprobación:
Redactado por: Claude (por delegación de Diego), 2026-10-20
Protocolo anterior (si sustituye a otro): —

> Este protocolo decide **qué parte de los datos no se mira nunca durante la investigación**. Se escribe y se aprueba
> **antes** de descargar ningún precio de Darwinex. Hasta su aprobación no se descarga nada.
> La plantilla `plantilla_acceso_sellado.md` es otra cosa: sirve para **abrir** lo sellado en el examen final.
> **Este protocolo no autoriza a leer `data/sealed/`.** No se usa nunca en la variable `LAB_PROTOCOLO_SELLADO`: el
> guardián concedería acceso a cualquier protocolo aprobado que se le indique.

Propuesta concreta para completar las secciones 3–5 y el presupuesto: `docs/decisiones/0003-reparto-mercado-presupuesto.md`
(**ACEPTADA v6** el 2026-10-21). **Manda la 0003 v6** donde este borrador diga otra cosa: el inicio del sellado ya no es
fijo (2024-10-01), sale de la regla de la 0003 §1 (fecha más tardía vista en el curso); el mercado es EURUSD. Este
protocolo se reescribe y se aprueba **después de B1** (prueba de exportar/importar), con la fecha de corte calculada.

## 1. Lo que ya se sabe (solo metadatos, ningún precio visto)

Registro n.º 87 (`-symbol action=darwinexsymbols`): la licencia permite 328 símbolos de Darwinex.
Forex y metales: 45 (casi todos desde **2017-10-01**). Índices: 13 (desde 2017-10, 2018-06 o 2019-12). Energía: 3.
Cripto: 9. Acciones de EE. UU.: 258 (desde 2019-12). La fecha final no se conoce todavía.
**Como mucho hay ~9 años de forex** para investigar, validar y examinar.

## 2. Condiciones previas (todas, antes de descargar un solo precio)

1. **Guardián sin el agujero de PowerShell**, aplicado en la sesión de mantenimiento y comprobado con una llamada **real**
   de PowerShell sobre un archivo inexistente de la carpeta sellada (no solo simulada). Mientras no existían datos sellados
   era un riesgo teórico; con ellos, deja de serlo.
2. **Primer mercado elegido** con los criterios de la sección 5, aprobados antes de ver ningún backtest de ese mercado.
3. **Presupuesto y criterios de abandono con cifras** (hoja de ruta: "se fijan en H0, antes de ver ningún resultado").
4. **Comprobado en H0 cómo descarga SQX los datos de Darwinex** (sección 6): si admite una fecha de fin, su granularidad,
   zona horaria y modelo de costes.

## 3. Reparto temporal propuesto (lo decide Diego)

El **mismo corte de calendario para todos los instrumentos**: ver EURUSD de 2025 también informa sobre GBPUSD de 2025.

| Bloque | Periodo | Uso |
|---|---|---|
| Investigación | 2017-10-01 → **2024-09-30** (7 años) | Generación, selección y validación interna (fuera de muestra y walk-forward **dentro** de este bloque) |
| **Sellado** (examen final) | **2024-10-01** → fecha de descarga (~24 meses) | No se mira. Se abre una sola vez, con protocolo de acceso aprobado |
| Prospectivo | Después de la fecha de descarga | Validación en demo (H4): datos que no existían al investigar |

Por qué 24 meses: con estrategias H1 da del orden de cientos de operaciones por estrategia (suficiente para un intervalo
de incertidumbre útil) y deja 7 años para investigar. **Alternativas:** 18 meses (más investigación, examen más débil) o
36 meses (examen más fuerte, 6 años para investigar). No se elige mirando datos.

## 4. Cómo se sella (el problema de fondo)

SQX guarda toda la historia descargada en su almacén (`user/data/History`) y la **generación lee de ahí**: un periodo
sellado que siga dentro de SQX **no está sellado**. Opciones, por orden de preferencia (a confirmar en la sección 6):

- **A. Descargar solo hasta 2024-09-30** en la instalación de investigación, si SQX acepta una fecha de fin para Darwinex.
  El bloque sellado se descarga aparte, se exporta a archivo, se **cifra** (7-Zip AES-256, contraseña que solo conoce
  Diego), se registra su SHA-256 y la copia en claro se elimina. Lo hace Diego o un proceso que él supervisa.
- **B. Segunda instalación de SQX** solo para el examen final (SQX lo admite: "múltiples instalaciones en carpetas
  distintas"). La de investigación nunca tiene el bloque sellado.
- **C. Descargar todo y recortar** en la instalación de investigación. **Última opción:** hay un momento en que el
  bloque sellado está dentro de SQX, y recortar datos en SQX no está probado.

En cualquier opción: el bloque sellado no entra nunca en `data/raw/` ni en ningún proyecto de SQX de investigación, y
cada paso se registra en `registry/` (sin abrir el contenido: solo nombres, tamaños y hashes).

## 5. Criterios para elegir el primer mercado (fijados antes de ver backtests)

Se puntúan **sin mirar precios ni resultados**, solo con información de contrato y de disponibilidad:

1. Historia en Darwinex desde 2017-10 (máxima longitud del bloque de investigación).
2. Operable en el vehículo previsto (Darwinex Zero / MT4) con **costes documentados** (spread, comisión, swap).
3. Coste de transacción bajo en relación con el movimiento típico (se estima con las especificaciones del broker, no con
   precios del bloque sellado).
4. Horario y liquidez adecuados para estrategias intradía/H1.
5. **No USDCHF** (decisión 0002: datos quemados en H0).
6. Penalización para los mercados más minados por usuarios de SQX (oro, Nasdaq, DAX, según la hoja de ruta), a
   compensar con el valor de seguir el curso de Imox. **Esto lo pondera Diego.**

Candidatos que cumplen 1 y 5: EURUSD, GBPUSD, USDJPY, AUDUSD, XAUUSD, NDXm (Nasdaq), GDAXIm (DAX) y otros.
Claude no recomienda uno por rendimiento: no lo conoce ni debe conocerlo.

## 6. Qué falta comprobar en H0 antes de descargar (tarea 5, sin precios)

- **Fecha de fin para Darwinex: según la documentación instalada, NO.** `-symbol action=add` solo registra el símbolo y
  la descarga es `-data action=update`; con `datefrom`/`dateto` "solo está implementado para Dukascopy; las demás fuentes
  informan de que el rango no está soportado" (`docs/cli/qdmcli.md`). Sin rango, se descarga **toda** la historia.
  → La opción A de la sección 4 probablemente no es posible; **la B (segunda instalación) pasa a ser la preferida**.
  No se ha comprobado intentándolo: si la documentación se equivocara, el intento metería precios en SQX antes de aprobar
  este protocolo.
- **Costes que trae SQX** (registro n.º 88, sin precios): perfiles de broker "Darwinex" y "Darwinex Zero"; spread por
  defecto EURUSD 0,6 · GBPUSD 0,8 · USDJPY 1,4 · AUDUSD 1,4 · USDCAD 1,6 · XAUUSD 28 · SP500 6 · WS30 4 · XTIUSD 6
  (en la unidad de cada instrumento). Son valores por defecto de SQX, **no** las condiciones oficiales de Darwinex Zero.
  Comisión y swap no salen por línea de comandos: INCONCLUSO (interfaz o condiciones oficiales del broker).
  El valor del punto de los pares que no cotizan en USD es fijo (p. ej. USDCAD 72.157,88): tipo de cambio congelado.
- Granularidad real (la ayuda ofrece `datatype=M1` o `TICK`) y fecha final disponible.
- Zona horaria y la incoherencia horaria ya vista en SQX (consola 2 h adelantada; aviso de cambio de convención en datos).
- Modelo de costes que trae SQX para los instrumentos de Darwinex (spread, comisión, swap) frente a las condiciones
  vigentes de Darwinex Zero.

## 7. Registro

Cada paso (descarga, exportación, cifrado, eliminación de la copia en claro, hashes) es una entrada en `registry/`.
El commit de este protocolo **aprobado** fecha la decisión: cualquier cambio posterior exige un protocolo nuevo que
cite a este y explique por qué.
