from ourClass.ClassHTTPService import HTTPService
from ourClass.ClassFunctionsOS import Windows_system, Commands
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

class Bot(HTTPService):
    def __init__(self):
        self.bot = None
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.usersPath = f'..\\telegramControl\\telegramHistory\\users.txt'
        self.users = Windows_system._read(self.usersPath)


    def start(self, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        # Проверяем, есть ли пользователь уже в списке
        if f"{user.id}" not in self.users or f"{user.username}" not in users:
            Windows_system._write(
                f"id: {user.id}, username: @{user.username}, first_name: {user.first_name}, last_name: {user.last_name} \n",
                self.usersPath)
        update.message.reply_text('Привет! Я твой бот.')

    # Функция для команды /users
    def list_users(self, update: Update, context: CallbackContext) -> None:
        user_list = f"Список пользователей:\n {self.users}"
        update.message.reply_text(user_list)