from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_app.misc import _


def admin_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Перелік завдань')
    m2 = KeyboardButton('Додати завдання')
    m.add(m1, m2)
    return m


def status_keyboard():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Active')
    m2 = KeyboardButton('Inactive')
    m.add(m1, m2)
    return m


def cancel():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton('Відмінити'))
    return m


def task_keyboard():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton('Початкові завдання')
    m2 = KeyboardButton('Додаткові завдання')
    m3 = KeyboardButton('Відмінити')
    m.add(m1, m2, m3)
    return m
