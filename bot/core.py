from telebot import (
    TeleBot
)
import sqlalchemy
import os
from dotenv import load_dotenv
load_dotenv()

bot = TeleBot(token=os.getenv('BOT_TOKEN'))
