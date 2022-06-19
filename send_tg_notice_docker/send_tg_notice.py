from db_api.db_api import change_tg_notice_status
import requests
import os
import time

token = os.getenv('token')
chat_id = os.getenv('chat_id')


def send_telegram(text: str):
    """
    Send entries to specified chat_id.
    :param text: obviously given entry.
    :return: None.
    """
    url = "https://api.telegram.org/bot"
    channel_id = chat_id
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")


def main():
    entries = change_tg_notice_status()
    if entries:
        send_telegram('(номер заказа, стоимость $, срок доставки(год, мес, день), был ли удален из Google Sheet)')
        for row in entries:
            send_telegram(str(row))


if __name__ == '__main__':
    main()
    while True:
        time.sleep(60)
        main()

