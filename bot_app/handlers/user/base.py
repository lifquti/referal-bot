from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ChatType
from bot_app import markups, misc, db, config
from bot_app.db.admin import get_all_tasks
from bot_app.db.users import get_user, create_user
from bot_app.markups.base import links_ikb
from bot_app.misc import bot, dp, _, _l


@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    await state.finish()
    user_check = await get_user(message.from_user.id)
    ref = message.get_args()
    if user_check is not None:
        await bot.send_message(message.from_user.id, text='Ви вже є нашим учаснимом')
    else:
        user_data = await get_user(message.from_user.id)
        await create_user(message.from_user)
        all_tasks = await get_all_tasks()
        await bot.send_message(message.from_user.id, text='Тримай ссилки на канали',
                               reply_markup=links_ikb(all_tasks, message.from_user.id))
        await db.users.add_refferal(ref[3:], message.from_user.id)





#
# @dp.callback_query_handler(CallbackQuery)
# async def check_connection(call: CallbackQuery):
#     await bot.send_message(text='Проверить подписки на каналы', reply_markup=check_if_exist())
#
#
# @dp.message_handler(text='Перевірити підписки')
# async def checker(message: Message):
#     for channel in channels_id:
#         try:
#             result = bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
#             if result.status == 'left':
#                 await bot.send_message(message.from_user.id, text=f'Ви не підписані на канал @{channel}')
#                 break
#             else:
