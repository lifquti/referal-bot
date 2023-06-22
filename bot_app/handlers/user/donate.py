import json

import requests
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import config
from bot_app.markups.base import donate_link_ikb
from bot_app.misc import dp, bot, routes
from bot_app.states.user import User


async def create_link_to_pay(summ):
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer $HIG#IRHRF#gn3ljpgHEIROF42IGHPOWJF',
        'Content-Type': 'application/json',
    }

    json_data = {
        'amount': summ,
        'currency': 'UAH',
        'callback_url': 'https://10fe-185-151-85-70.ngrok-free.app/aiogram2_bot_api/payment',
    }

    response = requests.post('https://prud-super-payment-api.telegram-crm.work/payment', headers=headers,
                             json=json_data)

    link = response.json()['payment_url']
    payment_id = response.json()["payment_id"]
    return link, payment_id


@dp.message_handler(text='Задонатити')
async def create_donate(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text='Введіть сумму донату')
    await state.set_state(User.Donate.summ)


@dp.message_handler(state=User.Donate.summ)
async def add_summ(message: Message, state: FSMContext):
    link_to_pay, payment_id = await create_link_to_pay(message.text)
    await bot.send_message(message.from_user.id,
                           text='Ось ваша силка на донат:',
                           reply_markup=await donate_link_ikb(link_to_pay))





















