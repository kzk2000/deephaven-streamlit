FROM docker.io/eclipse-temurin:21 as openjdk

FROM python:3.10-slim

# add basics
RUN set -eux \
    && apt-get update  \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV \
    LANG='en_US.UTF-8' \
    LANGUAGE='en_US:en' \
    LC_ALL='en_US.UTF-8'

# add Java
COPY --link --from=openjdk /opt/java/openjdk /opt/java/openjdk
ENV \
    JAVA_HOME="/opt/java/openjdk" \
    PATH="/opt/java/openjdk/bin:${PATH}"

ENV JAVA_VERSION 11.0.15
ENV JAVA_HOME /usr/lib/jvm/java-11-amazon-corretto

RUN pip3 install deephaven-server streamlit

ENTRYPOINT ["streamlit", "run", "/app/__init__.py", "--server.port=8501", "--server.address=0.0.0.0"]