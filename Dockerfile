FROM python:3.9-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update  \
  && apt-get upgrade -y \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev tree \
  # Translations dependencies
  && apt-get install -y gettext \
  && apt-get install -y telnet \
  && apt-get install -y iputils-ping \
  && apt-get install -y npm 

COPY ./setup_20.x /setup_20.x
RUN chmod +x /setup_20.x

  # cleaning up unused files
# Original
# RUN curl -sL  file:///setup_20.x | bash -  

#Windows
RUN curl -sL /setup_20.x | bash -

RUN apt-get install -y nodejs 

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Madrid

RUN addgroup django \
  && useradd -g django django

# Requirements are installed here to ensure they will be cached.
COPY requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/dev.txt

ENV PYTHONUNBUFFERED 1

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

# COPY ./compose/dev/django/celery/worker/start /start-celeryworker
# RUN sed -i 's/\r//' /start-celeryworker
# RUN chmod +x /start-celeryworker

# COPY ./compose/dev/django/celery/beat/start /start-celerybeat
# RUN sed -i 's/\r//' /start-celerybeat
# RUN chmod +x /start-celerybeat

# COPY ./compose/dev/django/celery/flower/start /start-flower
# RUN sed -i 's/\r//' /start-flower
# RUN chmod +x /start-flower

COPY ./buildReact.sh /buildReact.sh 
RUN sed -i 's/\r//' /buildReact.sh
RUN chmod +x /buildReact.sh

WORKDIR /app

COPY . .

# RUN cd krm-react && npm i

# RUN chmod -R 755 ./krm-react/node_modules/.bin/react-scripts*
#RUN ./buildReact.sh 

RUN chmod -R 755 **/locale/en
RUN chmod -R 755 buildReact.sh

ENTRYPOINT ["/entrypoint"]

CMD ["/start"]
