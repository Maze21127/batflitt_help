from os import getenv
from dotenv import load_dotenv


load_dotenv('.env')

BOT_TOKEN = getenv('BOT_TOKEN')
HELP_CHAT_ID = int(getenv('HELP_CHAT_ID'))
HELPERS_ID = map(int, getenv("HELPERS_ID")[1:-1].replace(",", "").split())
CHATS_ID = map(int, getenv("CHATS_ID")[1:-1].replace(",", "").split())

USER_CHATS = {key: value for key, value in zip(HELPERS_ID, CHATS_ID)}
print(USER_CHATS)
