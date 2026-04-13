# Proyecto: Arquitectura de Microservicios y Resiliencia en AWS
**Alumno:** Gerardo Escamilla Cerda
**Materia:** Diseño y Arquitectura de Software
**Fecha:** Abril 2026

---

## ¿Qué problema resuelve mi aplicación?
Mi aplicación gestiona el registro de consultas técnicas en un entorno de nube. Permite que un usuario envíe información a través de una interfaz web, la cual es procesada por un backend especializado para tareas pesadas, asegurando que la persistencia de datos sea confiable.

---

## ¿Cuál era el problema del monolito?
Al correr Apache Benchmark (`ab`), observé que el monolito presentaba un cuello de botella crítico. Como el procesamiento de datos ocurría en el mismo servicio que la interfaz web, el sistema se bloqueaba para todos los usuarios mientras procesaba una sola petición, resultando en tiempos de espera excesivos.

---

## ¿Qué responsabilidad tiene cada microservicio?
**Servicio A:** Gestiona la interfaz de usuario, recibe las solicitudes vía HTTP y realiza el primer guardado en la tabla `respuestas`.
**Servicio B:** Actúa como el motor de procesamiento; recibe notificaciones del Servicio A, ejecuta la lógica pesada y registra el log en la tabla `bitacora_ia`.

---

## ¿Cómo se comunican los servicios?
El Servicio A llama al Servicio B mediante una petición HTTP síncrona. Se utiliza el nombre del contenedor `servicio_b` como hostname, lo cual funciona gracias a la resolución de DNS interna que Docker habilita automáticamente entre servicios de la misma red.

---

## Tablas en la base de datos
| Tabla | Servicio dueño | Qué guarda |
|-------|---------------|------------|
| `respuestas` | Servicio A | Datos iniciales del formulario del usuario. |
| `bitacora_ia` | Servicio B | Confirmaciones de procesamiento y timestamps. |

---

## ¿Qué pasa si el Servicio B se cae?
Durante la prueba de resiliencia, al detener el Servicio B, el Servicio A detectó la interrupción pero siguió operando. El sistema entró en un modo de mantenimiento visual para el usuario, pero permitió que los datos se siguieran guardando en la base de datos principal sin caerse.

---

## Cómo levantar el proyecto
```bash
# 1. Clonar el repositorio
git clone [https://github.com/GeraEsc/Avance_del_Proyecto_Individual.git](https://github.com/GeraEsc/Avance_del_Proyecto_Individual.git)

# 2. Entrar a la carpeta
cd gerardo-escamilla-microservicios/microservicios

# 3. Configurar las variables de entorno en docker-compose.yml
# (Cambiar MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB por los de tu RDS)

# 4. Levantar
sudo docker-compose up --build -d

# 5. Abrir en el navegador
# http://<TU_IP_PUBLICA_EC2>:5000```


## Reflexión Final
Lo más difícil de este proyecto fue lograr que la comunicación entre contenedores fuera fluida, especialmente al configurar el DNS interno de Docker para que el Servicio A reconociera al Servicio B sin usar IPs estáticas. Entendí que la arquitectura de microservicios no solo se trata de "separar el código", sino de gestionar la red y la tolerancia a fallos (resiliencia) de forma independiente. Antes pensaba que un error en un componente debía tirar todo el sistema, pero ahora comprendo que con un buen manejo de excepciones y una arquitectura desacoplada, la experiencia del usuario puede mantenerse a salvo. En una situación real, usaría microservicios para aplicaciones de alta demanda como un e-commerce o una plataforma de servicios financieros (como OXXO GAS), donde el procesamiento de facturas o pagos no debe impedir que otros usuarios sigan navegando en la interfaz principal.
