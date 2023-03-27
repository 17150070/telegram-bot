import logging

from telebot import types

from business_logic.admin_menu import callback_inline_admin
from business_logic.user import create_user_by_telegram_id, get_user_by_telegram_id
from models.users import User
from business_logic.user_menu import callback_inline_user
from config import bot

logging.basicConfig(level=logging.INFO, format='[%(name)s] [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])  # Явно указываем в декораторе, на какую команду реагируем.
def send_welcome(message: types.Message):
    mark_up = types.InlineKeyboardMarkup(row_width=2)
    # mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # # resize_keyboard позволяет менять размер кнопок

    item1 = types.InlineKeyboardButton('Личный кабинет', callback_data='Личный кабинет')
    item2 = types.InlineKeyboardButton('Пополнить баланс', callback_data='Пополнить баланс')
    item3 = types.InlineKeyboardButton('Приобрести тариф', callback_data='Приобрести тариф')
    item5 = types.InlineKeyboardButton('Техподдержка', callback_data='Техподдержка')

    mark_up.add(item1, item2, item3, item5)

    try:
        user: User = get_user_by_telegram_id(message.from_user.id)
        if user is not None:
            if user.is_admin:
                admin_button = types.InlineKeyboardButton('Админ', callback_data='Админ')
                mark_up.add(admin_button)
            bot.send_message(message.chat.id, f'Добро пожаловать, рады что вы вернулись!', reply_markup=mark_up)

            return

        create_user_by_telegram_id(message.from_user.id)

    except Exception as err:
        logger.exception(err)
        bot.send_message(message.chat.id, f'Чел прости я умер {err}', reply_markup=mark_up)
        return

    bot.send_message(message.chat.id, 'Добро пожаловать! Выберите действие, {0.first_name}'.format(message.from_user),
                     reply_markup=mark_up)


@bot.callback_query_handler(func=lambda call: True)  # вешаем обработчик событий на нажатие всех inline-кнопок
def callback_inline(message):
    user: User = get_user_by_telegram_id(message.from_user.id)
    if user.is_admin:
        callback_inline_admin(message)
    else:
        callback_inline_user(message)


logger.info("Telegram bot starting...")
bot.polling(none_stop=True)  # бесперебойное подключение бота
