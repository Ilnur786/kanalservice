FROM python:3.8

WORKDIR /app

COPY db_api /app/db_api

COPY exchange_api /app/exchange_api

COPY send_tg_notice_docker /app/

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt