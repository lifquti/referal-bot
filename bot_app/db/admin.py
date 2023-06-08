from aiogram.types import User
from bot_app.db.base import create_dict_con


async def set_task_db(data):
    con, cur = await create_dict_con()
    info = await data
    await cur.execute('insert ignore into task_list_db (name, url, status, payment, group_id) '
                      'values (%s, %s, %s, %s, %s)',
                      (info['name'], info['url'], info['status'], info['payment'], info['group_id']))
    await con.commit()
    await con.ensure_closed()


async def get_all_tasks():
    con, cur = await create_dict_con()
    await cur.execute('select * from start_task')
    all_tasks = await cur.fetchall()
    await con.ensure_closed()
    return all_tasks


async def get_all_new_tasks():
    con, cur = await create_dict_con()
    await cur.execute('select * from task_list_db')
    all_tasks = await cur.fetchall()
    await con.ensure_closed()
    return all_tasks


async def change_amin_task(new_values):
    con, cur = await create_dict_con()
    await cur.execute('update start_task set name_task, url = %s, %s where name_task = %s',
                      (new_values['name'], new_values['url'], new_values['name_to_edit']))
    await con.commit()
    await con.ensure_closed()

