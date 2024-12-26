#!/bin/bash
set -e

psql --username "${POSTGRES_USER}" -d "${POSTGRES_DB}" <<-EOSQL
    CREATE DATABASE pgtest;
EOSQL
