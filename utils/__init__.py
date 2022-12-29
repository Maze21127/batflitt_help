from aiogram import types

from logger import logger


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start bot'),
        types.BotCommand('help', 'Help'),
        types.BotCommand('language', 'Change language'),
    ])
    logger.info("Commands added")
