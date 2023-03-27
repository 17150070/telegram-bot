import logging

from telebot import types
from telebot.types import CallbackQuery

from business_logic.user import get_user_by_telegram_id, create_user_by_telegram_id
from config import bot
from models.users import User

logger = logging.getLogger(__name__)


def callback_inline_user(call: CallbackQuery):
    if call.message:
        if call.data == 'Личный кабинет':
            mark_up = types.InlineKeyboardMarkup(row_width=2)
            back = types.InlineKeyboardButton('Назад', callback_data='Назад')
            mark_up.add(back)

            try:
                user = get_user_by_telegram_id(call.from_user.id)

                if user is None:
                    bot.send_message(call.message.chat.id, "Пожалуйста используйте /start перед началом работы", reply_markup=mark_up)
                    return

                'Пользователь' + '\n\nВаше ID:' + '\nВаш Telegram ID:' + str() + \
                '\nВаш баланс: ' + '2000' + 'рублей' + '\nВаш тариф: полный'
                message = f'Пользователь {call.from_user.full_name}:\n\n' \
                          f'Ваше ID: {user.id}\n' \
                          f'Ваш Telegram ID: {call.from_user.id}\n' \
                          f'Ваш баланс: {user.balance}\n' \
                          f'Ваш тариф: полный'

            except Exception as err:
                logger.exception("Error during user fetch", err)
                bot.send_message(call.message.chat.id, f"Чел ты {err}", reply_markup=mark_up)
                return

            bot.send_message(call.message.chat.id, message, reply_markup=mark_up)


        elif call.data == 'Пополнить баланс':
            mark_up = types.InlineKeyboardMarkup(row_width=2)
            back = types.InlineKeyboardButton('Назад', callback_data='Назад')
            mark_up.add(back)
            bot.send_message(call.message.chat.id, 'Чуть позже появится', reply_markup=mark_up)

        elif call.data == 'Приобрести тариф':
            mark_up = types.InlineKeyboardMarkup(row_width=2)
            partial = types.InlineKeyboardButton('Частичный', callback_data='Частичный')
            average = types.InlineKeyboardButton('Средний', callback_data='Средний')
            full = types.InlineKeyboardButton('Полный', callback_data='Полный')
            back = types.InlineKeyboardButton('Назад', callback_data='Назад')
            mark_up.add(partial, average, full, back)
            bot.send_message(call.message.chat.id, 'Выберите тариф', reply_markup=mark_up)

        elif call.data == 'Техподдержка':
            mark_up = types.InlineKeyboardMarkup(row_width=2)
            back = types.InlineKeyboardButton('Назад', callback_data='Назад')
            mark_up.add(back)
            bot.send_message(call.message.chat.id, 'Чуть позже появится', reply_markup=mark_up)

        elif call.data == 'Назад':
            mark_up = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Личный кабинет', callback_data='Личный кабинет')
            item2 = types.InlineKeyboardButton('Пополнить баланс', callback_data='Пополнить баланс')
            item3 = types.InlineKeyboardButton('Приобрести тариф', callback_data='Приобрести тариф')
            item5 = types.InlineKeyboardButton('Техподдержка', callback_data='Техподдержка')
            mark_up.add(item1, item2, item3, item5)

            try:
                user: User = get_user_by_telegram_id(call.from_user.id)
                if user is not None:
                    if user.is_admin:
                        admin_button = types.InlineKeyboardButton('Админ', callback_data='Админ')
                        mark_up.add(admin_button)
                    bot.send_message(call.message.chat.id, f'Выберите действие', reply_markup=mark_up)
                    return
                create_user_by_telegram_id(call.from_user.id)
            except Exception as err:
                logger.exception(err)
                bot.send_message(call.message.chat.id, f'Чел прости я умер {err}', reply_markup=mark_up)
                return

            bot.send_message(call.message.chat.id, 'Выберите действие, {0.first_name}'.format(call.from_user),
                             reply_markup=mark_up)
