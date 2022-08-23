def old_account_print(user_id):

    balance = get_balance(user_id)

    markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item_back = types.KeyboardButton(text='Назад🔻')

    if int(balance) >= 10:
        item_buy = types.KeyboardButton(text='Купить ответ🔻')
        markup_inline.add(item_back, item_buy)
    else:
        markup_inline.add(item_back)

    message = f'Привет! \n👉Ты пригласил - {balance} человек' \
              f'\n\n👉Твоя личная ссылка - https://t.me/vipege_bot?start={user_id}' \
              f'\n👉 Личная ссылка для распространения ВК - https://teleg.run/vipege_bot?start={user_id}' \
              f'\n\n✔️Копируй и рассылай друзьям,' \
              f'кидай в группы с ЕГЭ, ОГЭ, ВПР, в беседы, комметария чтобы быстро набрать людей!' \
              f'\n\n✔️Пригласи 10 человек чтобы получить ответы!'

    bot.send_message(user_id, message, reply_markup=markup_inline)


def old_main_menu(message):
    markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    # main menu buttons

    item_ege = types.KeyboardButton(text='EГЭ ответы🔻')
    item_oge = types.KeyboardButton(text='ОГЭ ответы🔻')
    item_vpr = types.KeyboardButton(text='ВПР ответы🔻')
    item_guaranties = types.KeyboardButton(text='Наши гарантии🏆')
    item_account = types.KeyboardButton(text='Моя ссылка / Баланс🔑')

    markup_inline.add(item_ege, item_oge, item_vpr, item_account, item_guaranties)
    bot.send_message(message.chat.id, "🔝 Главное меню", reply_markup=markup_inline)


@bot.message_handler()
def get_user_text(message):
    try:
        if message.text == 'EГЭ ответы🔻':
            print('ege')
        elif message.text == 'ОГЭ ответы🔻':
            print('oge')
        elif message.text == 'ВПР ответы🔻':
            print('vpr')
        elif message.text == 'Наши гарантии🏆':
            print('guaranties')
        elif message.text == 'Моя ссылка / Баланс🔑':
            delete_last_bot_message(message, bot)
            account_print(message.chat.id)
        elif message.text == 'Купить ответ🔻':
            delete_last_bot_message(message, bot)
            buy_answers(message.chat.id)
        elif message.text == 'Назад🔻':
            delete_last_bot_message(message, bot)
            main_menu(message)

    except ApiTelegramException:
        print('exception raised')  # need to change
