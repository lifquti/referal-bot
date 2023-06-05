from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    main = State()

    class Task(StatesGroup):
        url_task = State()
        name_task = State()
        status = State()
        payment = State()

    class MassSend(StatesGroup):
        to_all_message = State()
