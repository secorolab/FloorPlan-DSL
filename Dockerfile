# syntax=docker/dockerfile:1

# Base: image with bpy and python built and installed
#FROM zocker160/blender-bpy:stable

# ============
FROM ubuntu:20.04
WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND noninteractive

ARG PYTHON_VER_MAJ=3.10
ARG PYTHON_VER=3.10.2

ARG BLENDER_VERSION=3.0

ENV PYTHON_SITE_PACKAGES /usr/local/lib/python$PYTHON_VER_MAJ/site-packages/
ENV WITH_INSTALL_PORTABLE OFF

RUN apt-get update && \
    apt-get -y install \
    build-essential \
    cmake \
    curl \
    git \
    subversion \
    sudo \
    ncdu \
    zlib1g \
    zlib1g-dev \
    libx11-dev \
    libxxf86vm-dev \
    libxcursor-dev \
    libxi-dev \
    libxrandr-dev \
    libxinerama-dev \
    libglew-dev \                                                               
    pkg-config \
    libxkbcommon-x11-dev \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    libffi-dev && \
    rm -rf /var/lib/apt/lists/* 

WORKDIR /home/tmp/python
ADD https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz Python.tgz
RUN tar xzf Python.tgz
WORKDIR /home/tmp/python/Python-$PYTHON_VER
RUN ./configure --enable-optimizations
#RUN ./configure
RUN make -j$(nproc) install

WORKDIR /home/tmp/lib
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64

WORKDIR /home/tmp
RUN git clone https://git.blender.org/blender.git # -b v3.1.2

WORKDIR /home/tmp/blender
RUN git submodule update --init --recursive && make bpy

WORKDIR /home/tmp/blender/build_linux_bpy
#RUN ls -l
RUN cmake .. \
    -DPYTHON_SITE_PACKAGES=/usr/local/lib/python$PYTHON_VER_MAJ/site-packages/ \
    -DWITH_INSTALL_PORTABLE=OFF \
    -DWITH_PYTHON_INSTALL=OFF \
    -DWITH_PLAYER=OFF \
    -DWITH_PYTHON_MODULE=ON \
    -DWITH_MEM_JEMALLOC=OFF && \
    make install -j$(nproc) && rm -rf /home/tmp

# ============
#RUN mkdir /usr/src/app

RUN pip3 install textX[cli] pyyaml matplotlib shapely

#RUN python3 -c "import bpy;import bmesh;import yaml;import PIL;import textx;import matplotlib.pyplot;import shapely"
# Copy language files
RUN mkdir src 

# Copy the code 
COPY src src/
COPY setup.py . 
COPY config.yaml .
COPY README.md .

# Set python path for project src
ENV PYTHONPATH ./src

# Install languages
RUN pip3 install .

# Check for install
RUN textx list-languages
RUN textx list-generators

RUN mkdir models
RUN mkdir output
COPY models/hospital.floorplan models/
COPY models/hospital.variation models/

#RUN ls -R
RUN python3 -c "import bpy; print(dir(bpy.ops.export_mesh))"

ADD test.sh /
RUN chmod +x /test.sh

CMD ["/test.sh"]