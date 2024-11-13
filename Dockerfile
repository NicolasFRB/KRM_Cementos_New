FROM quay.pre.eci.geci/ocp-base-images/eci-python-311-rhel8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Asegurarse de que los siguientes comandos se ejecuten como root
USER root

# Actualizar paquetes e instalar dependencias
RUN yum -y update && \
    # Dependencias de psycopg2
    yum -y install postgresql-devel tree && \
    # Dependencias de traducciones
    yum -y install gettext && \
    yum -y install telnet && \
    yum -y install xmlsec1 && \
    yum -y install iputils && \
    # Limpieza de archivos no utilizados
    yum clean all && \
    rm -rf /var/cache/yum

# Configurar zona horaria
ENV TZ=Europe/Madrid

# Crear grupo y usuario 'django' en RHEL 8
RUN groupadd django && \
    useradd -g django django

# Instalar pip si no está disponible
RUN yum -y install python39-pip && \
    pip3 install --upgrade pip

# Establecer alias 'pip' para 'pip3' si es necesario
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# Instalar requerimientos
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

# Copiar y preparar scripts de inicio
COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//' /entrypoint && \
    chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r$//' /start && \
    chmod +x /start

COPY ./compose/dev/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//' /start-celeryworker && \
    chmod +x /start-celeryworker

COPY ./compose/dev/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//' /start-celerybeat && \
    chmod +x /start-celerybeat

COPY ./compose/dev/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//' /start-flower && \
    chmod +x /start-flower

# Establecer el directorio de trabajo
WORKDIR /data

# Copiar el resto del código de la aplicación
COPY . .

# Cambiar al usuario 'django' por seguridad
USER django

ENTRYPOINT ["/entrypoint"]

