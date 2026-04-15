# Proyecto: Arquitectura de Microservicios y Resiliencia en AWS
**Alumno:** Gerardo Escamilla Cerda
**Materia:** Diseño y Arquitectura de Software
**Fecha:** Abril 2026

---

## Que problema resuelve mi aplicacion?
Mi aplicación gestiona el registro de consultas técnicas en un entorno de nube. Permite que un usuario envíe información a través de una interfaz web, la cual es procesada por un backend especializado para tareas pesadas, asegurando que la persistencia de datos sea confiable.

---

## Cual era el problema del monolito?
Al correr Apache Benchmark (`ab`), observé que el monolito presentaba un cuello de botella crítico. Como el procesamiento de datos ocurría en el mismo servicio que la interfaz web, el sistema se bloqueaba para todos los usuarios mientras procesaba una sola petición, resultando en tiempos de espera excesivos.

---

## Que responsabilidad tiene cada microservicio?
**Servicio A:** Gestiona la interfaz de usuario, recibe las solicitudes vía HTTP y realiza el primer guardado en la tabla `respuestas`.
**Servicio B:** Actúa como el motor de procesamiento; recibe notificaciones del Servicio A, ejecuta la lógica pesada y registra el log en la tabla `bitacora_ia`.

---

## Como se comunican los servicios?
El Servicio A llama al Servicio B mediante una petición HTTP síncrona. Se utiliza el nombre del contenedor `servicio_b` como hostname, lo cual funciona gracias a la resolución de DNS interna que Docker habilita automáticamente entre servicios de la misma red.

---

## Tablas en la base de datos
| Tabla | Servicio dueño | Que guarda |
|-------|---------------|------------|
| `respuestas` | Servicio A | Datos iniciales del formulario del usuario. |
| `bitacora_ia` | Servicio B | Confirmaciones de procesamiento y timestamps. |

---

## Que pasa si el Servicio B se cae?
Durante la prueba de resiliencia, al detener el Servicio B, el Servicio A detectó la interrupción pero siguió operando. El sistema entró en un modo de mantenimiento visual para el usuario, pero permitió que los datos se siguieran guardando en la base de datos principal sin caerse.

---

## Como levantar el proyecto
```bash
# 1. Clonar el repositorio
git clone https://github.com/GeraEsc/Avance_del_Proyecto_Individual.git

# 2. Entrar a la carpeta del proyecto
cd Avance_del_Proyecto_Individual/microservicios

# 3. Instalación de Dependencias (Si no están instaladas)
sudo yum update -y
sudo yum install -y docker docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
# Aplicar cambios de grupo sin cerrar sesión
newgrp docker

# 4. Configurar variables de entorno
# Edita el archivo y pon tus credenciales de RDS
nano docker-compose.yml 

# 5. Levantar los servicios
# Probamos con 'docker compose' (versión moderna)
sudo docker compose up --build -d

# 6. Comandos de Verificación (¡Agrega estos!)
# Ver si los contenedores están arriba
sudo docker compose ps

# Ver logs en tiempo real (Útil si la página no carga)
sudo docker compose logs -f

# 7. Detener el proyecto
sudo docker compose down
```
---
## Reflexión Final
Lo más difícil de este proyecto fue lograr que la comunicación entre contenedores fuera fluida, especialmente al configurar el DNS interno de Docker para que el Servicio A reconociera al Servicio B sin usar IPs estáticas. Entendí que la arquitectura de microservicios no solo se trata de "separar el código", sino de gestionar la red y la tolerancia a fallos (resiliencia) de forma independiente. Antes pensaba que un error en un componente debía tirar todo el sistema, pero ahora comprendo que con un buen manejo de excepciones y una arquitectura desacoplada, la experiencia del usuario puede mantenerse a salvo. En una situación real, usaría microservicios para aplicaciones de alta demanda como un e-commerce o una plataforma de servicios financieros (como OXXO GAS), donde el procesamiento de facturas o pagos no debe impedir que otros usuarios sigan navegando en la interfaz principal.

