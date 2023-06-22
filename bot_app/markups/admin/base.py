from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot_app.misc import _


def admin_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Перелік завдань')
    m2 = KeyboardButton('Зробити розсилку')
    m.add(m1, m2)
    return m


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton('Відмінити'))
    return m


def another_tasks():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Додати завдання')
    m2 = KeyboardButton('Прибрати завдання')
    m3 = KeyboardButton('Відмінити')
    m.add(m1, m2, m3)
    return m


def task_keyboard():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Початкові завдання')
    m2 = KeyboardButton('Додаткові завдання')
    m3 = KeyboardButton('Відмінити')
    m.add(m1, m2, m3)
    return m


def users_for_spam():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Всім користувачам')
    m2 = KeyboardButton('Тим хто виконав')
    m3 = KeyboardButton('Хто не виконав')
    m4 = KeyboardButton('Відмінити')
    m.insert(m1).add(m2, m3, m4)
    return m


def new_markup_creating():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.row(KeyboardButton('Без кнопки'))
    return m


def custom_urls_markup_dict(markup):
    m = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    for button in markup:
        m.add(InlineKeyboardButton(button['button_text'], url=button['button_url']))
    return m
