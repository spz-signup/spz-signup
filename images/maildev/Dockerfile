# base information
FROM djfarrelly/maildev
MAINTAINER Marco Neumann <marco@crepererum.net>

# upgrade system and install requirements
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends attr && \
    rm -rf /root/.cache /var/cache/*

# PaX fix
COPY docker_entrypoint.sh /docker_entrypoint.sh
ENTRYPOINT ["/docker_entrypoint.sh"]
CMD ["bin/maildev", "--web", "80", "--smtp", "25"]
