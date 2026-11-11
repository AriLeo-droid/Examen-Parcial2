#!/usr/bin/env python3
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)

def obtener_conexion():
    """Conecta a la base de datos de PostgreSQL en el servicio 'db'."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        port=int(os.getenv("DB_PORT", 5432)),
        cursor_factory=RealDictCursor
    )

# ---------------------------------------------------------
# 1. GET /resultados -> Todos los registros
# ---------------------------------------------------------
@app.route('/resultados', methods=['GET'])
def obtener_todos():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute("SELECT clave, total, fecha_carga FROM resultados ORDER BY clave ASC;")
            filas = cur.fetchall()
        conn.close()
        return jsonify(filas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 2. GET /resultados/<clave> -> Filtro por clave (ej: /resultados/14,Electrónica)
# ---------------------------------------------------------
@app.route('/resultados/<path:clave>', methods=['GET'])
def obtener_por_clave(clave):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute("SELECT clave, total, fecha_carga FROM resultados WHERE clave = %s;", (clave,))
            registro = cur.fetchone()
        conn.close()

        if registro:
            return jsonify(registro), 200
        return jsonify({"error": f"No se encontró la clave: '{clave}'"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 3. POST /resultados -> Crear o actualizar registro (Escritura CRUD)
#    Cuerpo JSON esperado: {"clave": "18,Ropa", "total": 1500.50}
# ---------------------------------------------------------
@app.route('/resultados', methods=['POST'])
def crear_registro():
    datos = request.get_json()
    if not datos or 'clave' not in datos or 'total' not in datos:
        return jsonify({"error": "Campos 'clave' y 'total' son requeridos."}), 400

    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO resultados (clave, total)
                VALUES (%s, %s)
                ON CONFLICT (clave) 
                DO UPDATE SET total = EXCLUDED.total, fecha_carga = CURRENT_TIMESTAMP
                RETURNING clave, total, fecha_carga;
            """, (datos['clave'], datos['total']))
            nuevo = cur.fetchone()
        conn.commit()
        conn.close()
        return jsonify(nuevo), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 4. PUT /resultados/<clave> -> Actualizar un valor existente
#    Cuerpo JSON esperado: {"total": 2000.00}
# ---------------------------------------------------------
@app.route('/resultados/<path:clave>', methods=['PUT'])
def actualizar_registro(clave):
    datos = request.get_json()
    if not datos or 'total' not in datos:
        return jsonify({"error": "El campo 'total' es requerido."}), 400

    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE resultados 
                SET total = %s, fecha_carga = CURRENT_TIMESTAMP 
                WHERE clave = %s
                RETURNING clave, total, fecha_carga;
            """, (datos['total'], clave))
            actualizado = cur.fetchone()
        conn.commit()
        conn.close()

        if actualizado:
            return jsonify(actualizado), 200
        return jsonify({"error": f"La clave '{clave}' no existe."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# 5. DELETE /resultados/<clave> -> Eliminar registro
# ---------------------------------------------------------
@app.route('/resultados/<path:clave>', methods=['DELETE'])
def eliminar_registro(clave):
    try:
        conn = obtener_conexion()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM resultados WHERE clave = %s RETURNING clave;", (clave,))
            eliminado = cur.fetchone()
        conn.commit()
        conn.close()

        if eliminado:
            return jsonify({"mensaje": f"Registro '{clave}' eliminado exitosamente."}), 200
        return jsonify({"error": f"La clave '{clave}' no existe."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def inicializar_db():
    conn = obtener_conexion()

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            clave VARCHAR(100) PRIMARY KEY,
            total NUMERIC(15,2) NOT NULL,
            fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

    conn.commit()
    conn.close()


inicializar_db()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)