from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def links_ikb(data, id):
    m = InlineKeyboardMarkup(row_width=1)
    for row in data:
        if row['status'] == 'Active':
            link = str(row['url']) + '?start=ref' + str(id)
            m.insert(InlineKeyboardButton(text=row['name'], url=link))
    return m


def check_if_exist():
    m = InlineKeyboardMarkup(row_width=1)
    m.insert(KeyboardButton(text='Перевірити підписки'))
    return m

