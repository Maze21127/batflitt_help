from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.help import KEYBOARD, get_close_chat_keyboard, get_is_helpful_keyboard, \
    IS_HELPFUL_KEYBOARD, get_cancel_keyboard, CANCEL_KEYBOARD, SEND_PHONE_KEYBOARD, get_start_keyboard
from keyboards.reply import get_send_phone_keyboard
from loader import dp, bot, languages
from settings import HELP_CHAT_ID
from states.chat import Chat
from states.trouble import IsHelpful, Trouble, Contacts, AppContacts
from utils.messages import MESSAGES, troubles, get_message


@dp.callback_query_handler(lambda cb: cb.data in KEYBOARD.keys(), state="*")
async def callback_query_handler(callback_query: types.CallbackQuery):
    state = dp.current_state()
    await state.finish()
    language = languages.get_user_language(callback_query.from_user.id)

    if callback_query.data in ('back', 'other'):
        await Chat.in_chat.set()
        return await bot.send_message(callback_query.from_user.id, get_message(language, 'chat'),
                                      reply_markup=get_close_chat_keyboard(language))

    new_state = troubles[callback_query.data]
    await new_state.set()

    if callback_query.data == 'cooperation':
        return await bot.send_message(callback_query.from_user.id, get_message(language, callback_query.data),
                                      reply_markup=get_send_phone_keyboard(language))

    if callback_query.data == 'debited_money':
        return await bot.send_message(callback_query.from_user.id, get_message(language, 'is_returned'),
                                      reply_markup=get_is_helpful_keyboard(language))

    await bot.send_message(callback_query.from_user.id, get_message(language, callback_query.data),
                           reply_markup=types.ReplyKeyboardRemove())
    return await bot.send_message(callback_query.from_user.id, get_message(language, 'is_helpful'),
                                  reply_markup=get_is_helpful_keyboard(language))


@dp.callback_query_handler(lambda cb: cb.data in IS_HELPFUL_KEYBOARD.keys(), state=Trouble)
async def callback_query_handler(callback_query: types.CallbackQuery):
    state = dp.current_state()
    state_name = await state.get_state()
    language = languages.get_user_language(callback_query.from_user.id)

    if callback_query.data == 'yes':
        if state_name == 'Trouble:debited_money':
            await state.finish()
            await AppContacts.waiting_number.set()
            return await bot.send_message(callback_query.from_user.id, get_message(language, 'debited_money'),
                                          reply_markup=get_send_phone_keyboard(language))

        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(callback_query.from_user.id, get_message(language, 'help_success'))

    if state_name in ('Trouble:changeback', 'Trouble:wire', 'Trouble:other', 'Trouble:cooperation'):
        await state.finish()
        await Chat.in_chat.set()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(callback_query.from_user.id, get_message(language, 'chat'),
                                      reply_markup=get_close_chat_keyboard(language))

    if callback_query.data == 'no':
        await IsHelpful.first.set()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if state_name == 'Trouble:debited_money':
            await bot.send_message(callback_query.from_user.id, get_message(language, 'need_return'),
                                   reply_markup=None)
        else:
            await bot.send_message(callback_query.from_user.id, get_message(language, 'back'),
                                   reply_markup=None)
        return await bot.send_message(callback_query.from_user.id, get_message(language, 'is_helpful'),
                                      reply_markup=get_is_helpful_keyboard(language))


@dp.callback_query_handler(state=IsHelpful.first)
async def after_back(callback_query: types.CallbackQuery, state: FSMContext):
    language = languages.get_user_language(callback_query.from_user.id)
    if callback_query.data == 'no':
        await Chat.in_chat.set()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(callback_query.from_user.id, get_message(language, 'chat'),
                                      reply_markup=get_close_chat_keyboard(language))

    await state.finish()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    return await bot.send_message(callback_query.from_user.id, get_message(language, 'help_success'))


@dp.message_handler(content_types=types.ContentType.TEXT, state="*")
async def cancel_contacts(message: types.Message, state: FSMContext):
    language = languages.get_user_language(message['from']['id'])
    if message.text in CANCEL_KEYBOARD.values():
        await state.finish()
        await bot.send_message(message.from_user.id, get_message(language, 'change_mind'),
                               reply_markup=types.ReplyKeyboardRemove())
        await message.answer(get_message(language, "start2"),
                             reply_markup=get_start_keyboard(language))


@dp.message_handler(content_types=[types.ContentType.CONTACT, types.ContentType.TEXT],
                    state=[Trouble.cooperation, AppContacts.waiting_number])
async def contacts(msg: types.Message, state: FSMContext):
    language = languages.get_user_language(msg['from']['id'])
    try:
        number = msg.contact.phone_number
    except AttributeError:
        number = msg.text

    state_name = await state.get_state()

    await msg.answer(f"{get_message(language, 'success_number')}: {number}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    if state_name == 'AppContacts:waiting_number':
        await msg.answer(get_message(language, 'waiting_number'), reply_markup=get_cancel_keyboard(language))
        await AppContacts.waiting_date.set()

    elif state_name == 'Trouble:cooperation':
        await msg.answer(get_message(language, 'waiting_email'),
                         reply_markup=get_cancel_keyboard(language))
        await Contacts.waiting_email.set()

    return await state.update_data(number=number)


@dp.message_handler(state=Contacts.waiting_email)
async def email(message: types.Message, state: FSMContext):
    language = languages.get_user_language(message['from']['id'])

    data = await state.get_data()
    number = data.get("number")

    new_message = f"""
Пользователь хочет сотрудничать.
*User ID*: {message.from_user.id}
*Email*: {message.text}
*Номер телефона*: {number}
*Язык пользователя: {language}*
"""
    await state.finish()
    await message.answer(get_message(language, "request_sent"))
    await bot.delete_message(message.from_user.id, message.message_id - 1)
    return await bot.send_message(HELP_CHAT_ID, new_message, parse_mode="Markdown")


@dp.message_handler(state=AppContacts.waiting_date)
async def waiting_date_handler(message: types.Message, state: FSMContext):
    language = languages.get_user_language(message['from']['id'])
    data = await state.get_data()
    number = data.get("number")

    new_message = f"""
Списались деньги за потерю.
*User ID*: {message.from_user.id}
*Дата транзакции*: {message.text}
*Номер телефона*: {number}
*Message ID*: {message.message_id}
*Язык пользователя: {language}*
"""
    await state.finish()
    await message.answer(get_message(language, "request_sent"))
    await bot.delete_message(message.from_user.id, message.message_id - 1)
    return await bot.send_message(HELP_CHAT_ID, new_message, parse_mode="Markdown")


@dp.callback_query_handler(state=[Contacts.waiting_email, AppContacts.waiting_date])
async def after_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await state.finish()
    language = languages.get_user_language(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, get_message(language, 'change_mind'),
                           reply_markup=types.ReplyKeyboardRemove())
    await callback_query.message.answer(get_message(language, "start2"),
                                        reply_markup=get_start_keyboard(language))

# @dp.message_handler(lambda message: message.text in SEND_PHONE_KEYBOARD['cancel'].items())
# def cancel(message: types.Message):
#     state = dp.current_state()
#     await state.finish()
