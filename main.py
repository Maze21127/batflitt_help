from aiogram import executor, Dispatcher
from logger import logger
from loader import dp

import handlers, keyboards, states, utils


async def on_startup(dispatcher: Dispatcher):
    from utils import set_default_commands
    await set_default_commands(dispatcher)
    logger.info("Start bot")


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info("Bot shut down")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

