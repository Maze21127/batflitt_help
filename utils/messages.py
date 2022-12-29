from states.trouble import Trouble

changeback_message = """
Возврат осуществляется в течение 2 - 5 рабочих дней с момента возврата power bank и после осуществления проверки на работоспособность устройства
"""


chat_message_ru = """
Вы переведены в режим чата с оператором, все ваши сообщения будут отправлены оператору.
Пожалуйста, опишите вашу проблему.
Для выхода нажмите кнопку "Выход из чата"
"""

chat_message_en = """
Now you in chat mode with support, all of your messages will be sent to our support service.
Please, describe your issue.
For closing chat click the button "Exit from chat"
"""

chat_message_la = """
Jūs tagad atrodaties tērzēšanas režīmā ar operatoru, un visi jūsu ziņojumi tiks nosūtīti operatoram.
Lūdzu, aprakstiet savu problēmu.
Lai izietu, nospiediet pogu „Aizvērt tērzēšanas režīmu”
"""


def get_message(language: str, message_type: str) -> str:
    return MESSAGES[message_type][language] if language in MESSAGES[message_type] else MESSAGES[message_type]['en']


MESSAGES = {
    "start": {
        "ru": "Привет, я BattFlit",
        "en": "Hi' i'm BattFlit",
        "la": "Sveiki, es esmu BattFlit"
    },
    "start2": {
        "ru": "Чем я могу помочь?",
        "en": "How can i help you?",
        "la": "Kā varu palīdzēt?"
    },
    "charge": {
        "ru": "Нажмите кнопку на боковой панели зарядного устройства.\nТакже проверьте горит ли индикатор на устройстве",
        "en": "Press the button on the side of power bank\nAlso check lighting indicator on power bank",
        "la": "Nospiediet pogu PowerBank sānu panelī.\nPārbaudiet arī, vai deg ierīces indikators"
    },
    "back": {
        "ru": "Верните Power Bank (зарядное устройство) и возьмите новый",
        "en": "Return Power Bank and take new one",
        "la": "Nododiet PowerBank (uzlādes ierīci) atpakaļ un paņemiet jaunu"
    },
    "wire": {
        "ru": "Если провод имеет повреждения верните PowerBank (Зарядку) в станцию и возьмите новый.\nСообщите в приложении, об дефекте устройства",
        "en": "If the wire is damaged, return the PowerBank (Charging) to the station and take a new one.\nReport in the application about the defect of the device",
        "la": "Ja vads ir bojāts, nododiet PowerBank (lādētāju) atpakaļ stacijā un paņemiet jaunu.\nPaziņojiet lietotnē  par ierīces defektu"
    },
    "changeback": {
        "ru": "Возврат осуществляется в течение 2 - 5 рабочих дней с момента возврата power bank и после осуществления проверки на работоспособность устройства",
        "en": "The return is carried out within 2 - 5 working days from the moment the power bank is returned and after the device has been checked for operability",
        "la": "Atpakaļatdošana tiek veikta 2-5 darba dienu laikā, skaitot no PowerBank nodošanas brīža, un pēc ierīces darbspējīguma pārbaudes"
    },
    "other": {
        "ru": "Связаться с поддержкой",
        "en": "Contact with support",
        "la": "Sazināties ar atbalsta dienestu"
    },
    "describe": {
        "ru": "Опишите вашу проблему",
        "en": "Describe your issue",
        "la": "Aprakstiet savu problēmu"
    },
    "number": {
        "ru": "Укажите ваш номер телефона",
        "en": "Set you phone number",
        "la": "Norādiet savu tālruņa numuru"
    },
    "debited_money": {
        "ru": "Укажите свой номер телефона и дату транзакции, и мы свяжемся с вами.",
        "en": "Set your phone number and payment date, and we contact with you",
        "la": "Norādiet savu tālruņa numuru un transakcijas datumu, un mēs ar jums sazināsimies."
    },
    "is_helpful": {
        "ru": "Я смог вам помочь?",
        "en": "Could i help you?",
        "la": "Vai jums noderēja mana palīdzība?"
    },
    "help_success": {
        "ru": "Был рад помочь. Спасибо что используете наш сервис!",
        "en": "Was happy to help. Thank you for using our service!",
        "la": "Palīdzēju ar prieku. Paldies, ka izmantojat mūsu pakalpojumu!"
    },
    "cooperation": {
        "ru": "Укажите свой номер телефона и электронный ящик, и мы свяжемся с вами.",
        "en": "Set your phone number and email, and we contact with you",
        "la": "Norādiet savu tālruņa numuru un elektroniskā pasta adresi, un mēs ar jums sazināsimies."
    },
    "chat": {
        "ru": chat_message_ru,
        "en": chat_message_en,
        "la": chat_message_la,
    },
    "close_chat": {
        "ru": "Оцените качество вашего обслуживания от 1 до 5 ,спасибо вам ❤",
        "en": "Rate the quality of service from 1 to 5, thank you ❤",
        "la": "Novērtējiet apkalpošanas kvalitāti ar atzīmi no 1 līdz 5. Paldies ❤"
    },
    "change_mind": {
        "ru": "Если передумаете, вы в любой момент можете сделать это снова",
        "en": "If you change your mind, you can do it again at any time.",
        "la": "Ja pārdomājat, varat jebkurā laikā to veikt no jauna",
    },
    "close_chat_no_message": {
        "ru": "Если передумаете, нажмите на ту же кнопку.",
        "en": "If you change your mind, click on the same button.",
        "la": "Ja pārdomājat, nospiediet to pašu pogu.",
    },
    "is_returned": {
        "ru": "Вы вернули PowerBank?",
        "en": "Have you returned the PowerBank?",
        "la": "Vai nodevāt atpakaļ PowerBank?"
    },
    "need_return": {
        "ru": "Необходимо вернуть повербанк. До момента возвращение он считается купленным вами.",
        "en": "You need to return the bank. Until the moment of return, it is considered purchased by you.",
        "la": "Jums ir jānodod atpakaļ PowerBank. Līdz nodošanas brīdim tiek uzskatīts, ka jūs to iegādājāties."
    },
    'success_number': {
        "ru": "Твой номер успешно получен",
        "en": "Your number has been successfully received",
        "la": "Jūsu numurs ir veiksmīgi saņemts"
    },
    "waiting_number": {
        "ru": 'Теперь введите дату транзакции или нажми на кнопку "Отмена"',
        "en": "Now input payment date or click 'Cancel' button",
        "la": "Tagad ievadiet transakcijas datumu vai nospiediet pogu „Atcelt”"
    },
    'waiting_email': {
        "ru": 'Теперь введи свой электронный ящик или нажми кнопку "Отмена"',
        "en": "Now input email or click 'Cancel' button",
        "la": "Tagad ievadiet savu elektroniskā pasta adresi vai nospiediet pogu „Atcelt”"
    },
    "request_sent": {
        "ru": "Ваша заявка отправлена оператору, с вами свяжутся в ближайшее время. Спасибо!",
        "en": "Your request sent to support, you will be contacted shortly. Thank you!",
        "la": "Jūsu pieprasījums ir nosūtīts operatoram, ar jums tuvākajā laikā sazināsies. Paldies!"
    },
    "change_language": {
        "ru": "Выберите язык",
        "en": "Choose language",
        "la": "Izvēlieties valodu"
    }
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

ANSWER_MESSAGE = 'Что бы ответить пользователю, нажмите "Ответить" на сообщение выше, иначе пользователь не получит ответ.'
