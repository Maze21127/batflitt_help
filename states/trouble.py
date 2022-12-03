from aiogram.dispatcher.filters.state import StatesGroup, State


class Contacts(StatesGroup):
    waiting_email = State()


class AppContacts(StatesGroup):
    waiting_number = State()
    waiting_date = State()


class IsHelpful(StatesGroup):
    first = State()
    second = State()


class Trouble(StatesGroup):
    charging = State()
    back = State()
    wire = State()
    changeback = State()
    debited_money = State()
    cooperation = State()
    other = State()

