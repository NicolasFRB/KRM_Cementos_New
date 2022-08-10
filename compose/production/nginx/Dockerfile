FROM nginx

RUN mkdir /certs
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./krm/templates/error_pages/* /usr/share/nginx/html/
RUN chmod -R 755 /usr/share/nginx/html
RUN chown -R nginx:nginx /usr/share/nginx/html