# base information
FROM python:2.7-alpine
MAINTAINER Marco Neumann <marco@crepererum.net>

# create user
RUN adduser -h /home/spz -s /bin/bash -u 1000 -D spz

# set workdir
WORKDIR /home/spz/code

# upgrade system
RUN apk update && \
    apk upgrade && \
    apk add bash file gcc musl-dev postgresql-client postgresql-dev && \
    ln -s /usr/lib/libmagic.so.1 /usr/lib/libmagic.so && \
    pip install -U pip

# install requirements
COPY requirements.txt /home/spz/code/requirements.txt
RUN pip install -U -r requirements.txt

# copy code
COPY . /home/spz/code
RUN chown -R spz:spz /home/spz/code

# security and volumes
VOLUME /home/spz
USER 1000

# set entry point
ENTRYPOINT ["/home/spz/code/util/docker_entrypoint.sh"]

# default to bash
CMD ["bash"]

