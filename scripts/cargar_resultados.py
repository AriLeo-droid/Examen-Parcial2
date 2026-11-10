#!/usr/bin/env python3
import os
import sys
import psycopg2

def obtener_conexion_db():
    """Conecta a PostgreSQL usando variables de entorno o valores por defecto del docker-compose."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),         # Nombre del servicio en docker-compose
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        port=int(os.getenv("DB_PORT", 5432))
    )

def crear_tabla(conn):
    """Crea la tabla 'resultados' para almacenar la clave (hora,categoria) y el total."""
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                clave VARCHAR(100) PRIMARY KEY,
                total NUMERIC(12, 2) NOT NULL,
                fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.commit()

def cargar_resultados(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo '{ruta_archivo}' no existe.")
        sys.exit(1)

    try:
        conn = obtener_conexion_db()
        crear_tabla(conn)
        
        registros_insertados = 0

        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            with conn.cursor() as cursor:
                for linea in archivo:
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    try:
                        clave, valor_str = linea.split('\t')
                        total = float(valor_str)

                        # Insertar o actualizar si ya existe la clave (UPSERT)
                        cursor.execute("""
                            INSERT INTO resultados (clave, total)
                            VALUES (%s, %s)
                            ON CONFLICT (clave) 
                            DO UPDATE SET total = EXCLUDED.total, fecha_carga = CURRENT_TIMESTAMP;
                        """, (clave, total))

                        registros_insertados += 1
                    except ValueError:
                        # Ignorar líneas que no cumplan el formato clave\tvalor
                        continue

        conn.commit()
        conn.close()
        print(f"Exito: Se cargaron/actualizaron {registros_insertados} registros en la base de datos.")

    except Exception as e:
        print(f"Error de base de datos o archivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ruta por defecto a la salida estándar de Hadoop MapReduce
    ruta_part = sys.argv[1] if len(sys.argv) >= 2 else "/data/output/resultado/part-00000"
    cargar_resultados(ruta_part)