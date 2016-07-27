# base information
FROM postgres:9.4
MAINTAINER Marco Neumann <marco@crepererum.net>

# upgrade system
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y --no-install-recommends && \
    rm -rf /root/.cache /var/cache/*

# copy config
COPY postgresql.conf /var/lib/postgresql/postgresql.conf
