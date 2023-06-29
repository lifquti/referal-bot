
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot_app.misc import _


def user_main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton(text='Нові завдання')
    m2 = KeyboardButton(text='Реферальна програма')
    m3 = KeyboardButton(text='Баланс')
    m.add(m1, m2, m3)
    return m


def balance_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m1 = KeyboardButton(text='Вивести баланс')
    m2 = KeyboardButton(text='Головне меню')
    m.add(m1, m2)
    return m
