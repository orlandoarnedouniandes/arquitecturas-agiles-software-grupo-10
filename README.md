# Para correr el proyecto

- Abrir una terminal apuntando a la raiz del proyecto al mismo nivel donde se encuentra el archivo docker-compose.yml
- Correr el comando docker-compose up --build
- Esperar unos segundos a que la orquestacion de los servicios se complete. Usualmente puede ser unos 30 segundos

# Para ver la informacion contenida en la base de datos dentro de los contenedores.

- La base de datos del monitor por ejempo se encuentra en esta ruta: arquitecturas-agiles-software-grupo-10-monitor-1:/app/src/dbmonitor.db
- Sabiendo esto, puedes tomar esa ruta y guardar la base de datos en una ruta mas familiar en tu computador corriendo este comando: docker cp arquitecturas-agiles-software-grupo-10-monitor-1:/app/src/dbmonitor.db C:/Users/TuUsuario.../etc.../dbmonitor_docker.db
  -Luego ya puedes ver el contenido en esta base de datos con SQLite u otra herramienta
