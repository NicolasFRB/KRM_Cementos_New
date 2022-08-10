FROM bienvenidosaez/krm_django_base_prod:latest

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

#RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords');"

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
