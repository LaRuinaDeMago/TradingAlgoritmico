# Revisión externa 01 – Sobre la auditoría del curso y la decisión 0003

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego en el chat · Tipo: revisión de método (no propone estrategias)

## Resumen de lo que propone (redactado por Claude)

1. No dar por aprobada la decisión 0003: leer configuraciones del curso no justifica cambiar el mercado, comprar ni
   rediseñar el laboratorio.
2. Separar lo que las configuraciones demuestran de lo que no: no prueban que el curso siga siempre ese proceso ni que
   sus estrategias funcionaran fuera de muestra.
3. Matices: (a) el problema del fuera de muestra usado para seleccionar está bien visto, pero la solución no es quitar
   el OOS del curso sino conservar un periodo final intocable que evalúe el procedimiento completo, selección incluida;
   (b) decir "no se identifica una corrección explícita en las configuraciones", no "el curso no corrige"; (c) el
   deslizamiento 0 es una hipótesis optimista a medir con escenarios adversos, no una prueba de inviabilidad; (d) generar
   con velas H1 no es incorrecto en sí: el riesgo es que el simulador no reproduzca lo que pasa dentro de la vela.
4. "Ignorada por git" no es "privada": sacar la nota del curso de la carpeta del proyecto y aclarar si hay autorización
   para usar el material. Examinar el curso solo en modo lectura.
5. Seguir con la prueba de exportar/importar por fechas como **prueba de integridad de datos**, con criterios de
   aceptación: intervalo exacto, importación sin errores, velas idénticas tras normalizar (fecha/hora, OHLC…), sin
   ausentes/duplicadas/desplazadas, repetible; atención a límites inclusivos, zona horaria y cambios de horario.
6. No decidir todavía EURUSD: separar el H0 técnico de la elección del mercado de investigación, y aclarar la
   discrepancia de cobertura (datos del curso desde 2015 frente a EURUSD de Darwinex desde 2017-10).

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| 1. 0003 pendiente | De acuerdo (ya estaba así) | Sigue PROPUESTA |
| 2. Límite de lo demostrado | De acuerdo | La nota privada ya distinguía "configuraciones" de "vídeos" |
| 3a. OOS: evaluar el procedimiento completo | De acuerdo; es exactamente el papel del bloque sellado | — |
| 3b. "No se identifica corrección explícita" | **Tenía razón: me excedí** | Corregido en la nota privada y en el diario |
| 3c. Deslizamiento 0 = hipótesis | De acuerdo | Se medirá con escenarios de coste adversos (H2) |
| 3d. H1 no es incorrecto en sí | De acuerdo; lo dije como riesgo, no como error | — |
| 4. Nota fuera del repositorio | **Tenía razón** | Movida a `C:\Users\SERVILAB\Documents\LAB_PRIVADO_CURSO\` (fuera del proyecto); la autorización del material la aclara Diego |
| 5. Prueba de integridad export/import | De acuerdo con los criterios | Se adopta su tabla como criterios de aceptación |
| 6. EURUSD sin decidir; aclarar 2015 vs 2017-10 | De acuerdo | Queda abierto en la decisión 0003 y en la ficha H0 |
