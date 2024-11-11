FROM quay.pre.eci.geci/ocp-base-images/eci-python-39-rhel8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN yum -y update \
  # psycopg2 dependencies
  && yum -y install postgresql-devel tree \
  # Translations dependencies
  && yum -y install gettext \
  && yum -y install telnet \
  && yum -y install xmlsec1 \
  && yum -y install iputils \
  # cleaning up unused files
  && yum clean all \
  && rm -rf /var/cache/yum

ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Madrid

RUN addgroup django \
  && useradd -g django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt



COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/dev/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/dev/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/dev/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

WORKDIR /data

COPY . .

ENTRYPOINT ["/entrypoint"]
