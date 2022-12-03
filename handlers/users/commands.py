from aiogram import types

from keyboards.inline.help import keyboard
from loader import dp
from utils.messages import MESSAGES


@dp.message_handler(commands=['start', 'help'], state='*')
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()

    await message.answer(MESSAGES['start'])
    await message.answer(MESSAGES['start2'], reply_markup=keyboard)

