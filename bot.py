import json

import telebot
import requests

bot = telebot.TeleBot(token='7144823259:AAEborHn6X6yFNNOAwn4QZZylE3vhyEMh4w')
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
    auth(message)
    # додати кнопки "Знайти" та "Тест"
    # зареєструвати наступний крок menu

def menu(message, current_bot):
    pass

def process_search(message, current_bot):
    # вивести інформаційне повідомлення "Введіть параметри пошуку..."
    # зареєструвати наступний крок search_vacancies
    pass

def search_vacancies(message, current_bot):
    # зчитує параметри які ввів користувач  розбиває на окремі змінні
    # робить запит на АПІ з потрібними фільтрами
    # отримує відповідь з АПІ і формує текстове повідомлення з вакансіями та надсилає його юзеру

def process_test(message, current_bot):
    pass



if __name__ == '__main__':
    bot.polling()