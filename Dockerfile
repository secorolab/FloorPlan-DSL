# syntax=docker/dockerfile:1

FROM ubuntu:24.04
WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND noninteractive
ENV VIRTUAL_ENV=/opt/venv

ARG PYTHON_VER_MAJ=3.7
ARG PYTHON_VER=3.7.17
ARG BLENDER_VERSION=3.0

RUN apt-get update
RUN apt-get install blender python3-pip python3-venv -y
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .

RUN pip install -r requirements.txt

# Set python path for project src
ENV PYTHONPATH /usr/src/app/src

# Install languages
RUN pip3 install .

WORKDIR /usr/src/app/src

# Check for install
RUN textx list-languages
RUN textx list-generators

ADD test.sh /
RUN chmod +x /test.sh

CMD ["/test.sh"]