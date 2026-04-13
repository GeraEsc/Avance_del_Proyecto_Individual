import os
import requests
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

@app.route('/')
def index():
    return '''
        <h1>Servicio A: Registro de Consultas</h1>
        <form action="/registrar" method="post">
            <input type="text" name="pregunta" placeholder="Escribe tu pregunta" required>
            <button type="submit">Enviar al Sistema</button>
        </form>
    '''

@app.route('/registrar', methods=['POST'])
def registrar():
    pregunta = request.form.get('pregunta')
    
    # 1. Guardar en la Tabla A (respuestas)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO respuestas (pregunta, respuesta) VALUES (%s, %s)", (pregunta, "Registrado en A"))
        conn.commit()
        cursor.close()
        conn.close()
        msg_a = "Guardado en Tabla A"
    except Exception as e:
        msg_a = f"Error en Tabla A: {str(e)}"

    # 2. Intentar llamar al Servicio B (Comunicación entre contenedores)
    try:
        url_b = os.getenv('URL_SERVICIO_B')
        response = requests.get(url_b, params={'pregunta': pregunta}, timeout=5)
        res_b = response.json().get('mensaje')
    except:
        res_b = "Servicio B no disponible (Modo Resiliencia Activo)"

    return jsonify({
        "status": "Procesado",
        "servicio_a": msg_a,
        "servicio_b": res_b
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
