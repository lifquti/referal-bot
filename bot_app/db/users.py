import datetime

from aiogram.types import User
from bot_app.db.base import create_dict_con


async def create_user(user: User):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into data_tg_user (user_id, `name`, user_name, balance, time_registration) '
                      'values (%s, %s, %s, %s, %s)',
                      (user.id, user.first_name, user.username, 0, datetime.datetime.now()))
    await con.commit()
    await cur.execute('select * from data_tg_user where user_id = %s ', (user.id,))
    user_data = await cur.fetchone()
    await con.ensure_closed()
    return user_data


async def get_user(user_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from data_tg_user where user_id = %s ', (user_id,))
    user_data = await cur.fetchone()
    await con.ensure_closed()
    if user_data is None:
        return None
    return user_data


async def add_refferal(from_user_id, for_user_id):
    con, cur = await create_dict_con()
    await cur.execute('UPDATE data_tg_user SET refer_from = %s WHERE user_id = %s', (from_user_id, for_user_id))
    await con.commit()
    await con.ensure_closed()


async def get_all():
    con, cur = await create_dict_con()
    await cur.execute('select * from data_tg_user ')
    users = await cur.fetchall()
    await con.ensure_closed()
    return users


async def update_locale(user_id: int, new_locale_code: str):
    con, cur = await create_dict_con()
    await cur.execute('update data_tg_user set `language` = %s where user_id = %s ', (new_locale_code, user_id,))
    await con.commit()
    await con.ensure_closed()


async def check_start_task():
    con, cur = await create_dict_con()
    await cur.execute('select url from start_task')
    urls_list = await cur.fetchall()
    await con.ensure_closed()
    return urls_list


async def add_balance(id):
    con, cur = await create_dict_con()
    await cur.execute('UPDATE data_tg_user SET balance = balance + 5 WHERE user_id = %s', (id, ))
    await con.commit()
    await con.ensure_closed()


async def get_referal(id):
    con, cur = await create_dict_con()
    await cur.execute('select refer_from from data_tg_user where user_id = %S', (id, ))
    refer_id = await cur.fetchone()
    await con.ensure_closed()
    return refer_id




