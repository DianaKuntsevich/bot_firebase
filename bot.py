import json
from environs import Env
import telebot
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

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
    with open('keyboard.json', encoding='utf-8') as menu_config:
        config_data = json.load(menu_config)

    all_buttons = []
    for keyboard in config_data:
        for button in keyboard['buttons']:
            all_buttons.append(button)

    return all_buttons

def get_keyboard(keyboard_name: str):
    with open('keyboard.json', encoding='utf-8') as menu_config:
        config_data = json.load(menu_config)

    actual_keyboard = list(filter(lambda el: el ['keyboard_name'] == keyboard_name, config_data))[0]
    keyboard = InlineKeyboardMarkup()
    buttons = sorted(actual_keyboard['buttons'], key=lambda el: int(el['id']))

    for button in buttons:
        keyboard.add(InlineKeyboardButton(button['name'], callback_data=button['id']))

    return keyboard



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.username}', reply_markup=get_keyboard('main') )


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