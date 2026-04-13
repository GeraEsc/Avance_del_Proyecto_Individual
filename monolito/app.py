from flask import Flask, request, render_template_string
import mysql.connector
import random
import time

app = Flask(__name__)

# --- CONFIGURACIÓN Y ACCESO A DATOS ---
db_config = {
    "host": "db-actividades.crocdsukejuv.us-east-1.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": "Password1234",
    "database": "actividades"
}

def guardar_en_db(pregunta, respuesta):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO respuestas (pregunta, respuesta) VALUES (%s, %s)"
        cursor.execute(sql, (pregunta, respuesta))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return False

# --- LÓGICA DE NEGOCIO (Simulación IA) ---
def procesar_con_ia(pregunta):
    respuestas = ["Análisis completado", "Resultado optimizado", "Procesado por IA"]
    time.sleep(0.1)  # Simula tiempo de procesamiento
    return random.choice(respuestas)

# --- INTERFAZ (UI) Y RUTAS ---
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje = ""
    if request.method == 'POST':
        pregunta = request.form.get('pregunta')
        if pregunta:
            respuesta = procesar_con_ia(pregunta)
            if guardar_en_db(pregunta, respuesta):
                mensaje = f"✅ Guardado: {respuesta}"
            else:
                mensaje = "❌ Error al conectar con RDS"

    # HTML dentro del mismo archivo para mantener el concepto de Monolito
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monolito IA - Actividad A</title>
            <style>
                body { font-family: sans-serif; text-align: center; background: #f4f4f4; }
                .container { background: white; padding: 20px; border-radius: 10px; display: inline-block; margin-top: 50px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                input { padding: 10px; width: 250px; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>IA Monolítica - RDS</h1>
                <form method="post">
                    <input type="text" name="pregunta" placeholder="Escribe tu pregunta..." required>
                    <button type="submit">Enviar a IA</button>
                </form>
                <p>{{ mensaje }}</p>
                <hr>
                <small>Servidor: Amazon Linux 2023 | DB: MySQL RDS</small>
            </div>
        </body>
        </html>
    ''', mensaje=mensaje)

# --- RUTA PARA STRESS TEST ---
# Esto permite que un programa externo (como JMeter o un script) ataque esta URL
@app.route('/stress', methods=['GET'])
def stress():
    pregunta = f"Auto-Pregunta {random.randint(1,1000)}"
    respuesta = procesar_con_ia(pregunta)
    guardar_en_db(pregunta, respuesta)
    return {"status": "ok", "pregunta": pregunta}, 200

if __name__ == "__main__":
    # Escucha en todas las IPs en el puerto 8080
    app.run(host='0.0.0.0', port=8080)
