### Build dtn7
FROM golang:1.14 AS dtn7-go-builder

COPY dtn7-go /dtn7-go
WORKDIR /dtn7-go
RUN go build -race -o /dtnd ./cmd/dtnd \
    && go build -race -o /dtn-tool ./cmd/dtn-tool

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
COPY --from=dtn7-go-builder /dtnd     /usr/local/sbin/
COPY --from=dtn7-go-builder /dtn-tool /usr/local/sbin/
