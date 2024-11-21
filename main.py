"""
The main entry point to run the bot. This file is responsible to run 
all the dependencies and construct improtant variables.
"""

import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core import register_handlers

# Important Variables
TOKEN = getenv("TOKEN")

async def main() -> None:
    """
    The main sync function that starts the polling of the bot and keeps it online.
    """
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    # All handlers should be attached to the Dispatcher
    dp = Dispatcher()
    register_handlers(dp)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())