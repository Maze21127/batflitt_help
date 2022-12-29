from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from keyboards.inline.help import SEND_PHONE_KEYBOARD


def get_send_phone_keyboard(language: str):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    language = language if language in SEND_PHONE_KEYBOARD['cancel'].keys() else "en"

    keyboard.add(KeyboardButton(SEND_PHONE_KEYBOARD['phone_number'][language], request_contact=True))
    keyboard.add(KeyboardButton(SEND_PHONE_KEYBOARD['cancel'][language]))
    return keyboard
