from aiogram.dispatcher.filters.state import StatesGroup, State

class Admin(StatesGroup):
    ID = State()
    Time = State()
    Time_id = State()
    Add_service = State()
    Delete_service = State()
    For_all = State()
    Delete_balance = State()
    Phone_find = State()
    Block = State()