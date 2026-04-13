import os
import time
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

@app.route('/procesar')
def procesar():
    pregunta = request.args.get('pregunta')
    
    # Simular carga pesada (Requisito de la Actividad)
    time.sleep(3)
    
    # Guardar en la Tabla B (bitacora_ia)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bitacora_ia (detalle) VALUES (%s)", (f"Procesando: {pregunta}",))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Notificación enviada al Servicio B y procesada en bitácora"})
    except Exception as e:
        return jsonify({"mensaje": f"Error en Servicio B: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
