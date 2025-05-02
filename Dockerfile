# syntax=docker/dockerfile:1
FROM ubuntu:24.04
WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update
RUN apt-get install python3-pip python3-venv -y
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

# Set python path for project src
ENV PYTHONPATH=/usr/src/app/src

# Install languages
RUN pip3 install .

CMD textx generate --target json-ld -o /usr/src/app/output /usr/src/app/models/*.fpm