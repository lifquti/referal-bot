import aiogram
from aiogram.types import Message, ChatType

from bot_app import config
from bot_app.misc import bot, dp


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), chat_type=ChatType.PRIVATE)
async def echo(message: Message):
    await bot.send_message(message.from_user.id, 'Будь ласка натисніть /admin')
