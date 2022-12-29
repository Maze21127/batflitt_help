from aiogram import types

from keyboards.inline.help import get_start_keyboard, LANGUAGES_KEYBOARD, LANGUAGES
from loader import dp, languages, bot
from utils.messages import get_message


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()
    language = message['from']['language_code']
    languages.add_user(message['from']['id'], message['from']['language_code'])
    await message.answer(get_message(language, 'start'), reply_markup=LANGUAGES_KEYBOARD)
    # await message.answer(language, 'start2', reply_markup=get_start_keyboard(language))


@dp.message_handler(commands=['language'], state='*')
async def change_language(message: types.Message):
    state = dp.current_state()
    await state.finish()
    language = message['from']['language_code']
    return await message.answer(get_message(language, 'change_language'), reply_markup=LANGUAGES_KEYBOARD)


@dp.message_handler(commands=['help'], state='*')
async def menu(message: types.Message):
    state = dp.current_state()
    await state.finish()
    language = languages.get_user_language(message['from']['id'])
    return await message.answer(get_message(language, "start2"),
                                reply_markup=get_start_keyboard(language))


@dp.callback_query_handler(lambda cb: cb.data in LANGUAGES.keys(), state="*")
async def callback_query_handler(callback_query: types.CallbackQuery):
    language = languages.update_user(callback_query.from_user.id, callback_query.data)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    return await bot.send_message(callback_query.from_user.id, get_message(language, "start2"),
                                  reply_markup=get_start_keyboard(language))
