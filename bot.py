import telebot
from telebot import types
import requests
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from db_backend import DB

# from config import token

bot = telebot.TeleBot(token='7144823259:AAEborHn6X6yFNNOAwn4QZZylE3vhyEMh4w')
API_URL = 'http://127.0.0.1:8000'

db = DB()


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

def create_keyboard(options, prefix):
    buttons = [InlineKeyboardButton(option, callback_data=f"{prefix}_{option}") for option in options]
    markup = InlineKeyboardMarkup()
    markup.row(*buttons)
    return markup

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
    programming_language = ["Python", "Java", "JavaScript", "C++", "PHP"]
    markup = create_keyboard(programming_language, "programming_language")
    bot.send_message(message.chat.id, "Мова програмування:", reply_markup=markup)

    level_need = ["Junior", "Middle", "Senior"]
    markup = create_keyboard(level_need, "level_need")
    bot.send_message(message.chat.id, "Рівень програмування:", reply_markup=markup)

    location = ["Lviv", "Odesa", "Kyiv", "віддалено"]
    markup = create_keyboard(location, "location")
    bot.send_message(message.chat.id, "Місто:", reply_markup=markup)

    action = ["Пошук", "Скасувати"]
    markup = create_keyboard(action, "search")
    bot.send_message(message.chat.id, "Виберіть опцію:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_selection(call):
    category = call.data.rsplit('_', 1)[0]
    button = call.data.split('_')[-1]
    chat_id = call.message.chat.id


    # if chat_id not in db.chats():
    #     db.update(chat_id, {})
    if category in ["programming_language", "level_need"]:
        db.update(chat_id, {category: button})
    elif category == "location":
        if button != "віддалено":
            db.update(chat_id, {category: button})
        else:
            db.update(chat_id, {"is_remote": True})

    elif category == "search" and button == "Пошук":
        search_vacancies(call.message)
    elif category == "search" and button == "Скасувати":
        db.clear(chat_id)

def search_vacancies(message):
    url_search = f"{API_URL}/api/vacancy/"
    try:
        # робить запит на АПІ з потрібними фільтрами
        response = requests.get(url_search, params=db.get(message.chat.id))
        if response.status_code == 200:
            results = response.json().get('results', [])
            for item in results:
                bot.send_message(message.chat.id, f"{item.get('programming_language')}\n{item.get('url')}")

        # отримує відповідь з АПІ і формує текстове повідомлення з вакансіями та надсилає його юзеру

        # user_search_create(message, search.get(message.chat.id))
    except:
        pass


def get_user(message):
    url = f'{API_URL}/api/user/?telegram_id={message.chat.id}'
    response = requests.get(url=url)
    if response.ok and response.json() and response.json().get('count') >= 1:
        user = response.json().get('results', [])[0]
        return user.get('id')
    return None


def user_search_create(message, data):
    user_id = get_user(message)
    data.update({'user': user_id})
    url = f'{API_URL}/api/user-search/'
    response = requests.post(url=url, data=data)


def process_test(message):
    bot.send_message(message.chat.id, "Тестова кнопка, просто щоб була :)")

if __name__ == '__main__':
    bot.polling()