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
