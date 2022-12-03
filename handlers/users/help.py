from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.help import KEYBOARD, is_helpful_keyboard, IS_HELPFUL_KEYBOARD, close_chat, send_phone_keyboard, \
    cancel_keyboard
from loader import dp, bot
from settings import HELP_CHAT_ID
from states.chat import Chat
from states.trouble import IsHelpful, Trouble, Contacts, AppContacts
from utils.messages import MESSAGES, troubles


@dp.callback_query_handler(lambda cb: cb.data in KEYBOARD.keys(), state="*")
async def callback_query_handler(callback_query: types.CallbackQuery):
    state = dp.current_state()
    await state.finish()

    if callback_query.data in ('back', 'other'):
        await Chat.in_chat.set()
        return await bot.send_message(callback_query.from_user.id, MESSAGES['chat'], reply_markup=close_chat)

    new_state = troubles[callback_query.data]
    await new_state.set()

    if callback_query.data == 'cooperation':
        return await bot.send_message(callback_query.from_user.id, MESSAGES[callback_query.data],
                                      reply_markup=send_phone_keyboard)

    if callback_query.data == 'debited_money':
        return await bot.send_message(callback_query.from_user.id, MESSAGES['is_returned'],
                                      reply_markup=is_helpful_keyboard)

    await bot.send_message(callback_query.from_user.id, MESSAGES[callback_query.data])
    return await bot.send_message(callback_query.from_user.id, MESSAGES['is_helpful'], reply_markup=is_helpful_keyboard)


@dp.callback_query_handler(lambda cb: cb.data in IS_HELPFUL_KEYBOARD.keys(), state=Trouble)
async def callback_query_handler(callback_query: types.CallbackQuery):
    state = dp.current_state()
    state_name = await state.get_state()
    if callback_query.data == 'yes':
        if state_name == 'Trouble:debited_money':
            await state.finish()
            await AppContacts.waiting_number.set()
            return await bot.send_message(callback_query.from_user.id, MESSAGES['debited_money'],
                                          reply_markup=send_phone_keyboard)

        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(callback_query.from_user.id, MESSAGES["help_success"])

    if state_name in ('Trouble:changeback', 'Trouble:wire', 'Trouble:other', 'Trouble:cooperation'):
        await state.finish()
        await Chat.in_chat.set()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(callback_query.from_user.id, MESSAGES['chat'], reply_markup=close_chat)

    if callback_query.data == 'no':
        await IsHelpful.first.set()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if state_name == 'Trouble:debited_money':
            await bot.send_message(callback_query.from_user.id, MESSAGES['need_return'])
        else:
            await bot.send_message(callback_query.from_user.id, MESSAGES['back'])
        return await bot.send_message(callback_query.from_user.id, MESSAGES['is_helpful'],
                                      reply_markup=is_helpful_keyboard)


@dp.callback_query_handler(state=IsHelpful.first)
async def after_back(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'no':
        await Chat.in_chat.set()
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        return await bot.send_message(callback_query.from_user.id, MESSAGES['chat'], reply_markup=close_chat)

    await state.finish()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    return await bot.send_message(callback_query.from_user.id, MESSAGES["help_success"])


@dp.message_handler(content_types=[types.ContentType.CONTACT, types.ContentType.TEXT], state=[Trouble.cooperation, AppContacts.waiting_number])
async def contacts(msg: types.Message, state: FSMContext):
    try:
        number = msg.contact.phone_number
    except AttributeError:
        number = msg.text

    state_name = await state.get_state()

    await msg.answer(f"Твой номер успешно получен: {number}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    if state_name == 'AppContacts:waiting_number':
        await msg.answer('Теперь введите дату транзакции "Отмена"', reply_markup=cancel_keyboard)
        await AppContacts.waiting_date.set()

    elif state_name == 'Trouble:cooperation':
        await msg.answer('Теперь введи свой электронный ящик или нажми кнопку "Отмена"', reply_markup=cancel_keyboard)
        await Contacts.waiting_email.set()

    await state.update_data(number=number)


@dp.message_handler(content_types=types.ContentType.TEXT, state=[Trouble.cooperation, AppContacts.waiting_number])
async def cancel_contacts(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        return await bot.send_message(message.from_user.id, MESSAGES['change_mind'],
                                      reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Contacts.waiting_email)
async def email(message: types.Message, state: FSMContext):
    data = await state.get_data()
    number = data.get("number")

    new_message = f"""
Пользователь хочет сотрудничать.
*User ID*: {message.from_user.id}
*Email*: {message.text}
*Номер телефона*: {number}
"""
    await state.finish()
    await message.answer("Ваша заявка отправлена оператору, с вами свяжутся в ближайшее время. Спасибо!")
    await bot.delete_message(message.from_user.id, message.message_id - 1)
    return await bot.send_message(HELP_CHAT_ID, new_message, parse_mode="Markdown")


@dp.message_handler(state=AppContacts.waiting_date)
async def waiting_date_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    number = data.get("number")

    new_message = f"""
Списались деньги за потерю.
*User ID*: {message.from_user.id}
*Дата транзакции*: {message.text}
*Номер телефона*: {number}
*Message ID*: {message.message_id}
"""
    await state.finish()
    await message.answer("Ваша заявка отправлена оператору, с вами свяжутся в ближайшее время. Спасибо!")
    #await bot.delete_message(message.from_user.id, message.message_id - 1)
    return await bot.send_message(HELP_CHAT_ID, new_message, parse_mode="Markdown")


@dp.callback_query_handler(state=[Contacts.waiting_email, AppContacts.waiting_date])
async def after_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await state.finish()
    return await bot.send_message(callback_query.from_user.id, MESSAGES['change_mind'])
