import telebot
from telebot import types

from account_manager import *
from util import *

# constants

bot = telebot.TeleBot('5708218868:AAER7yY4DCP8gQpVU2mFrmNlsEcpYQ_jxwU')

status = ['member', 'administrator', 'creator']  # allowed statuses
group_id = -1001578519176  # channel id for check subscribing


@bot.message_handler(commands=['start'])
def start(message):
    bot.delete_message(message.chat.id, message.id, timeout=100)  # delete user start message

    register(message.chat.id, message.chat.username, message)  # registering message ot database

    unique_code = extract_unique_code(message.text)  # taking referral link id
    if unique_code:  # If referral code existing

        if add_balance(message.from_user.id, unique_code):  # adding balance (+1) for referral
            keyboard = [[types.InlineKeyboardButton("🔻Удалить это сообщение🔻",
                                                    callback_data=f'delete{message.id + 1}')]]
            markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=unique_code, text='🔻У вас новый реферал🔻', reply_markup=markup)

    if is_subscribed(group_id, message.from_user.id, bot, status):  # checking if user subscribed
        main_menu(message)  # printing main menu
    else:
        bot.send_message(message.chat.id, 'Для начала подпишитесь на наш телеграм канал t.me/vipege2023',
                         parse_mode='html')  # need to subscribe message


def main_menu(message):
    keyboard = [[types.InlineKeyboardButton("🔻EГЭ ответы🔻", callback_data=f'ege')],
                [types.InlineKeyboardButton("🔻ОГЭ ответы🔻", callback_data=f'oge')],
                [types.InlineKeyboardButton("🔻ВПР ответы🔻", callback_data=f'vpr')],
                [types.InlineKeyboardButton("🏆Наши гарантии🏆", callback_data=f'guaranties')],
                [types.InlineKeyboardButton("🔑Моя ссылка / Баланс🔑", callback_data=f'account')]]
    markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, "🔝 Главное меню 🔝", reply_markup=markup)


def account_print(user_id, call):  # print user account data
    balance = get_balance(user_id)  # getting user balance from database

    if int(balance) >= 10:
        keyboard = [[types.InlineKeyboardButton("🔻Назад🔻", callback_data='back')],
                    [types.InlineKeyboardButton("🔻Купить ответы🔻", callback_data='buy_answers')]]
    else:
        keyboard = [[types.InlineKeyboardButton("🔻Назад🔻", callback_data='back')]]

    message = f'Привет! \n👉Ты пригласил - {balance} человек' \
              f'\n\n👉Твоя личная ссылка - https://t.me/vipege_bot?start={user_id}' \
              f'\n👉 Личная ссылка для распространения ВК - https://teleg.run/vipege_bot?start={user_id}' \
              f'\n\n✔️Копируй и рассылай друзьям,' \
              f'кидай в группы с ЕГЭ, ОГЭ, ВПР, в беседы, комметария чтобы быстро набрать людей!' \
              f'\n\n✔️Пригласи 10 человек чтобы получить ответы!'

    markup = types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message,
                          reply_markup=markup)  # editing main message


def ege_print(user_id, call):  # need to rewrite for adding answers
    keyboard = [[types.InlineKeyboardButton("🔻Назад🔻", callback_data='back')]]
    markup = types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text='🔻Выберите регион🔻',
                          reply_markup=markup)


def oge_print(user_id, call):  # need to rewrite for adding answers
    keyboard = [[types.InlineKeyboardButton("🔻Назад🔻", callback_data='back')]]
    markup = types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text='🔻Выберите регион🔻',
                          reply_markup=markup)


def vpr_print(user_id, call):  # need to rewrite for adding answers
    keyboard = [[types.InlineKeyboardButton("🔻Назад🔻", callback_data='back')]]
    markup = types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text='🔻Выберите класс🔻',
                          reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def get_user_commands(call):  # getting data from button pressing
    user_message = "".join(re.findall(r"[a-z]", call.data))
    try:
        user_id = int("".join(re.findall(r"[0-9]", call.data)))  # if user callback contains id
    except Exception:  # checking for id in callback
        pass
    if user_message == "ege":
        ege_print(call.message.chat.id, call)
    if user_message == "oge":
        oge_print(call.message.chat.id, call)
    if user_message == "vpr":
        vpr_print(call.message.chat.id, call)
    if user_message == "guaranties":
        guaranties_print(call)
    if user_message == "account":
        account_print(call.message.chat.id, call)
    if user_message == "back":
        keyboard = [[types.InlineKeyboardButton("🔻EГЭ ответы🔻", callback_data=f'ege')],
                    [types.InlineKeyboardButton("🔻ОГЭ ответы🔻", callback_data=f'oge')],
                    [types.InlineKeyboardButton("🔻ВПР ответы🔻", callback_data=f'vpr')],
                    [types.InlineKeyboardButton("🏆Наши гарантии🏆", callback_data=f'guaranties')],
                    [types.InlineKeyboardButton("🔑Моя ссылка / Баланс🔑", callback_data=f'account')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="🔝 Главное меню 🔝", reply_markup=markup)  # menu printing
    if user_message == "buy_answers":
        buy_answers(call.message.chat.id)
    if user_message == "delete":
        bot.delete_message(call.message.chat.id, user_id)


def buy_answers(user_id):  # need to rewrite for changing text message
    balance = get_balance(user_id)
    if int(balance) < 10:
        bot.send_message(user_id, 'Нехватает валюты')
        return False
    else:
        remove_balance(user_id, 10)
        # need to write


def guaranties_print(call):
    keyboard = [[types.InlineKeyboardButton("🔻Назад🔻", callback_data='back')]]
    markup = types.InlineKeyboardMarkup(keyboard)
    message = f'Наши гарантии 👑 \n\n1. Это совершенно бесплатно. Получая ответы бесплатно вы ничего не теряете! \n\n' \
              f'2. Мы сотрудничаем с крупным проектом по ответами ЕГЭ / ОГЭ \n\n' \
              f'3. У нас есть поставщики а именно региональные координаторы ОГЭ и ЕГЭ  через которых мы получаем ' \
              f'материалы \n\n' \
              f'4. Мы имеет доступ на все VIP популярных групп и каналов по ответам ЕГЭ и ОГЭ \n\n' \
              f'5. Мы рассылаем ответы БЕСПЛАТНО со всех популярных VIP каналов по ответам! \n\n' \
              f'6. В чем наша выгода спросите вы? Выгода в посещаемости нашего бота! Мы от вас просим лишь ' \
              f'приглашать друзей и ' \
              f'все! Вы приглашаете а мы даём бесплатные ответы! ' \
              f'\n\n‼️Примеры + гарантии - {123}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=message, reply_markup=markup)


@bot.message_handler()
def get_user_text(message):
    try:
        if message.text == '192837465':
            admin_update(message.chat.id)
    except Exception:
        pass


bot.polling(none_stop=True)  # bot starting
