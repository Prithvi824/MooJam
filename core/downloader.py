import os
import asyncio
from typing import Dict, Optional
from pydantic import BaseModel
from yt_dlp import YoutubeDL

class DownloaderOutput(BaseModel):
    """Pydantic model for output example of a downloaded file"""
    path: str
    thumbnail: Optional[str]

class Downloader():
    """This class is responsible to download the music video from a given link"""
    def __init__(self, output_folder: str, config: Dict[str, str | int] = {}) -> None:
        # Default config
        os.makedirs(output_folder, exist_ok=True)
        self.output_folder = output_folder
        self.config = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
            "age_limit": 10 * 60
        }

        # Keep a track of all downloaded files
        self.downloaded = []

        # Add the new config
        for key, value in config.items():
            self.config[key] = value
    
    async def download_async(self, yt_url: str) -> DownloaderOutput:
        """Runs the download in a separate thread to avoid blocking."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.download, yt_url)

    def download(self, yt_url) -> DownloaderOutput:
        """Main function containing the logic for downloading songs
        
        Args:
            yt_url (str): The url to the song
        
        Returns:
            DownloaderOutput (DownloaderOutput): The pydantic model containing details to the downloaded file
        """
        with YoutubeDL(self.config) as ydl:
            # Extract information and download
            info_dict = ydl.extract_info(yt_url, download=True)
            downloaded_path = ydl.prepare_filename(info_dict)

            # Add to the downloaded list
            self.__add_downloaded__(downloaded_path)
            return DownloaderOutput(path=downloaded_path, thumbnail=info_dict.get("thumbnail"))

    def __add_downloaded__(self, path: str) -> None:
        """Add the downloaded file to a list to keep track and clear all at once
        
        Args:
            path (str): The path to add

        Returns:
            None (None): None
        """
        self.downloaded.append(path)

    def clean_all(self) -> None:
        """Delete all downloaded files and songs
                
        Args:
            None (None): None

        Returns:
            None (None): None
        """
        for path in self.downloaded:
            os.remove(path)
        self.downloaded = []