FROM nginx

RUN mkdir /certs
COPY ./compose/sacyr/nginx/certs/* /certs/
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/sacyr/nginx/nginx.conf /etc/nginx/conf.d/default.conf
