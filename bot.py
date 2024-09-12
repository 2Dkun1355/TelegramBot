import json
import telebot
from telebot import types
import requests
from config import token

bot = telebot.TeleBot(token=token)
API_URL = 'http://127.0.0.1:8000'

def auth(message):
    url = f'{API_URL}/auth/users/'
    data = {
        'username': f'{message.chat.id}',
        'password': f'{message.chat.id}',
    }
    response = requests.post(url=url, data=data)

    if response.status_code == 201:
        user_id = response.json().get('id')
        url_next = f'{API_URL}/api/user-additional/'
        data_next = {
          "user": user_id,
          "telegram_id": message.chat.id,
        }
        response = requests.post(url=url_next, data=data_next)

@bot.message_handler(commands=['start'])
def start(message):
    # auth(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Знайти"),
        types.KeyboardButton("Тест"),
    )

    bot.send_message(message.chat.id, "Виберіть опцію:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.text == 'Знайти':
        process_search(message)
    elif message.text == 'Тест':
        process_test(message)

def process_search(message):
    bot.send_message(message.chat.id, f"Введіть параметри пошуку в форматі:\n"
                                      f"Мова програмування\n"
                                      f"Рівень\n"
                                      f"Місто чи віддалено")
    bot.register_next_step_handler(message, search_vacancies)

def search_vacancies(message):
    # зчитує параметри які ввів користувач  розбиває на окремі змінні
    # робить запит на АПІ з потрібними фільтрами
    # отримує відповідь з АПІ і формує текстове повідомлення з вакансіями та надсилає його юзеру
    try:
        text = message.text.split()
        data = {'programming_language': text[0],
                'level_need': text[1],
                }
        if text[2].lower() == 'віддалено':
            data.update({
                'is_remote': True
            })
        else:
            data.update({
                'location': text[2]
            })
    except:
        pass

def process_test(message):
    bot.send_message(message.chat.id, "Тестова кнопка, просто щоб була :)")

if __name__ == '__main__':
    bot.polling()