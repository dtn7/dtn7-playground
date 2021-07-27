### Container to build dtn7-go
FROM golang:1.15 AS dtn7-go-builder

COPY dtn7-go /dtn7-go
WORKDIR /dtn7-go
RUN go build -race -o /dtnd ./cmd/dtnd \
  && go build -race -o /dtn-tool ./cmd/dtn-tool


### CORE Container
FROM maciresearch/core_worker:7.5.1-1

RUN apt-get update \
  && apt-get install --no-install-recommends -yq \
  libtk-img \
  lxterminal \
  tmux \
  wireshark \
  && apt-get clean

RUN echo 'custom_services_dir = /root/.core/myservices' >> /etc/core/core.conf

COPY icons/normal/* /usr/local/share/core/icons/normal/
COPY icons/tiny/* /usr/local/share/core/icons/tiny/

COPY --from=dtn7-go-builder /dtnd     /usr/local/sbin/
COPY --from=dtn7-go-builder /dtn-tool /usr/local/sbin/
