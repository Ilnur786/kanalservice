FROM python:3.8

WORKDIR /app

COPY db_api /app/db_api

COPY web_app_service /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

RUN python -m pip install dash==2.5.1
