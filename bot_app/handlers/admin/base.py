import re

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app.db.admin import set_task_db, get_all_tasks
from bot_app.markups.admin.base import status_keyboard, cancel, admin_menu
from bot_app.misc import bot, dp, _, _l
from bot_app import markups, config
from bot_app.misc import bot, dp
from bot_app.states.admin import Admin


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), commands=['admin'], state='*')
async def process_start(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Вітаю в адмін меню',
                           reply_markup=admin_menu())
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Додати завдання')
async def add_name_task(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Відправте назву силки', reply_markup=cancel())
    await state.set_state(Admin.Task.name_task)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Відмінити', state='*')
async def cancel_add(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, text='Ви повернулись на головне меню', reply_markup=admin_menu())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.name_task)
async def add_url_task(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await bot.send_message(message.from_user.id, text='Додайте силку на канал', reply_markup=cancel())
    await state.set_state(Admin.Task.url_task)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.url_task)
async def wrong_url(message: Message, state: FSMContext):
    regexp = re.compile(
        r'(?:http[s]?:\/\/.)?[-a-zA-Z0-9@%._\+~#=]{1,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)')
    matches = re.findall(regexp, message.text)

    if not matches:
        await bot.send_message(message.from_user.id,
                               text='Не правильно написана силка, ось вам приклад, спробуйте знову:\n'
                                    'https://t.me/referal3_bot',)

        return

    #TODO update link
    await state.update_data({'status': message.text})

    await state.set_state(Admin.Task.status)
    await bot.send_message(message.from_user.id, text='Виберіть статус завдання', reply_markup=status_keyboard())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.status)
async def add_payment(message: Message, state: FSMContext):
    await state.update_data({'status': message.text})
    await bot.send_message(message.from_user.id, text='Додайте сумму за це завдання', reply_markup=cancel())
    await state.set_state(Admin.Task.payment)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.payment)
async def add_to_db(message: Message, state: FSMContext):
    info = await state.get_data()
    name_chanel = str(info['url'])[13:]
    chat_info = await bot.get_chat(chat_id='@'+name_chanel)
    await state.update_data({'payment': message.text, 'group_id': chat_info.id})
    await set_task_db(state.get_data())
    await bot.send_message(message.from_user.id, text='Ви додали нове завдання:\n'
                                                      f'\tНазва завдання(кнопки)\n{info["name"]}\n'
                                                      f'\tПосилання на сайт або канал\n{info["url"]}\n'
                                                      f'\tСумма за підписку на канал: {message.text}',
                           reply_markup=admin_menu())
    await state.finish()


# @dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Перелік завдань')
# async def task_list(message: Message, state: FSMContext):
#     all_tasks = await get_all_tasks()
#     for task in all_tasks:

