FROM quay.pre.eci.geci/ocp-base-images/eci-python-311-rhel8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Asegurarse de que los siguientes comandos se ejecuten como root
USER root

# Actualizar paquetes e instalar dependencias
RUN yum -y update && \
    yum clean all && \
    rm -rf /var/cache/yum

# Crear un directorio temporal para los RPMs
RUN mkdir /tmp/rpms

# Descargar los RPMs necesarios desde un repositorio público
# Nota: Es importante verificar la compatibilidad y seguridad de los paquetes descargados.
# RUN cd /tmp/rpms && \
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/xmlsec1-1.2.25-4.el8.x86_64.rpm && \
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/xmlsec1-openssl-1.2.25-4.el8.x86_64.rpm && \
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/libxml2-devel-2.9.7-9.el8.x86_64.rpm && \
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/libxml2-2.9.7-9.el8.x86_64.rpm && \
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/libxml2-python3-2.9.7-9.el8.x86_64.rpm
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/xmlsec1-devel-1.2.25-4.el8.x86_64.rpm && \
    # curl -O http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/xmlsec1-openssl-devel-1.2.25-4.el8.x86_64.rpm && \
    

# Descargar los RPMs necesarios desde un repositorio público
# Nota: Es importante verificar la compatibilidad y seguridad de los paquetes descargados.

# Probando a no utilizarlos ya que al parecer ya existen
# curl -O https://www.rpmfind.net/linux/centos-stream/9-stream/AppStream/x86_64/os/Packages/libxml2-devel-2.9.13-2.el9.x86_64.rpm && \
# curl -O https://www.rpmfind.net/linux/centos-stream/9-stream/BaseOS/x86_64/os/Packages/libxml2-2.9.13-2.el9.x86_64.rpm && \
RUN cd /tmp/rpms && \
    curl -O https://www.rpmfind.net/linux/almalinux/8.10/AppStream/x86_64/os/Packages/xmlsec1-1.2.25-4.el8.x86_64.rpm && \
    curl -O https://www.rpmfind.net/linux/almalinux/8.10/AppStream/x86_64/os/Packages/xmlsec1-openssl-1.2.25-4.el8.x86_64.rpm && \
    curl -O https://www.rpmfind.net/linux/mageia/distrib/8/x86_64/media/core/release/libxml2-python3-2.9.10-7.mga8.x86_64.rpm && \
    curl -O https://vault.centos.org/centos/8/PowerTools/x86_64/os/Packages/xmlsec1-devel-1.2.25-4.el8.x86_64.rpm && \
    curl -O https://vault.centos.org/centos/8/PowerTools/x86_64/os/Packages/xmlsec1-openssl-devel-1.2.25-4.el8.x86_64.rpm 

# Instalar los RPMs descargados
RUN rpm -Uvh /tmp/rpms/*.rpm --nodeps --force

# Actualizar paquetes e instalar dependencias
RUN yum -y install postgresql-devel postgresql gettext telnet iputils python3-tkinter.x86_64 tree  && \
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

# Copiar el script de inicialización de la base de datos
COPY init_db.sh /usr/local/bin/init_db.sh
RUN chmod +x /usr/local/bin/init_db.sh

# Establecer el directorio de trabajo
WORKDIR /data

# Copiar el resto del código de la aplicación
COPY . .
RUN chmod -R 755 **/locale/en
RUN chmod 755 **/krm-media

# Cambiar al usuario 'django' por seguridad
USER django

# Modificar el ENTRYPOINT para ejecutar el script de inicialización y luego el entrypoint original
ENTRYPOINT ["/bin/sh", "-c", "/init_db.sh && /entrypoint"]
