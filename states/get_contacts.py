from aiogram.dispatcher.filters.state import StatesGroup, State

class GetContacts(StatesGroup):
    Phone = State()
    Name = State()