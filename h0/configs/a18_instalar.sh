#!/bin/sh
# A18 (aprobado por Diego el 2026-10-23): numpy y scipy con versiones fijadas, solo binarios oficiales de PyPI, en el
# Python del laboratorio. Uso: sh h0/configs/a18_instalar.sh MENSAJE_COMMIT
. h0/configs/b1_funciones.sh "$1"
confirmar
PYTHONPATH=src python -m lab ejecutar --version-sqx N/A --nombre a18_instalar_numpy_scipy --timeout 900 \
  --descripcion "A18 (aprobado por Diego el 2026-10-23): instalar numpy 2.5.4 y scipy 1.18.1, solo binarios de PyPI, en el Python 3.14.6 del laboratorio" \
  -- python -m pip install --only-binary :all: numpy==2.5.4 scipy==1.18.1 | resumen
confirmar
PYTHONPATH=src python -m lab ejecutar --version-sqx N/A --nombre a18_comprobar \
  --descripcion "A18: comprobar versiones instaladas y una operacion de cada libreria" \
  -- python -I -c "import numpy, scipy, scipy.stats; print('numpy', numpy.__version__, 'scipy', scipy.__version__); print('media', numpy.mean([1, 2, 3]), 'p binomial', round(scipy.stats.binomtest(3, 10, 0.5).pvalue, 4))" | resumen
confirmar
