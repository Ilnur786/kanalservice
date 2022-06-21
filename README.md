# Тестовое задание для Каналсервис

## Сервис мониторит изменения в Google Sheet

Ссылка на Google Sheet: https://docs.google.com/spreadsheets/d/1PsVLEBmCdrp9R8KSIqGC8eD252DIa26IYSOnatMkAUU/edit#gid=0

Настройка и запуск:
* Клонируйте репозиторий на локальную машину git clone https://github.com/Ilnur786/kanalservice.git
* Заполните поле chat_id в конфиг файле config/.env.prod. Чтобы получить chat_id, запустите бота @username_to_id_bot.
* Бот присылающий уведомления доступен по адресу @kanalserviceNoticeBot.
* Перед запуском докер композа обязательно найдите бота в тг
* Убедитесь что на вашей машине установлен docker и docker-compose
* Находясь в папке проекта запустите команду в терминале: sudo docker-compose --env-file ./config/.env.prod up

### Время обновления:
- Скрипт проверят Google Sheet раз в минуту
- Скрипт проверяет просроченные заказы раз в минуту

### Если хотите собрать композ заново:
- удалить базу (опционально) sudo rm -rf db-data
- docker-compose rm -f
- sudo docker-compose --env-file ./config/.env.prod build
- sudo docker-compose --env-file ./config/.env.prod up

Проект разрабатывался и тестировался на WSL2 (Ubuntu 20.04).


