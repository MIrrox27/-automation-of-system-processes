from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from ourClass.ClassBot import Bot
from ourClass.ClassHTTPService import HTTPService

# Функция, которая будет обрабатывать команду /start



parametrs = {
    'message': "None",
    'color': "a2222",
    'state': "228666"
}
finalIPofServer = int(input("Введите последнюю цифру ip сервера: "))
server = f"http://192.168.0.{finalIPofServer}/light" #замените на ваш ip
token = "ваш токен"
requets = HTTPService(server, parametrs=parametrs)

def main():
    global token
    # Вставь сюда свой токен
    updater = Updater(token)
    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    myBot = Bot()

    # Регистрация обработчика команды /start
    dispatcher.add_handler(CommandHandler("start", myBot.start))
    dispatcher.add_handler(CommandHandler("users", myBot.list_users))

    # Запуск бота
    updater.start_polling()

    # Ожидание завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
    parametrs = {
        "red": {'D5': 0, 'D6': 1, 'D7': 0},
        "blue": {'D5': 0, 'D6': 0, 'D7': 1},
        "green": {'D5': 1, 'D6': 0, 'D7': 0},
        "white": {'D5': 1, 'D6': 1, 'D7': 1},
        "black": {'D5': 0, 'D6': 0, 'D7': 0}
    }