### Build dtnd & dtncat
FROM golang:1.16.2 AS dtn7-builder

RUN git clone https://github.com/dtn7/dtn7-go.git /dtn7-go
RUN cd /dtn7-go \
    && go build ./cmd/dtn-tool \
    && go build ./cmd/dtnd

FROM ubuntu:20.04

ARG CORE_TAG=release-7.5.1

LABEL maintainer="sterz@informatik.uni-marburg.de"
LABEL name="dtn7/dtn7-go_core-tests"
LABEL url="https://github.com/dtn7/dtn7-go_core-tests"
LABEL version="${CORE_TAG}-1"

ENV DEBIAN_FRONTEND noninteractive

# update system, install wget and python
RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -y wget python3-pip \
    && apt-get clean

RUN wget --quiet https://github.com/coreemu/core/archive/${CORE_TAG}.tar.gz \
    && mkdir core \
    && tar xf ${CORE_TAG}.tar.gz \
    && mv /core-${CORE_TAG} /usr/local/share/core

# Install CORE similar to core's tasks.py file
RUN apt-get update \
    && apt-get install -y \
    automake \
    pkg-config \
    gcc \
    libev-dev \
    ebtables \
    iproute2 \
    ethtool \
    tk \
    python3-tk \
    bash \
    && apt-get clean

RUN python3 -m pip install --user \
    grpcio==1.27.2 \
    grpcio-tools==1.27.2 \
    requests

RUN cd /usr/local/share/core \
    && ./bootstrap.sh \
    && ./configure --prefix="/usr/local" \
    && make -j$(nproc) \
    && make install

RUN cd /usr/local/share/core/daemon \
    && python3 -m pip install . \
    && cp scripts/* "/usr/local/bin" \
    && mkdir -p /etc/core \
    && cp data/* /etc/core

RUN echo "custom_services_dir = /root/.core/myservices" >> /etc/core/core.conf

# install core-dtn7 integration
COPY --from=dtn7-builder /dtn7-go/dtn-tool /usr/local/sbin/dtn-tool
COPY --from=dtn7-builder /dtn7-go/dtnd /usr/local/sbin/dtnd

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
