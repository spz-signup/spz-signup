# base information
FROM debian:jessie
MAINTAINER Marco Neumann <marco@crepererum.net>

# versions
ENV LIBASR_VERSION="1.0.2" \
    OPENSMPTD_VERSION="5.9.2p1" \
    LIBASR_SHA512="a4825a30130f70a452044c484871ac37459e1c1e6659c4c38dead7d3abbdaecb3517b7accb46586537975fee033857566fd279ecf97ae87dc80bb6bcdd467d3e" \
    OPENSMPTD_SHA512="99ca15101557848aa6d642f0c0171b152d805192e6839a97410b19431c981a21a5c0dc011e2c8cd91f3e6f6acb37a77f0f4c8e68114bf9808240392fe2b5d375"

# upgrade system and install deps
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends bison ca-certificates file gcc libevent-dev libssl-dev make wget && \
    rm -rf /root/.cache /var/cache/*

# build opensmtpd and prepare system
RUN mkdir src && \
    cd src && \
    wget "https://www.opensmtpd.org/archives/libasr-$LIBASR_VERSION.tar.gz" && \
    wget "https://www.opensmtpd.org/archives/opensmtpd-$OPENSMPTD_VERSION.tar.gz" && \
    (echo "$LIBASR_SHA512 libasr-$LIBASR_VERSION.tar.gz" | sha512sum --check -) && \
    (echo "$OPENSMPTD_SHA512 opensmtpd-$OPENSMPTD_VERSION.tar.gz" | sha512sum --check -) && \
    tar xf libasr-$LIBASR_VERSION.tar.gz && \
    tar xf opensmtpd-$OPENSMPTD_VERSION.tar.gz && \
    cd libasr-$LIBASR_VERSION && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd ../opensmtpd-$OPENSMPTD_VERSION && \
    ./configure --prefix=/usr --with-path-CAfile=/etc/ssl/certs/ca-certificates.crt && \
    make && \
    make install && \
    cd ../.. && \
    rm -rf src && \
    useradd --uid 1000 _smtpd && \
    useradd --uid 1001 _smtpq && \
    mkdir /var/empty

# expose only simple, unencrypted SMTP port
EXPOSE 25

# copy config
COPY smtpd.conf /etc/smtpd.conf

# standard command
CMD ["/usr/sbin/smtpd", "-f", "/etc/smtpd.conf", "-d"]
