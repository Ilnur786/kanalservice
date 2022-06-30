FROM python:3.8

WORKDIR /app

COPY db_api /app/db_api

COPY df_api /app/df_api

COPY exchange_api /app/exchange_api

COPY update_db_service /app/

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt