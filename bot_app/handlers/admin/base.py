import re

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType

from bot_app.db.admin import set_task_db, get_all_tasks, get_all_new_tasks, change_amin_task, delete_task
from bot_app.db.users import get_all
from bot_app.markups.admin.base import cancel, admin_menu, task_keyboard, another_tasks
from bot_app.markups.base import new_task_for_user_ikb
from bot_app.misc import bot, dp, _, _l
from bot_app import config
from bot_app.misc import bot, dp
from bot_app.states.admin import Admin


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), commands=['admin'], state='*',
                    chat_type=ChatType.PRIVATE)
async def process_start(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Вітаю в адмін меню',
                           reply_markup=admin_menu())
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Відмінити', state='*',
                    chat_type=ChatType.PRIVATE)
async def cancel_add(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, text='Ви повернулись на головне меню', reply_markup=admin_menu())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Перелік завдань',
                    chat_type=ChatType.PRIVATE)
async def task_list(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Виберіть які саме завдання', reply_markup=task_keyboard())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Початкові завдання',
                    chat_type=ChatType.PRIVATE)
async def main_tasks_list(message: Message, state: FSMContext):
    all_tasks = await get_all_tasks()
    list_of_orders = [', '.join(str(value) for key, value in one_task.items()) for one_task in all_tasks]
    new_list = []
    for task in list_of_orders:
        new_list.append(task)

    tasks_text = '\n\n'.join(new_list)
    if tasks_text:
        await bot.send_message(message.from_user.id,
                               text='Всі завдання:\n\n{}\n\n Щоб змінити натисніть напишіть назву'.format(tasks_text),
                               reply_markup=cancel())
        await state.set_state(Admin.Edit_task.name_to_edit)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Edit_task.name_to_edit,
                    chat_type=ChatType.PRIVATE)
async def name_to_edit(message: Message, state: FSMContext):
    await state.update_data({'name_to_edit': message.text})
    await bot.send_message(message.from_user.id, text='Напишіть нижче на що хочете змінити назву(кнопки):',
                           reply_markup=cancel())
    await state.set_state(Admin.Edit_task.name)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Edit_task.name,
                    chat_type=ChatType.PRIVATE)
async def new_name_to_task(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await bot.send_message(message.from_user.id, text='Відправте нову силку:')
    await state.set_state(Admin.Edit_task.new_url)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Edit_task.new_url,
                    chat_type=ChatType.PRIVATE)
async def url_new_task(message: Message, state: FSMContext):
    regexp = re.compile(
        r'(?:http[s]?:\/\/.)?[-a-zA-Z0-9@%._\+~#=]{1,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)')
    matches = re.findall(regexp, message.text)
    if not matches:
        await bot.send_message(message.from_user.id,
                               text='Не правильно написана силка, ось вам приклад, спробуйте знову:\n'
                                    'https://t.me/referal3_bot', )

        return

    await state.update_data({'url': message.text})
    edited_task = await state.get_data()
    await change_amin_task(edited_task)
    await bot.send_message(message.from_user.id, text='Змінено', reply_markup=admin_menu())
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Додаткові завдання',
                    chat_type=ChatType.PRIVATE)
async def main_tasks_list(message: Message, state: FSMContext):
    all_tasks = await get_all_new_tasks()

    tasks_text = ''
    for one_task in all_tasks:
        task_items = []
        for key, value in one_task.items():
            if key != 'first_key':
                task_items.append(str(value))
        task_text = ', '.join(task_items)
        tasks_text += f'{task_text}\n\n'

    if tasks_text:
        await bot.send_message(message.from_user.id,
                               text='Всі додаткові завдання:\n\n{}'.format(tasks_text),
                               reply_markup=another_tasks())


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Додати завдання',
                    chat_type=ChatType.PRIVATE)
async def add_name_task(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Напишіть назву каналу', reply_markup=cancel())
    await state.set_state(Admin.Task.name_task)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.name_task,
                    chat_type=ChatType.PRIVATE)
async def add_url_task(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await bot.send_message(message.from_user.id, text='Додайте силку на канал', reply_markup=cancel())
    await state.set_state(Admin.Task.url_task)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.url_task,
                    chat_type=ChatType.PRIVATE)
async def wrong_url(message: Message, state: FSMContext):
    regexp = re.compile(
        r'(?:http[s]?:\/\/.)?[-a-zA-Z0-9@%._\+~#=]{1,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)')
    matches = re.findall(regexp, message.text)

    if not matches:
        await bot.send_message(message.from_user.id,
                               text='Не правильно написана силка, ось вам приклад, спробуйте знову:\n'
                                    'https://t.me/referal3_bot', )

        return

    await state.update_data({'url': message.text})
    await bot.send_message(message.from_user.id, text='Додайте сумму за це завдання', reply_markup=cancel())
    await state.set_state(Admin.Task.payment)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), state=Admin.Task.payment,
                    chat_type=ChatType.PRIVATE)
async def add_to_db(message: Message, state: FSMContext):
    info = await state.get_data()
    await state.update_data({'payment': message.text})
    await set_task_db(state.get_data())
    await bot.send_message(message.from_user.id, text='Ви додали нове завдання:\n'
                                                      f'\tНазва завдання(кнопки)\n{info["name"]}\n'
                                                      f'\tПосилання на сайт або канал\n{info["url"]}\n'
                                                      f'\tСумма за підписку на канал: {message.text}',
                           reply_markup=admin_menu())
    user_list = await get_all()
    try:
        for users in user_list:
            await bot.send_message(chat_id=users['user_id'], text='Нове завдання',
                                   reply_markup=await new_task_for_user_ikb(info))
    except Exception as e:
        print(e)
    await state.finish()


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Прибрати завдання',
                    chat_type=ChatType.PRIVATE)
async def delete_some_task(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Напишіть назву каналу, щоб його прибрати', reply_markup=cancel())
    await state.set_state(Admin.Task.name_to_delete)


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), chat_type=ChatType.PRIVATE,
                    state=Admin.Task.name_to_delete)
async def name_task_to_delete(message: Message, state: FSMContext):
    try:
        await delete_task(message.text)
        await bot.send_message(message.from_user.id, text=f'Ви видалили {message.text}', reply_markup=admin_menu())
        await state.finish()
    except Exception as e:
        print(e)
        await bot.send_message(message.from_user.id, text='Не вдалося, спрбуйте знову', reply_markup=cancel())
        await state.set_state(Admin.Task.name_to_delete)
