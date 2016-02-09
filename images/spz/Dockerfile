# base information
FROM python:2.7-slim
MAINTAINER Marco Neumann <marco@crepererum.net>

# create user
RUN useradd --home-dir /home/spz --create-home --shell /bin/bash --uid 1000 spz

# set workdir
WORKDIR /home/spz/code

# upgrade system and install requirements (normal and build)
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends gcc libmagic1 libpq-dev postgresql-client && \
    pip install -U pip --no-cache-dir && \
    rm -rf /root/.cache /var/cache/*

# install requirements and do cleanup
COPY requirements.txt /home/spz/code/requirements.txt
RUN pip install -U -r requirements.txt --no-cache-dir && \
    rm -rf /root/.cache /var/cache/*

# copy code
COPY . /home/spz/code
RUN mkdir /state && \
    chown -R spz:spz /home/spz/code /state

# security and volumes
VOLUME ["/home/spz/code/spz/static", "/state"]
USER 1000

# set entry point
ENTRYPOINT ["/home/spz/code/util/docker_entrypoint.sh"]

# default to bash
CMD ["bash"]

