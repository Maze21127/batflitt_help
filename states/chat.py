from aiogram.dispatcher.filters.state import StatesGroup, State


class Chat(StatesGroup):
    in_chat = State()
    score = State()
