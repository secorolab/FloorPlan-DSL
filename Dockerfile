# syntax=docker/dockerfile:1

FROM ubuntu:20.04
WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND noninteractive

ARG PYTHON_VER_MAJ=3.7
ARG PYTHON_VER=3.7.17
ARG BLENDER_VERSION=3.0

RUN apt-get update
RUN apt-get install blender python3-pip -y
# RUN apt install python3-pip -y
RUN pip3 install textX[cli] pyyaml matplotlib shapely

# RUN mkdir src 

COPY . .

# Set python path for project src
ENV PYTHONPATH ./src

# Install languages
RUN pip3 install .

# Check for install
RUN textx list-languages
RUN textx list-generators

ADD test.sh /
RUN chmod +x /test.sh

CMD ["/test.sh"]