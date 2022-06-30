from db_api.db_api import change_tg_notice_status
import requests
import os
import time
from datetime import datetime
import telebot


def main():
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    bot = telebot.TeleBot(token)
    while True:
        entries = change_tg_notice_status()
        if entries:
            bot.send_message(chat_id, '(номер заказа, стоимость $, срок доставки(год, мес, день), был ли удален из Google Sheet)')
            result = ''
            for row in entries:
                result += str(row) + '\n'
            bot.send_message(chat_id, result)
            print('was send notice about out of delivery date orders', datetime.now(), flush=True)
        time.sleep(60)


if __name__ == '__main__':
    # give a time to db-driver create and set database
    time.sleep(10)
    main()



