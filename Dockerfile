FROM python:3.10-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.1 \
  PIP_VERSION=22.1.2

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
    libaio1 \
    libnsl2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade "pip==$PIP_VERSION" \
    && pip install "poetry==$POETRY_VERSION"

WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2120000/instantclient-basic-linux.x64-21.20.0.0.0dbru.zip \
    && wget https://download.oracle.com/otn_software/linux/instantclient/2120000/instantclient-sqlplus-linux.x64-21.20.0.0.0dbru.zip \
    && unzip -o instantclient-basic-linux.x64-21.20.0.0.0dbru.zip \
    && unzip -o instantclient-sqlplus-linux.x64-21.20.0.0.0dbru.zip \
    && rm instantclient-basic-linux.x64-21.20.0.0.0dbru.zip \
    && rm instantclient-sqlplus-linux.x64-21.20.0.0.0dbru.zip \
    && ln -s /opt/oracle/instantclient_21_20/libclntsh.so /usr/lib/libclntsh.so \
    && ln -s /opt/oracle/instantclient_21_20/libsqlplus.so /usr/lib/libsqlplus.so

ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_21_20

WORKDIR /app
COPY . /app/
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \ 
  && poetry install --no-interaction --no-ansi

CMD ["python3", "main.py"]
