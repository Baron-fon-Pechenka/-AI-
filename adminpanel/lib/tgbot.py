import telebot
import os
from dotenv import load_dotenv
load_dotenv()

# Указываем токен вашего бота
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет!")

# Запускаем бота
bot.infinity_polling()
