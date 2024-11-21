"""
This file is responsible for defining all the commands and filters 
to be used when registering event handlers for the bot
Every filter or command should be registered in the MooJamCommands class according to the needs.
"""

from aiogram.filters import Command
from aiogram.types import CallbackQuery
from .helpers.utils import check_valid_yt_url

class MooJamCommands():
    @staticmethod
    def start():
        """Returns true if the `/start` command is detected"""
        return Command("start", ignore_case=True)

    @staticmethod
    def help():
        """Returns true if the `/help` command is detected"""
        return Command("help", ignore_case=True)

    @staticmethod
    def handle_yt_link(message: str) -> bool:
        """Returns true if a valid yt url is detected"""
        return True if check_valid_yt_url(message) else False

    @staticmethod
    def handle_yt_search(message: str) -> bool:
        """Returns true for all the text meessages since a YT search should be done"""
        return True if isinstance(message, str) else False
    
    @staticmethod
    def handle_callbacks(callback: CallbackQuery) -> bool:
        return True if isinstance(callback, CallbackQuery) else False