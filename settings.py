from os import getenv
from dotenv import load_dotenv


load_dotenv('.env')

BOT_TOKEN = getenv('BOT_TOKEN')
HELP_CHAT_ID = int(getenv('HELP_CHAT_ID'))
