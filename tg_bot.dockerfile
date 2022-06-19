FROM python:3.8

WORKDIR /app

COPY tg_bot_docker /app/

RUN python -m pip install --upgrade pip

RUN python -m pip install pyTelegramBotAPI==4.5.1