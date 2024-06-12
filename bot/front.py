from telebot import (
    types
)
from core import bot


@bot.message_handler(commands=['start'])
def hello(msg: types.Message):
    keyboard_texts = ['Документы для поступления', 'Дообучение', 'Целевое обучение', 'Способы поступления',
                      'Проходные баллы']
    keyboard = types.ReplyKeyboardMarkup()
    temp = []
    for item in keyboard_texts:
        temp.append(types.KeyboardButton(text=item))
        if len(temp) == 3:
            keyboard.add(temp[0], temp[1], temp[2])
            temp = []
    if len(temp) != 0:
        for item in temp:
            keyboard.add(item)

    bot.send_message(chat_id=msg.chat.id,
                     text='Привет, я информационная система для поступающих в КУБГАУ! '
                          'Ты можешь спросить у меня что-то или выбрать команду из меню!',reply_markup=keyboard)


print('running...')
bot.polling()
