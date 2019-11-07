### Build dtn7
FROM golang:1.12 AS dtn7-builder

COPY dtn7 /dtn7
WORKDIR /dtn7
RUN go build -o /dtn7cat ./cmd/dtncat \
    && go build -o /dtn7d ./cmd/dtnd

### Compose the actual worker container
FROM maciresearch/core_worker:0.4.2

# Install further measuring tools
RUN apt-get update \
    && apt-get install --no-install-recommends -yq \
    bwm-ng \
    sysstat \
    tcpdump \
    patch \
    python-nacl \
    python-ipcalc \
    libdaemon-dev \
    libnl-3-dev \
    libnl-cli-3-dev \
    libnl-genl-3-dev \
    libnl-nf-3-dev \
    libnl-route-3-dev \
    libarchive-dev \
    psmisc \
    wireshark \
    && apt-get clean

# Install CORE extensions for the network test
COPY dotcore /root/.core/
RUN echo 'custom_services_dir = /root/.core/myservices' >> /etc/core/core.conf

# Install the software
COPY --from=dtn7-builder /dtn7d   /usr/local/sbin/
COPY --from=dtn7-builder /dtn7cat /usr/local/sbin/
