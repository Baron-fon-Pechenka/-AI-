from telegram.ext import Updater, CommandHandler

# Функция, которая будет вызываться при команде /start
def start(update, context):
    # Отправляем приветственное сообщение
    update.message.reply_text('Привет! Я бот. Как дела?')

def main():
    # Токен вашего бота, полученный от BotFather в Telegram
    token = '1164848717:AAGrwsNOiyLW6HXC2lPj_KFJDzKAAaVlTu8'
    
    # Создаем объект Updater и передаем ему токен бота
    updater = Updater(token, use_context=True)
    
    # Получаем диспетчер для обработчиков команд
    dispatcher = updater.dispatcher
    
    # Добавляем обработчик для команды /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Начинаем поиск обновлений
    updater.start_polling()
    
    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
