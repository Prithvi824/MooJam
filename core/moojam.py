"""
This file is responsible for defining all the functions and feautures 
to be used by the bot.
Every function of the bot should be either imported here or created here 
in the MooJamBot class according to the needs.
"""

import os
import json
from aiogram.types import Message, FSInputFile, URLInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.enums import ParseMode
from .downloader import Downloader
from .helpers.utils import check_valid_yt_url, youtube_search, split_string, generate_url_with_id
from .config import MESSAGES_PATH, DOWNLOADS_DIR

# Load the messages
with open(MESSAGES_PATH, "r", encoding="utf-8") as file:
    messages = json.load(file)

# Initialize the downloader
DOWNLOADER = Downloader(DOWNLOADS_DIR)

class MooJamBot:
    @staticmethod
    async def start(message: Message) -> None:
        """
        This handler is for the `/start` command
        """
        
        await message.answer(messages["intro"], parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    async def help(message: Message) -> None:
        """
        This handler is for the `/help` command
        """
        await message.answer(messages["help"], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    @staticmethod
    async def handle_yt_links(message: Message) -> None:
        """
        This handler is to handle any yt link sent in the chat.
        """
        # Download the file
        url = check_valid_yt_url(message.text)
        download_details = await DOWNLOADER.download_async(url)

        # Upload the file to telegram servers and remove from local
        file_with_ext = os.path.basename(download_details.path)
        file_name = os.path.splitext(file_with_ext)[0]
        audio_file = FSInputFile(download_details.path, file_with_ext)
        thumbnail = URLInputFile(download_details.thumbnail, filename=f"{file_name}.png")

        # Send to user
        # TODO: Store the file id to a database
        sent_msg = await message.answer_audio(audio_file, thumbnail=thumbnail)

        # delete the message and clean local storage
        await message.delete()
        DOWNLOADER.clean_all()

    @staticmethod
    async def handle_yt_search(message: Message) -> None:
        """
        This handler is to handle a yt search in the chat.
        """
        # Get the top 10 yt search result
        search_result = youtube_search(message.text)

        # Construct the keyboard
        keyboard_btns = []
        for index, result in enumerate(search_result, 1):
            text = split_string(f"{index}. {result.title}")
            keyboard_btns.append(
                [InlineKeyboardButton(text=text, callback_data=result.video_id)]
            )
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_btns, row_width=1)

        # Send the keyboard and wait for reply
        await message.answer(f"Search results for <b><i>{message.text}</i></b>",parse_mode=ParseMode.HTML, reply_markup=keyboard, reply_to_message_id=message.message_id)

    # Callback handler for button presses
    @staticmethod
    async def process_callback(callback_query: CallbackQuery):
        # Download the file
        vid_id = callback_query.data
        url = generate_url_with_id(vid_id)
        download_details = await DOWNLOADER.download_async(url)

        # Upload the file to telegram servers and remove from local
        file_with_ext = os.path.basename(download_details.path)
        file_name = os.path.splitext(file_with_ext)[0]
        audio_file = FSInputFile(download_details.path, file_with_ext)
        thumbnail = URLInputFile(download_details.thumbnail, filename=f"{file_name}.png")

        # Send to user
        # TODO: Store the file id to a database
        sent_msg = await callback_query.bot.send_audio(callback_query.from_user.id, audio_file, thumbnail=thumbnail)
        await callback_query.answer()

        # delete the message and clean local storage
        await callback_query.bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        DOWNLOADER.clean_all()
