import telebot

from token import TOKEN

API_TOKEN = TOKEN
# API_TOKEN = 'Вставьте свой телеграм токен'

# Инициализируем проект ниже
bot = telebot.TeleBot(API_TOKEN)
