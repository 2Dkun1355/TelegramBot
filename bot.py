import json

import telebot
from config import token
import requests

bot = telebot.TeleBot(token=token)
url = 'http://127.0.0.1:8000/api/vacancy/'


@bot.message_handler(commands=['start'])
def you_id(message):
    bot.send_message(message.chat.id, f"ID: {message.chat.id} Name: {message.from_user.first_name} ")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        for item in results:
            item_str = json.dumps(item, ensure_ascii=False, indent=4)
            bot.send_message(message.chat.id, item_str)


if __name__ == '__main__':
    bot.polling()