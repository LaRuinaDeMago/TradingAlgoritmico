# Revisión externa 07 – Alimentar el sistema con conocimiento, en el orden correcto

Fecha: 2026-10-20 · Origen: otra IA, aportada por Diego en el chat · Tipo: organización del conocimiento (no propone estrategias)

## Resumen de lo que propone (redactado por Claude)

- Dos trabajos en paralelo: cerrar H0 y preparar la 0003; y crear ya una base de conocimiento cuantitativo **sin
  contaminar las pruebas de rentabilidad**. No volcar gigas de vídeos y cientos de artículos esperando que salga una ventaja.
- **Papers fundamentales primero**, convertidos en fichas (problema, método, supuestos y limitaciones, qué respaldan los
  autores frente a qué interpretamos nosotros, qué podemos implementar, qué control cambia): *The Probability of Backtest
  Overfitting*, *The Deflated Sharpe Ratio*, *Pseudo-Mathematics and Financial Charlatanism*.
- **Vídeos del curso:** no se cargan tal cual; (1) extraer el audio con FFmpeg y transcribir con marcas de tiempo;
  (2) capturas de los momentos con parámetros, contrastadas con los `.cfx` y XML; (3) manual técnico por vídeo con
  referencias a minutos. **Piloto con 2–3 vídeos** (Builder, Retester, Optimizer) midiendo calidad, tiempo y coste antes
  de procesar el resto. Verificar el derecho a procesarlos y mantenerlo todo privado.
- **Cuatro bloques:** A fundamentos científicos; B curso; C evidencia empírica propia; D decisiones. Cada afirmación
  rastreable a una fuente, experimento o decisión, distinguiendo hecho verificado, conclusión publicada, interpretación
  nuestra e hipótesis. El curso y los backtests no tienen el mismo valor probatorio que los datos.
- Temas posteriores (sobreajuste, validación temporal, costes, incertidumbre y muestra, régimen y sensibilidad,
  diversificación, reproducibilidad), buscando también evidencia en contra. No implementar todo lo que se lea.
- Orden: H0 sin nuevas dependencias en el proceso crítico; en paralelo, biblioteca privada y piloto de vídeos; después
  automatizar si compensa; antes de H1, incorporar al protocolo las mejoras decididas.

## Respuesta de Claude

| Punto | Postura | Acción |
|---|---|---|
| Base de conocimiento en paralelo, separada del motor crítico | De acuerdo | `conocimiento/README.md` con los 4 bloques; regla 4: nada entra al motor sin validar y decidir |
| Fichas de papers con tipos de afirmación | De acuerdo; encaja con las fichas de la revisión 02 | `conocimiento/fundamentos/PLANTILLA_ficha.md` |
| Tres papers primero | De acuerdo | `LECTURAS.md`. **Descargar requiere permiso de Diego** (A16). No escribo fichas de memoria: serían afirmaciones sin verificar |
| Vídeos: transcribir + capturas + manual | De acuerdo con el método. **Hechos comprobados hoy:** no hay FFmpeg ni Whisper instalados; hay que instalarlos y descargar modelos (1–3 GB) | Pendiente de permiso (A17) y de la procedencia del material (A8) |
| Parte visual de los vídeos | **Matiz:** Claude puede leer imágenes directamente; basta con que FFmpeg extraiga fotogramas | Simplifica el piloto: no hace falta otra herramienta para lo visual |
| Piloto de 2–3 vídeos antes de procesar todo | De acuerdo; proporcional | B11, tras A8 y A17 |
| Los PDF y el curso fuera del repositorio público | De acuerdo | PDF enlazados, no subidos; curso en `LAB_PRIVADO_CURSO` |
| Sin dependencias nuevas en el proceso crítico | De acuerdo. **Hallazgo:** numpy, pandas y scipy tampoco están instalados y H2 los necesita (decisión 0001) | A18 |
