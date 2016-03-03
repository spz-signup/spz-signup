# base information
FROM nginx:1.9
MAINTAINER Marco Neumann <marco@crepererum.net>

# upgrade system
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /root/.cache /var/cache/*

# copy config + keys
COPY dhparam.pem main.crt+chain.pem main.key.pem nginx.conf /etc/nginx/
