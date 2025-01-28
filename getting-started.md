# Despliegue de KRM

Necesitaremos tener instalado tanto Docker como Docker Compose, que es un orquestador de contenedores de Docker

El fichero que tendremos que cargar será el fichero dev.yml, ese fichero está compuesto por

- Contenedor principal django
- Contenedor de base de datos postgres
- Contenedores réplicas del primer contenedor Django para tareas asíncronas: celerybeat, celeryworker y flower
- Contenedor de redis para encolar los envíos de correo

## Creación de imágenes base

Tanto el contenedor de Django como las réplicas, necesitan de una imagen base que será la primera que tendremos que crear. Para ello navegaremos al directorio **compose/krm_django_base** y ejecutaremos la creación de la imagen base con el comando:

`docker build --no-cache -f dockerfiles/Dockerfile.dev -t 'bienvenidosaez/krm_django_base_dev:latest' .`

Esto nos creará la imagen 'bienvenidosaez/krm_django_base_dev:latest' que si os fijáis es la imagen de base del DockerFile de Django: `FROM bienvenidosaez/krm_django_base_dev:latest`

## Creación de las imágenes del stack

Una vez ya tenemos la imagen base, volvemos al directorio principal y ya podemos construir las imágenes del stack. Desde el directorio raiz:

`docker-compose -f dev.yml build`

## Creación de las tablas del sistema

Una vez con las imágenes realizadas, ya podremos lanzar el comando migrate para crear las tablas de la base de datos con:

`docker-compose -f dev.yml run --rm django python manage.py migrate`

## Creación de usuario administrador

Una vez creadas las tablas, creemos nuestro primer usuario administrador

`docker-compose -f dev.yml run --rm django python manage.py createsuperuser`

Ahí nos pedirá usuario, email contraseña etc...

## Creación de la instancia Configuration

`docker-compose -f dev.yml run --rm django python manage.py shell_plus`

Configuration.objects.create(app_name="KRM Tool")

exit()

`docker-compose -f dev.yml run --rm django python manage.py createsuperuser`


## Arrancar el stack

Ya tendremos todo listo para arrancar el stack. Lo arrancamos con:

`docker-compose -f dev.yml run --rm --service-ports django`
`docker-compose -f dev.yml up -d` # Esto es para arrancarlo en segundo plano

## Parar el stack

`docker-compose -f dev.yml down`

El contenedor de Django tiene el puerto 8000 puenteado por lo que ya podremos entrar desde nuestro navegador en http://localhost:8000



## Para el lanzador de evaluaciones hecho en ReactJS

0. Configurar la url base en el fichero krm-react/src/services/config.js y cambiar la variable de entorno KRM_DJANGO_DEVJS a False para que coja el fichero del bundle en las plantillas. Esa variable está en el fichero de variables de entorno que se llama .django
1. Entrar en la carpeta krm-react
2. Ejecutar `nvm use` para configurar la versión de nodeJS
3. Ejecutar `npm i` para instalar las dependencias
4. Ejecutar `npm run build` => te genera el build del bundle y solo necesitas dos ficheros
krm-react/build/static/js/main.xxxx.js
krm-react/build/static/js/main.xxxx.js.map
5. Esos dos ficheros hay que renombrarlos a main.react.js y main.react.js.map y moverlos a krm/static sobreescribiendo los existentes


## Para el lanzador de evaluaciones hecho en ReactJS en local y poder hacer cambios
0. Configurar la url base en el fichero krm-react/src/services/config.js y cambiar la variable de entorno KRM_DJANGO_DEVJS a True para que coja el fichero del bundle en las plantillas. Esa variable está en el fichero de variables de entorno que se llama .django
1. Entrar en la carpeta krm-react
2. Ejecutar `nvm use` para configurar la versión de nodeJS
3. Ejecutar `npm i` para instalar las dependencias
4. Ejecutar `npm run start` => lanza vite para hacer el bundle en tiempo real y dejarlo arrancado
5. Las plantillas de Django deben usar ya este archivo servido desde localhost:3000 ya que la variable KRM_DJANGO_DEVJS está a True
