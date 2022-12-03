import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.help import close_chat, score_keyboard
from logger import logger
from loader import bot, dp
from settings import HELP_CHAT_ID
from states.chat import Chat
from utils.messages import MESSAGES


@dp.message_handler(state=Chat.in_chat)
async def in_chat_handler(message: types.Message, state: FSMContext):
    new_message = f"""
*User ID*: {message.from_user.id}
*Message*: {message.text}
*Message ID*: {message.message_id}
Что бы ответить пользователю, нажмите "Ответить" на ЭТО сообщение, иначе пользователь не получит ответ.
    """
    await state.update_data(message=True)
    return await bot.send_message(HELP_CHAT_ID, new_message, parse_mode="Markdown")


@dp.channel_post_handler()
async def dialog_message(message: types.Message):
    if message.sender_chat.id != HELP_CHAT_ID or message.reply_to_message is None:
        return

    ids = re.findall(r'\d+', message.reply_to_message.text)
    return await bot.send_message(ids[0], message.text, reply_to_message_id=ids[-1], reply_markup=close_chat)


@dp.callback_query_handler(lambda cb: cb.data == 'close_chat', state=Chat.in_chat)
async def close_chat_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("message")
    if message is None:
        await bot.send_message(callback_query.from_user.id, MESSAGES['close_chat_no_message'])
    else:
        await bot.send_message(callback_query.from_user.id, MESSAGES['close_chat'],
                               reply_markup=score_keyboard)
        await Chat.score.set()
        await bot.send_message(HELP_CHAT_ID, f"Пользователь {callback_query.from_user.id} вышел из режима чата")
    return await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(state=Chat.score)
async def score_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Score:0":
        await state.finish()
        return await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    else:
        message = f"Пользователь {callback_query.from_user.id} поставил оценку вашей работе: " \
                  f"{callback_query.data[6]}."
        await state.finish()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(HELP_CHAT_ID, message, parse_mode="Markdown")
