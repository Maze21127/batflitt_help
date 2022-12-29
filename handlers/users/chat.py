import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.help import get_close_chat_keyboard, get_score_keyboard, GET_CUSTOMER_KEYBOARD
from logger import logger
from loader import bot, dp, languages, stats
from settings import HELP_CHAT_ID, USER_CHATS
from states.chat import Chat
from utils.messages import get_message, ANSWER_MESSAGE


def calculate_statistic(data: list):
    stats_dict = {i: 0 for i in range(6)}
    for score in data:
        stats_dict[score[0]] += 1
    return stats_dict


def average_score(data: dict):
    positive_stats = tuple(filter(lambda key: data[key] != 0, data))
    return sum(positive_stats) / len(positive_stats)


@dp.message_handler(state=Chat.in_chat)
async def in_chat_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    support_chat_id = HELP_CHAT_ID if not data.get('support_id') else data.get('support_id')
    print(support_chat_id)
    keyboard = GET_CUSTOMER_KEYBOARD if support_chat_id == HELP_CHAT_ID else None
    language = languages.get_user_language(message.from_user.id)
    new_message = f"""
*User ID*: {message.from_user.id}
*Message*: {message.text}
*Message ID*: {message.message_id}
*Язык пользователя: {language}*
"""
    await state.update_data(message=True)
    await bot.send_message(support_chat_id, new_message, parse_mode="Markdown",
                           reply_markup=keyboard)
    if keyboard is None:
        await bot.send_message(support_chat_id, ANSWER_MESSAGE)


@dp.channel_post_handler(lambda message: message.text == '/now')
async def get_stats(message: types.Message):
    data = stats.get_scores(message.chat.id)
    total = len(data)
    answer = f"*Обработано заявок:* {total}\n"
    statistic = calculate_statistic(data)
    answer += "*Оценки:*\n"
    for key, value in statistic.items():
        if key == 0:
            continue
        answer += f"{key} - {value}\n"
    answer += f"*Заявок без оценок:* {statistic[0]}\n"
    answer += f"*Средний рейтинг:* {average_score(statistic)}"
    return await message.answer(answer, parse_mode="Markdown")


@dp.channel_post_handler()
async def dialog_message(message: types.Message):
    if message.sender_chat.id in USER_CHATS.keys() or message.reply_to_message is None:
        return
    try:
        ids = re.findall(r'\d+', message.reply_to_message.text)
        state = dp.current_state(chat=ids[0], user=ids[0])
        if await state.get_state() is None:
            return
        language = languages.get_user_language(ids[0])
        return await bot.send_message(ids[0], message.text, reply_to_message_id=ids[-1],
                                      reply_markup=get_close_chat_keyboard(language))
    except IndexError:
        return


@dp.callback_query_handler(lambda cb: cb.data == 'get_request')
async def get_request(callback_query: types.CallbackQuery):
    try:
        redirect_chat = USER_CHATS[callback_query.from_user.id]
    except KeyError:
        return
    ids = re.findall(r'\d+', callback_query.message.text)
    user_id = ids[0]
    await callback_query.message.copy_to(redirect_chat)
    await callback_query.message.answer(f'{callback_query.from_user.id} ({callback_query.from_user.first_name}) '
                                        f'взял заявку в обработку')
    await bot.send_message(redirect_chat, ANSWER_MESSAGE)
    await callback_query.message.edit_reply_markup(reply_markup=None)
    state = dp.current_state(chat=user_id,
                             user=user_id)
    return await state.update_data(support_id=redirect_chat)
    # return await bot.send_message(redirect_chat, callback_query.message.text, parse_mode="Markdown")


@dp.callback_query_handler(lambda cb: cb.data == 'close_chat', state=Chat.in_chat)
async def close_chat_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message = data.get("message")
    support_chat_id = data.get('support_id')
    language = languages.get_user_language(callback_query.from_user.id)
    if message is None:
        await bot.send_message(callback_query.from_user.id, get_message(language, 'close_chat_no_message'))
    else:
        await bot.send_message(callback_query.from_user.id, get_message(language, 'close_chat'),
                               reply_markup=get_score_keyboard(language))
        await Chat.score.set()
        await bot.send_message(support_chat_id, f"Пользователь {callback_query.from_user.id} вышел из режима чата")
    return await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@dp.callback_query_handler(state=Chat.score)
async def score_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    support_chat_id = data.get('support_id')
    user_id = callback_query.from_user.id
    score = callback_query.data[6]
    if score == "Score:0":
        await state.finish()
        return await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    else:
        message = f"Пользователь {user_id} поставил оценку вашей работе: " \
                  f"{score}."
        await state.finish()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(support_chat_id, message, parse_mode="Markdown")

    stats.add_score(user_id, support_chat_id, score)
