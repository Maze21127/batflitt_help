from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


KEYBOARD = {
    "charge": {
        "ru": "Не заряжает",
        "en": "Not charging",
        "la": "Neuzlādē"
    },
    "back": {
        "ru": "Не могу вернуть устройство",
        "en": "Can't back Power Bank",
        "la": "Nevaru nodot atpakaļ ierīci"
    },
    "wire": {
        "ru": "Проблема с проводом",
        "en": "Wire issue",
        "la": "Vada problēma"
    },
    "changeback": {
        "ru": "Возврат средств",
        "en": "Money refund",
        "la": "Naudas atmaksa"
    },
    "debited_money": {
        "ru": "Списались деньги за потерю",
        "en": "Money written off for loss",
        "la": "Iekasēta nauda par nozaudēšanu"
    },
    "cooperation": {
        "ru": "Сотрудничество",
        "en": "Cooperation",
        "la": "Sadarbība"
    },
    "other": {
        "ru": "Другая проблема",
        "en": "Other issue",
        "la": "Cita problēma"
    }
}

IS_HELPFUL_KEYBOARD = {
    "yes": {
        "ru": "Да",
        "en": "Yes",
        "la": "Jā"
    },
    "no": {
        "ru": "Нет",
        "en": "No",
        "la": "Nē"
    }
}


CLOSE_CHAT_KEYBOARD = {
    "ru": "Выход из чата",
    "en": "Close chat",
    "la": "Aizvērt tērzēšanas režīmu"
}

SEND_PHONE_KEYBOARD = {
    "phone_number": {
        "ru": "Отправить номер телефона 📱",
        "en": "Send phone number 📱",
        "la": "Nosūtīt tālruņa numuru 📱"
    },
    "cancel": {
        "ru": "Отмена",
        "en": "Cancel",
        "la": "Atcelt"
    }
}

CANCEL_KEYBOARD = {
    "ru": "Отмена",
    "en": "Cancel",
    "la": "Atcelt"
}

DONT_SCORE_KEYBOARD = {
    "ru": "Не оценивать",
    "en": "Don't Score",
    "la": ""
}

LANGUAGES = {
    "ru": "Russian 🇷🇺",
    "en": "English 🇺🇸",
    "la": "Latvija 🇱🇻",
}

LANGUAGES_KEYBOARD = InlineKeyboardMarkup()
for key, value in LANGUAGES.items():
    LANGUAGES_KEYBOARD.add(InlineKeyboardButton(value, callback_data=key))


def get_start_keyboard(language: str):
    keyboard = InlineKeyboardMarkup()
    language = language if language in KEYBOARD['charge'].keys() else "en"
    for key, value in KEYBOARD.items():
        keyboard.add(InlineKeyboardButton(f"{value[language]}", callback_data=key))
    return keyboard


def get_is_helpful_keyboard(language: str):
    keyboard = InlineKeyboardMarkup()
    language = language if language in IS_HELPFUL_KEYBOARD['yes'].keys() else "en"
    for key, value in IS_HELPFUL_KEYBOARD.items():
        keyboard.add(InlineKeyboardButton(f"{value[language]}", callback_data=key))
    return keyboard


def get_close_chat_keyboard(language: str):
    keyboard = InlineKeyboardMarkup()
    language = language if language in CLOSE_CHAT_KEYBOARD.keys() else "en"
    keyboard.add(InlineKeyboardButton(CLOSE_CHAT_KEYBOARD[language], callback_data='close_chat'))
    return keyboard





def get_cancel_keyboard(language: str):
    keyboard = InlineKeyboardMarkup()
    language = language if language in CANCEL_KEYBOARD.keys() else "en"
    keyboard.add(InlineKeyboardButton(CANCEL_KEYBOARD[language], callback_data='cancel'))
    return keyboard


def get_score_keyboard(language: str):
    score_keyboard = InlineKeyboardMarkup()
    language = language if language in DONT_SCORE_KEYBOARD.keys() else "en"
    for i in range(1, 6):
        score_keyboard.add(InlineKeyboardButton(str(i), callback_data=f"Score:{i}"))
    score_keyboard.add(InlineKeyboardButton(DONT_SCORE_KEYBOARD[language], callback_data='Score:0'))

    return score_keyboard


GET_CUSTOMER_KEYBOARD = InlineKeyboardMarkup()
GET_CUSTOMER_KEYBOARD.add(InlineKeyboardButton("Взять в обработку", callback_data='get_request'))
