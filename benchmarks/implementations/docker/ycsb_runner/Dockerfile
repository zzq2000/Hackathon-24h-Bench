ARG YCSB_BASE_IMAGE=eclipse-temurin:11-jre-jammy
FROM ${YCSB_BASE_IMAGE}

ARG YCSB_RELEASE_URL
ARG YCSB_RELEASE_FALLBACK_URL

ENV YCSB_HOME=/opt/ycsb

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates curl tar \
    && rm -rf /var/lib/apt/lists/*

COPY install_ycsb.sh /usr/local/bin/install_ycsb.sh
COPY run_ycsb.sh /usr/local/bin/run_ycsb.sh

RUN chmod +x /usr/local/bin/install_ycsb.sh \
    && chmod +x /usr/local/bin/run_ycsb.sh \
    && /usr/local/bin/install_ycsb.sh "$YCSB_HOME" "$YCSB_RELEASE_URL" "$YCSB_RELEASE_FALLBACK_URL"

WORKDIR /opt/ycsb
ENTRYPOINT ["/usr/local/bin/run_ycsb.sh"]
