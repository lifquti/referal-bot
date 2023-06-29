import datetime
import json
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType, ChatMemberStatus, ChatJoinRequest, ChatMember

import bot_app
from bot_app import markups, misc, db, config
from bot_app.db.admin import get_all_tasks
from bot_app.db.users import get_user, create_user, check_start_task, add_balance, get_referal, get_time_registration, \
    edit_do_or_not, check_do_or_not, get_balance, tasks_info, get_all_new_task, looking_for_link, \
    check_payment_for_user, add_balance_from_task, check_task_in_task_db, complete_task, tasks_information
from bot_app.markups.base import links_ikb, channel_ikb, new_tasks_ikb
from bot_app.markups.user.main import user_main_menu, balance_menu
from bot_app.misc import bot, dp, _, _l
from bot_app.misc import scheduler as async_scheduler


async def schedule_message(user_id):
    url_list = await check_start_task()
    subscribed_all = True
    try:
        for url in url_list:
            name_channel = url['url'].split('/')[-1]
            member = await bot.get_chat_member(chat_id='@' + name_channel, user_id=id)
            if member.status.lower() == 'left':
                subscribed_all = False
            else:
                raise Exception("Some error")
    except Exception as e:
        await send_message_to_user(user_id)


async def send_message_to_user(user_id):
    await bot.send_message(user_id, 'Ви не пройшли всі базові завдання, якщо ви їх виконаєте отримаєте 5 гривень')


async def check_group(id):
    checker = await check_do_or_not(id)
    if checker['do_or_not'] == 1:
        await bot.send_message(id, text='Ви виконали всі початкові завдання', reply_markup=user_main_menu())
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
            if id_referal['refer_from'] is not None:
                await add_balance(id_referal['refer_from'])
                await bot.send_message(id_referal['refer_from'], text='По реферальній силці юзер пройшов завдання і ви отримуєте'
                                                                      'разом із ним 5 гривень')
            await bot.send_message(id,
                                   text='Ви підписані на всі базові канали и отримали 5 гривень на баланс, '
                                        'а також ваш реферал, якщо він є', reply_markup=user_main_menu())


@dp.message_handler(commands='start', state='*', chat_type=ChatType.PRIVATE)
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    user_check = await get_user(message.from_user.id)
    ref = message.get_args()
    if user_check is not None:
        await bot.send_message(message.from_user.id, text='Ви вже є нашим учаснимом')
        await check_group(message.from_user.id)
        return

    await create_user(message.from_user)
    all_tasks = await get_all_tasks()
    await bot.send_message(message.from_user.id, text='Тримай ссилки на канали',
                           reply_markup=links_ikb(all_tasks, message.from_user.id))
    time_to_send = datetime.datetime.now() + datetime.timedelta(days=1)

    async_scheduler.add_job(schedule_message, trigger='date', run_date=time_to_send, args=(message.from_user.id,))
    try:
        await db.users.add_refferal(ref[3:], message.from_user.id)
        await bot.send_message(ref[3:], text='У вас новий рефераал')
    except Exception as e:
        print(e)


@dp.chat_member_handler()
async def user_joined_chat(update: types.ChatMemberUpdated):
    if update.new_chat_member.status == 'member' and update.old_chat_member.status == 'left':
        try:
            link_task = await update.invite_link.invite_link
        except:
            get_chat_username = update.chat.username
            link_task = 'https://t.me/' + get_chat_username
    else:
        return

    had_a_task_payment = await check_task_in_task_db(link_task)
    print(had_a_task_payment)
    do_task = await tasks_information(update.from_user.id, link_task)
    if had_a_task_payment is None or do_task is not None:
        return

    await add_balance_from_task(had_a_task_payment['payment'], update.from_user.id)
    await complete_task(update.from_user.id, link_task)
    await bot.send_message(update.from_user.id, text=f'Ви отрамли на баланс {had_a_task_payment["payment"]}')


@dp.message_handler(text='Перевірити підписки', chat_type=ChatType.PRIVATE)
async def checker(message: Message):
    checker = await check_do_or_not(message.from_user.id)
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


@dp.callback_query_handler(text='do_all_tasks', chat_type=ChatType.PRIVATE)
async def check(call: CallbackQuery):
    await call.answer()
    await check_group(call.from_user.id)


@dp.message_handler(text='Реферальна програма', chat_type=ChatType.PRIVATE)
async def get_my_referal_link(message: Message):
    await bot.send_message(message.from_user.id, text=f'https://t.me/referal3_bot?start=ref{message.from_user.id}')


@dp.message_handler(text='Баланс', chat_type=ChatType.PRIVATE)
async def balance(message: Message):
    check_balance = await get_balance(message.from_user.id)
    await bot.send_message(message.from_user.id, text=f"На вашому балансі зараз: {check_balance['balance']}",
                           reply_markup=balance_menu())


@dp.message_handler(text='Головне меню', chat_type=ChatType.PRIVATE)
async def user_main(message: Message):
    await bot.send_message(message.from_user.id, text='Ви повернулись до головного меню', reply_markup=user_main_menu())


@dp.message_handler(text='Нові завдання')
async def new_task_for_user(message: Message):
    task_which_user_did = await tasks_info(message.from_user.id)
    all_task = await get_all_new_task()
    new_links = []
    for task in all_task:
        found = False
        for task_user in task_which_user_did:
            if task['url'] == task_user['url']:
                found = True
                break
        if not found:
            new_links.append(task['url'])

    if new_links:
        await bot.send_message(message.from_user.id,
                               text='Нижче представлені нові завдання',
                               reply_markup=await new_tasks_ikb(new_links))
    else:
        await bot.send_message(message.from_user.id,
                               text="Зараз немає нових завдань, ви отримаєте сповіщення коли воно з'явиться")


@dp.callback_query_handler(text='cancel', chat_type=ChatType.PRIVATE)
async def cancel(call: CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text='Ви повернулись на головне меню', reply_markup=user_main_menu())
