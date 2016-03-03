# base information
FROM redis:3.0
MAINTAINER Marco Neumann <marco@crepererum.net>

# upgrade system
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /root/.cache /var/cache/*
