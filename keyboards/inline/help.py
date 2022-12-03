from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import callback_data

KEYBOARD = {
    "charge": "Не заряжает",
    "back": "Не могу вернуть устройство",
    "wire": "Проблема с проводом",
    "changeback": "Возврат средств",
    "debited_money": "Списались деньги за потерю",
    'cooperation': "Сотрудничество",
    "other": "Другая ошибка"
}

IS_HELPFUL_KEYBOARD = {
    'yes': "Да",
    'no': "Нет"
}

keyboard = InlineKeyboardMarkup()
for key, value in KEYBOARD.items():
    keyboard.add(InlineKeyboardButton(f"{value}", callback_data=key))

is_helpful_keyboard = InlineKeyboardMarkup()
for key, value in IS_HELPFUL_KEYBOARD.items():
    is_helpful_keyboard.add(InlineKeyboardButton(f"{value}", callback_data=key))


close_chat = InlineKeyboardMarkup()
close_chat.add(InlineKeyboardButton(f"Выход из чата", callback_data='close_chat'))


send_phone_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
send_phone_keyboard.add(KeyboardButton("Отправить номер телефона 📱", request_contact=True))
send_phone_keyboard.add(KeyboardButton("Отмена"))


cancel_keyboard = InlineKeyboardMarkup()
cancel_keyboard.add(InlineKeyboardButton(f"Отмена", callback_data='cancel'))

score_keyboard = InlineKeyboardMarkup()
for i in range(1, 6):
    score_keyboard.add(InlineKeyboardButton(str(i), callback_data=f"Score:{i}"))
score_keyboard.add(InlineKeyboardButton("Не оценивать", callback_data='Score:0'))