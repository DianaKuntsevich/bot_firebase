

from environs import Env
import telebot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import db
from datetime import datetime, timezone, timedelta

env = Env()
env.read_env()

API_TOKEN = env('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


def generate_message(button):
    msg = ''
    if 'size' in button or 'price' in button:
        msg += f'<b>Услуга: {button["name"]}\n</b>'
    if 'size' in button:
        msg += f'<b>Размер услуги: {button['size']}\n\n</b>'
    msg += button['to_print'] + '\n'

    if 'price' in button:
        msg += '\n\n'
        msg += f'<b>Цена: {button['price']} BYN</b>'

    return msg


def get_all_buttons():
    config_data = db.get_collection('keyboard_name')
    all_buttons = []

    for keyboard in config_data:
        for button in keyboard['buttons']:
            all_buttons.append(button)
    return all_buttons


def get_keyboard(keyboard_name: str):
    config_data = db.get_collection('keyboard_name')

    actual_keyboard = list(filter(lambda el: el['keyboard_name'] == keyboard_name, config_data))[0]
    keyboard = InlineKeyboardMarkup()
    buttons = sorted(actual_keyboard['buttons'], key=lambda el: int(el['id']))

    for button in buttons:
        keyboard.add(InlineKeyboardButton(button['name'], callback_data=button['id']))

    return keyboard


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username}', reply_markup=get_keyboard('main'))


# @bot.message_handler(content_types=['text'])
# def wright_message(message: Message):
#     # now = datetime.now(timezone.utc) #получаем дату и время
#     # date = now.date() # получаем просто дату
#     counter = 0
#     while counter < 1000:
#         to_wright = {
#         "from_user_id": str(message.from_user.id),
#         "from_user_name": str(message.from_user.username),
#         "text": str(message.text)
#
#         }
#         count = 0
#         while count < counter:
#             db.set_document('messages', f'bot{str(count)}', to_wright)
#             count += 1
#         counter += 1








# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message: Message):
#     bot.reply_to(message, message.text)


@bot.callback_query_handler(func=lambda call:True)
def common_button(call: CallbackQuery):
    button = list(filter(lambda btn: call.data == btn['id'], get_all_buttons()))[0]
    bot.send_message(
        chat_id=call.message.chat.id,
        text =generate_message(button),
        reply_markup=get_keyboard(button['next_keyboard']),
        parse_mode='html'
    )



bot.infinity_polling()




