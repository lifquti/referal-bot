from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot_app.db.users import get_task_use_url


def links_ikb(data, id):
    m = InlineKeyboardMarkup(row_width=1)
    for row in data:
        link = str(row['url']) + '?start=ref' + str(id)
        m.insert(InlineKeyboardButton(text=row['name_task'], url=link))
    m.insert(InlineKeyboardButton(text='Виконав всі завдання', callback_data='do_all_tasks'))
    return m


def channel_ikb(name_chanel):
    m = InlineKeyboardMarkup(resize=True, row_width=1)
    m.insert(InlineKeyboardButton(text='Canal', url='https://t.me/'+name_chanel))
    m.insert(InlineKeyboardButton(text='Виконав завдання', callback_data='do_all_tasks'))
    return m


async def new_tasks_ikb(url_list):
    m = InlineKeyboardMarkup(row_width=1)
    for url in url_list:
        get_task = await get_task_use_url(url)
        m.insert(InlineKeyboardButton(text=get_task['name'], url=url))
    m.insert(InlineKeyboardButton(text='Відмінити', callback_data='cancel'))
    return m


async def new_task_for_user_ikb(dict):
    m = InlineKeyboardMarkup(resize=True)
    m.insert(InlineKeyboardButton(text=f'{dict["name"]}', url=dict["url"]))
    return m

