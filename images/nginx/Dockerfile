# base information
FROM nginx
MAINTAINER Marco Neumann <marco@crepererum.net>

# copy config + keys
COPY dhparam.pem main.crt+chain.pem main.key.pem nginx.conf /etc/nginx/
