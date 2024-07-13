from telebot import (
    types
)
import os
from .core import bot
from gigaChat import ai


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
                          'Ты можешь спросить у меня что-то или выбрать команду из меню!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def rnd_text_response(msg: types.Message):
    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waiting.gif')
    msgs_for_del = [bot.send_animation(chat_id=msg.chat.id,
                                       animation=open(gif_path, 'rb')),
                    bot.send_message(chat_id=msg.chat.id,
                                     text='Ваш запрос в обработке, пожалуйста, подождите несколько секунд...')
                    ]

    text, file_paths = ai.find_in_files(msg.text)
    right = ai.check_answer(query=msg.text, text_to_check=text)
    if right.lower() == "да":
        for msg_for_del in msgs_for_del:
            bot.delete_message(chat_id=msg.chat.id, message_id=msg_for_del.message_id)
        msgs_for_del = []
        if file_paths is not None:
            bot.send_message(chat_id=msg.chat.id, text=ai.reformat_text(msg.text))
            bot.send_message(chat_id=msg.chat.id, text='Вот откуда я взял эту информацию:')
            msgs_for_del.append(bot.send_message(chat_id=msg.chat.id, text='Файлы прогружаются...'))
            for file_path in file_paths:
                with open(file_path, 'rb') as file:
                    bot.send_document(msg.chat.id, file)
            for msg_for_del in msgs_for_del:
                bot.delete_message(chat_id=msg.chat.id, message_id=msg_for_del.message_id)
        else:
            bot.send_message(chat_id=msg.chat.id, text=text)
    else:
        bot.send_message(chat_id=msg.chat.id, text='Увы, я не знаю ответа на Ваш вопрос :(')
        for msg_for_del in msgs_for_del:
            bot.delete_message(chat_id=msg.chat.id, message_id=msg_for_del.message_id)


def run():
    print('running...')
    bot.infinity_polling()
