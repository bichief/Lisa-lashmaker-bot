from aiogram.dispatcher.filters.state import StatesGroup, State

class Admin(StatesGroup):
    ID = State()
    Time = State()
    Time_id = State()