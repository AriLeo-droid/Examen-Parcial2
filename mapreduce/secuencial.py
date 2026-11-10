#!/usr/bin/env python3
import sys
import csv
import os
from collections import defaultdict

def procesar_secuencial(ruta_csv):
    totales = defaultdict(float)

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        reader = csv.reader(archivo)
        
        for row in reader:
            try:
                if len(row) != 8 or row[0].lower() == "id":
                    continue
                
                fecha_hora = row[1]
                categoria = row[3]
                cantidad = int(row[5])
                precio = float(row[6])
                
                ingreso = cantidad * precio
                hora = fecha_hora.split(" ")[1][:2]
                
                clave = f"{hora},{categoria}"
                totales[clave] += ingreso

            except Exception:
                continue

    for clave in sorted(totales.keys()):
        print(f"{clave}\t{totales[clave]:.2f}")

if __name__ == "__main__":
    # 1. Si pasas la ruta por parámetro al ejecutar
    if len(sys.argv) >= 2:
        archivo_entrada = sys.argv[1]
    # 2. Si se ejecuta dentro de Docker (usa la ruta del volumen montado)
    elif os.path.exists("/data/input/ventas_125052638.csv"):
        archivo_entrada = "/data/input/ventas_125052638.csv"
    # 3. Si se ejecuta localmente fuera de docker buscando en la carpeta superior
    else:
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        archivo_entrada = os.path.join(directorio_actual, "..", "ventas_125052638.csv")

    procesar_secuencial(archivo_entrada)