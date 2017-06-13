FROM ubuntu:16.04

RUN sh -ex \
    && apt-get update \
    && apt-get install -y pdns-recursor \
    && :

ENTRYPOINT ["/usr/sbin/pdns_recursor", "--local-address=0.0.0.0"]
