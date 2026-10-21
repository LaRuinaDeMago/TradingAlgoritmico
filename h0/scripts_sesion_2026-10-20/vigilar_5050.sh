#!/bin/sh
# Anota cada segundo, durante 60 s, las conexiones y escuchas en el puerto 5050 (y el proceso dueño).
SALIDA="$1"
: > "$SALIDA"
i=0
while [ $i -lt 60 ]; do
  ahora=$(date +%H:%M:%S)
  netstat -ano | grep -E ":5050[[:space:]]" | sed "s/^/$ahora /" >> "$SALIDA"
  i=$((i + 1))
  sleep 1
done
echo "fin" >> "$SALIDA"
