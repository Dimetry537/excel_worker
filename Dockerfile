FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1 \
    PIP_VERSION=22.1.2 \
    ORACLE_CLIENT=/opt/oracle/instantclient_23_9

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    make \
    git \
    bash \
    wget \
    unzip \
    libaio-dev \
    fonts-dejavu-core


RUN pip install --upgrade "pip==$PIP_VERSION" && pip install "poetry==$POETRY_VERSION"

WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2390000/instantclient-basic-linux.x64-23.9.0.25.07.zip \
        && unzip instantclient-basic-linux.x64-23.9.0.25.07.zip \
        && rm instantclient-basic-linux.x64-23.9.0.25.07.zip \
        && ln -s /opt/oracle/instantclient_23_9/libclntsh.so /usr/lib/libclntsh.so
        
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_23_9

RUN echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
RUN ls -la /opt/oracle/instantclient_23_9

WORKDIR /app

COPY . /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["python3", "main.py"]
