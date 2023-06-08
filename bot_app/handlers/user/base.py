import time

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType, ChatMemberStatus
from bot_app import markups, misc, db, config
from bot_app.db.admin import get_all_tasks
from bot_app.db.users import get_user, create_user, check_start_task, add_balance, get_referal, get_time_registration, \
    edit_do_or_not, check_do_or_not
from bot_app.markups.base import links_ikb, channel_ikb
from bot_app.misc import bot, dp, _, _l
import schedule
import asyncio


async def job_that_executes_once(id, time):
    async def send_initial_message():
        await bot.send_message(id, text='Ви не пройшли початкові завдання')
        schedule.cancel_job(job)
    time_str = time.strftime("%H:%M")
    job = schedule.every().minute.at(time_str).do(asyncio.run, send_initial_message())

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def schedule_message(id):
    url_list = await check_start_task()
    time_registration = await get_time_registration(id)
    subscribed_all = True

    try:
        for url in url_list:
            name_channel = url['url'].split('/')[-1]
            member = await bot.get_chat_member(chat_id='@' + name_channel, user_id=id)
            if member.status.lower() == 'left':
                subscribed_all = False
            else:
                raise Exception("Some error occurred")
    except Exception as e:
        await job_that_executes_once(id, time_registration['time_registration'])


async def check_group(id):
    checker = await check_do_or_not(id)
    if checker['do_or_not'] == 1:
        await bot.send_message(id, text='Ви виконали всі початкові завдання')
    else:
        url_list = await check_start_task()
        subscribed_all = True
        for url in url_list:
            name_channel = url['url'].split('/')[-1]
            member = await bot.get_chat_member(chat_id='@' + name_channel, user_id=id)
            if member.status.lower() == 'LEFT'.lower():
                subscribed_all = False
                await bot.send_message(chat_id=id, text='Ви не підписані на всі канали',
                                       reply_markup=channel_ikb(name_channel))
                break

        if subscribed_all:
            await edit_do_or_not(id)
            await add_balance(id)
            id_referal = await get_referal(id)
            print(id_referal['refer_from'])
            if id_referal['refer_from'] is not None:
                await add_balance(id_referal['refer_from'])
            await bot.send_message(id,
                                   text='Ви підписані на всі базові канали и отримали 5 гривен на баланс, '
                                        'а також ваш реферал, якщо ві є')


@dp.message_handler(commands='start', state='*', chat_type=ChatType.PRIVATE)
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    user_check = await get_user(message.from_user.id)
    ref = message.get_args()
    if user_check is not None:
        await bot.send_message(message.from_user.id, text='Ви вже є нашим учаснимом')
        await check_group(message.from_user.id)
    else:
        user_data = await get_user(message.from_user.id)
        await create_user(message.from_user)
        all_tasks = await get_all_tasks()
        await bot.send_message(message.from_user.id, text='Тримай ссилки на канали',
                               reply_markup=links_ikb(all_tasks, message.from_user.id))
        await schedule_message(message.from_user.id)
        try:
            await db.users.add_refferal(ref[3:], message.from_user.id)
            await bot.send_message(ref[3:], text='У вас новий рефераал')
        except Exception as e:
            print(e)


@dp.message_handler(text='Перевірити підписки', chat_type=ChatType.PRIVATE)
async def checker(message: Message):
    checker = await check_do_or_not(id)
    if checker['do_or_not'] != 1:
        url_list = await check_start_task()
        subscribed_all = True
        for url in url_list:
            name_channel = url['url'].split('/')[-1]
            member = await bot.get_chat_member(chat_id='@' + name_channel, user_id=id)
            if member.status.lower() == 'LEFT'.lower():
                subscribed_all = False
                await bot.send_message(chat_id=id, text='Ви не підписані на всі канали',
                                       reply_markup=channel_ikb(name_channel))


@dp.message_handler(text='Моя реферальна ссилка', chat_type=ChatType.PRIVATE)
async def get_my_referal_link(message: Message):
    await bot.send_message(message.from_user.id, text=f'https://t.me/referal3_bot?start=ref{message.from_user.id}')

