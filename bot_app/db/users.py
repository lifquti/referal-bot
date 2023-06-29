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


async def check_start_task():
    con, cur = await create_dict_con()
    await cur.execute('select url from start_task')
    urls_list = await cur.fetchall()
    await con.ensure_closed()
    return urls_list


async def get_all_new_task():
    con, cur = await create_dict_con()
    await cur.execute('select url from task_list_db where status_of_task = True')
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
    await cur.execute('select refer_from from data_tg_user where user_id = %s', (id, ))
    refer_id = await cur.fetchone()
    await con.ensure_closed()
    return refer_id


async def get_time_registration(id):
    con, cur = await create_dict_con()
    await cur.execute('select time_registration from data_tg_user where user_id = %s', (id, ))
    date = await cur.fetchone()
    await con.ensure_closed()
    return date


async def edit_do_or_not(id):
    con, cur = await create_dict_con()
    await cur.execute('update data_tg_user set do_or_not = 1 where user_id = %s', (id,))
    await con.commit()
    await con.ensure_closed()


async def check_do_or_not(id):
    con, cur = await create_dict_con()
    await cur.execute('select do_or_not from data_tg_user where user_id = %s', (id,))
    answer = await cur.fetchone()
    await con.ensure_closed()
    return answer


async def get_balance(id):
    con, cur = await create_dict_con()
    await cur.execute('select balance from data_tg_user where user_id = %s', (id,))
    balance = await cur.fetchone()
    await con.ensure_closed()
    return balance


async def tasks_info(id):
    con, cur = await create_dict_con()
    await cur.execute('select url from task_complete where user_id = %s', (id, ))
    task = await cur.fetchall()
    await con.ensure_closed()
    if task is None:
        return None
    else:
        return task


async def tasks_information(id, url):
    con, cur = await create_dict_con()
    await cur.execute('select * from task_complete where user_id = %s and url = %s', (id, url))
    task = await cur.fetchone()
    await con.ensure_closed()
    if task is None:
        return None
    else:
        return task


async def get_task_use_url(link):
    con, cur = await create_dict_con()
    await cur.execute('select name from task_list_db where url = %s', (link,))
    name_task = await cur.fetchone()
    await con.ensure_closed()
    return name_task


async def looking_for_link(link):
    con, cur = await create_dict_con()
    await cur.execute('select * from task_list_db where url = %s', (link,))
    tasks_information = await cur.fetchone()
    await con.ensure_closed()
    return tasks_information


async def check_payment_for_user(id, url):
    con, cur = await create_dict_con()
    await cur.execute('select * from task_complete where user_id, url = %s, %s', (id, url))
    info = await cur.fetchone()
    if info is None:
        await cur.execute('update task_complete set user_id, url = %s, %s', (id, url))
        await con.ensure_closed()
        return None
    else:
        await con.ensure_closed()
        return info


async def add_balance_from_task(summ, id):
    con, cur = await create_dict_con()
    await cur.execute('select balance from data_tg_user where user_id = %s', (id,))
    balance_before = await cur.fetchone()
    balance_new = int(balance_before['balance']) + summ
    await cur.execute('UPDATE data_tg_user SET balance =  %s WHERE user_id = %s', (balance_new, id))
    await con.commit()
    await con.ensure_closed()


async def check_task_in_task_db(url):
    con, cur = await create_dict_con()
    await cur.execute('select payment from task_list_db where url = %s', (url))
    cost = await cur.fetchone()
    if cost is None:
        await con.ensure_closed()
        return None
    else:
        await con.ensure_closed()
        return cost


async def complete_task(id, url):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into task_complete set user_id = %s, url = %s', (id, url))
    await con.commit()
    await con.ensure_closed()