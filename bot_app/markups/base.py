from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def links_ikb(data, id):
    m = InlineKeyboardMarkup(row_width=1)
    for row in data:
        link = str(row['url']) + '?start=ref' + str(id)
        m.insert(InlineKeyboardButton(text=row['name_task'], url=link))
    return m


# def check_if_exist():
#     m = InlineKeyboardMarkup(row_width=1)
#     m.insert(KeyboardButton(text='Перевірити підписки'))
#     return m


def channel_ikb(name_chanel):
    m = InlineKeyboardMarkup()
    m.insert(InlineKeyboardButton(text='Canal', url='https://t.me/'+name_chanel))
    return m
