# base information
FROM djfarrelly/maildev:0.14.0
MAINTAINER Marco Neumann <marco@crepererum.net>

# upgrade system and install requirements
RUN apk update && \
    apk upgrade && \
    apk add attr && \
    rm -rf /root/.cache /var/cache/*

# PaX fix
COPY docker_entrypoint.sh /docker_entrypoint.sh
ENTRYPOINT ["/docker_entrypoint.sh"]
CMD ["bin/maildev", "--web", "80", "--smtp", "25"]
