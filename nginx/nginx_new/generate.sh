#!/bin/bash

IP="123.123.123.123"

mkdir -p /etc/nginx/certs

if [ ! -f /etc/nginx/certs/self.crt ]; then
    echo "Creating self-signed SSL certificate for IP $IP ..."
    openssl req -x509 -nodes -days 365 \
      -newkey rsa:2048 \
      -keyout /etc/nginx/certs/self.key \
      -out /etc/nginx/certs/self.crt \
      -subj "/CN=$IP"
fi
