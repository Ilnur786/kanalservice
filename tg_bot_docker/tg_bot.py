import telebot
import os

token = os.getenv('token')

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Пришлю просроченные заказы')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)