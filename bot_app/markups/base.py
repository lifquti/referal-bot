from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def links_ikb():
    m = InlineKeyboardMarkup(row_width=1)
    m1 = InlineKeyboardButton(text='Перший канал', url='https://t.me/+ZYPdy0cljAMwZjAy')
    m2 = InlineKeyboardButton(text='Другий канал', url='https://t.me/+7iq0hPsoYuNlY2Uy')
    m3 = InlineKeyboardButton(text='Третій канал', url='https://t.me/thtrdhtrh', callback_data='check_connection')
    m.add(m1, m2, m3)
    return m


def check_if_exist():
    m = InlineKeyboardMarkup(row_width=1)
    m.insert(KeyboardButton(text='Перевірити підписки'))
    return m

