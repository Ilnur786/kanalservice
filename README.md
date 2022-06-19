# Тестовое задание для Каналсервис

### Сервис мониторит изменения в Google Sheet

Настройка и запуск:
* Клонируйте репозиторий на локальную машину git clone https://github.com/Ilnur786/kanalservice.git
* Заполните поле chat_id в конфиг файле config/.env.prod. Чтобы получить chat_id, запустите бота @username_to_id_bot.
* Бот присылающий уведомления доступен по адресу @kanalserviceNoticeBot
* Убедитесь что на вашей машине установлен docker и docker-compose
* Находясь в папке проекта запустите команду в терминале: docker-compose --env-file ./config/.env.prod up

Проект разрабатывался и тестировался на WSL2 (Ubuntu 20.04).


