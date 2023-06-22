from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    main = State()

    class Task(StatesGroup):
        name_task = State()
        url_task = State()
        status = State()
        payment = State()
        delete = State()
        name_to_delete = State()

    class Edit_task(StatesGroup):
        name_to_edit = State()
        name = State()
        new_url = State()

    class MassSend(StatesGroup):
        Users = State()
        message_text = State()
        add_photo = State()
        to_all_message = State()
        message_to_send = State()
        message_markup = State()
