from states.trouble import Trouble

changeback_message = """
Возврат осуществляется в течение 2 - 5 рабочих дней с момента возврата power bank и после осуществления проверки на работоспособность устройства
"""


chat_message = """
Вы переведены в режим чата с оператором, все ваши сообщения будут отправлены оператору.
Пожалуйста, опишите вашу проблему.
Для выхода нажмите кнопку "Выход из чата"
"""

MESSAGES = {
    "start": "Привет, я BattFlit.",
    "start2": "Чем я могу помочь?",
    "charge": "Нажмите кнопку на боковой панели зарядного устройства. "
              "Также проверьте горит ли индикатор на устройстве",
    "back": "Верните PowerBank (зарядку) в станцию и возьмите новый",
    "wire": "Если провод имеет повреждения верните PowerBank (Зарядку) в станцию и возьмите новый. "
            "Сообщите в приложении, об дефекте устройства.",
    "changeback": changeback_message,
    "other": "Контакт менеджера",
    "describe": "Опишите вашу проблему",
    "number": "Укажите номер телефона",
    'debited_money': "Укажите свой номер телефона и дату транзакции, и мы свяжемся с вами.",
    "is_helpful": "Я смог вам помочь?",
    "help_success": "Был рад помочь. Спасибо что используете наш сервис!",
    'cooperation': 'Укажите свой номер телефона и электронный ящик, и мы свяжемся с вами.',
    'chat': chat_message,
    'close_chat': "Оцените качество вашего обслуживания от 1 до 5 ,спасибо вам ❤️",
    'change_mind': "Если передумаете, вы в любой момент можете сделать это снова",
    'close_chat_no_message': "Если передумаете, нажмите на ту же кнопку.",
    'is_returned': "Вы вернули PowerBank?",
    'need_return': "Необходимо вернуть повербанк. До момента возвращение он считается купленным вами."
}


troubles = {
    'charge': Trouble.charging,
    'back': Trouble.back,
    'wire': Trouble.wire,
    'changeback': Trouble.changeback,
    'debited_money': Trouble.debited_money,
    'cooperation': Trouble.cooperation,
    'other': Trouble.other
}

helpful_states = tuple(troubles.keys())[:-2]