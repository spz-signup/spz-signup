# base information
FROM python:2.7
MAINTAINER Marco Neumann <marco@crepererum.net>

# create user
RUN useradd --home-dir /home/spz --create-home --shell /bin/bash --uid 1000 spz

# set workdir
WORKDIR /home/spz/code

# upgrade system
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgresql-client && \
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

