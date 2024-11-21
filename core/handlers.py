"""
This file is responsible for linking all the functions and their handlers 
used by the bot.
Every handler should be registered in the register_handlers function.
"""

from aiogram import Dispatcher
from aiogram.types import Message
from .commands import MooJamCommands
from .moojam import MooJamBot

def register_handlers(dp: Dispatcher):
    # Register the Start command: `/start`
    @dp.message(MooJamCommands.start())
    async def __handle_start__(message: Message):
        """Register handler for the `/start command`"""        
        await MooJamBot.start(message)

    # Register the Help command: `/help`
    @dp.message(MooJamCommands.help())
    async def __handle_help__(message: Message):
        """Register handler for the `/help command`"""
        await MooJamBot.help(message)

    # Register Yt link sent in the chat: `Youtube`
    @dp.message(lambda message: MooJamCommands.handle_yt_link(message.text.lower()))
    async def __handle_handle_yt_link__(message: Message):
        """Register handler for the yt links shared in the chat"""
        await MooJamBot.handle_yt_links(message)

    # Register Yt link sent in the chat: `Youtube`
    @dp.message(lambda message: MooJamCommands.handle_yt_search(message.text))
    async def __handle_search__(message: Message):
        """Register handler for doing a yt search in the chat"""
        await MooJamBot.handle_yt_search(message)

    # Register the callback query handler
    @dp.callback_query(lambda message: MooJamCommands.handle_callbacks(message))
    async def __handle_callbacks__(message: Message):
        """Register handler for callbacks from inline keyboards"""
        await MooJamBot.process_callback(message)
