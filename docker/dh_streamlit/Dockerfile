FROM docker.io/eclipse-temurin:21 as openjdk

FROM python:3.11-slim

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

# add Python packages
COPY requirements.txt /requirements.txt
RUN pip3 install -r ./requirements.txt

WORKDIR /app

ENTRYPOINT ["streamlit", "run", "app.py"]
