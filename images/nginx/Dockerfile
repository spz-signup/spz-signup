# base information
FROM nginx:1.11
MAINTAINER Marco Neumann <marco@crepererum.net>

# upgrade system
# GPG key of nginx is expired! oO
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget && \
    wget https://nginx.org/keys/nginx_signing.key -O - | apt-key add - && \
    apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /root/.cache /var/cache/*

# copy config + keys
COPY dhparam.pem main.crt+chain.pem main.key.pem nginx.conf /etc/nginx/
