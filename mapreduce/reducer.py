#!/usr/bin/env python3

import sys

clave_actual = None
total = 0

for linea in sys.stdin:

    try:

        clave, valor = linea.strip().split("\t")
        valor = float(valor)

        if clave_actual == clave:

            total += valor

        else:

            if clave_actual is not None:
                print(f"{clave_actual}\t{total:.2f}")

            clave_actual = clave
            total = valor

    except Exception:
        continue

if clave_actual is not None:
    print(f"{clave_actual}\t{total:.2f}")