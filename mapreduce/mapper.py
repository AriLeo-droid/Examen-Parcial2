#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:

    try:
        # Ignorar líneas vacías
        if len(row) != 8:
            continue

        # Ignorar encabezado
        if row[0].lower() == "id":
            continue

        fecha_hora = row[1]
        categoria = row[3]
        cantidad = int(row[5])
        precio = float(row[6])

        ingreso = cantidad * precio

        hora = fecha_hora.split(" ")[1][:2]

        print(f"{hora},{categoria}\t{ingreso}")

    except Exception:
        continue