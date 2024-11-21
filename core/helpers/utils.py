"""Helper function used all over the code bases are written here"""

import re
from os import getenv
from urllib.parse import urlparse
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load env
load_dotenv(".env")

class YtSearchResult(BaseModel):
    """Pydantic model for Yt search result"""
    video_id: str
    title: str

def check_valid_yt_url(url: str) -> Optional[str]:
    """Checks if a given string contains a valid url and extracts it
    
    Args:
        url (str): The string containing the yt url
        
    Returns:
        str (str): The url or None
    """
    # Check for a valid YT url
    pattern = r"https:\/\/[a-zA-Z0-9\-\.]+(?:\/[^\s]*)?"
    search_result = re.search(pattern, url)
    if search_result:
        parsed_url = urlparse(search_result.group())
        return search_result.group() if "youtube" in parsed_url.netloc else None
    return None


def youtube_search(query: str, max_results: int = 10) -> List[YtSearchResult]:
    """Returns a list containig the top 10 yt search result for the query
    
    Args:
        query (str): The query to search on yt
        
    Returns:
        List[YtSearchResult]: A list containing the result
    """
    # API key
    api_key = getenv("YT_API")

    # Build the YouTube service
    youtube = build("youtube", "v3", developerKey=api_key)

    # Call the search.list method to search YouTube
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    # return the pydantic model with the top 10 results with url and title
    result = []
    for item in response.get("items", []):
        print(f"res: {item}\n")
        result.append(YtSearchResult(
            video_id=item['id']['videoId'],
            title=item['snippet']['title']
        ))

    return result

def split_string(input_string:str, min_chars:int=25, max_chars:int=35) -> str:
    """
    Splits a string at approximately min_chars to max_chars range without breaking words.
    Adds "..." if the string is longer than the split point.

    Args:
        input_string (str): The string to split.
        min_chars (int): Minimum number of characters before splitting.
        max_chars (int): Maximum number of characters before splitting.

    Returns:
        str: The split string with "..." appended if truncated.
    """
    if len(input_string) <= max_chars:
        return input_string

    # Start splitting within the desired range
    split_index = max_chars
    for i in range(min_chars, max_chars):
        if i >= len(input_string):
            break
        if input_string[i] == " ":  # Prefer splitting at spaces
            split_index = i
            break

    # Create the shortened string with "..."
    shortened = input_string[:split_index].strip() + " ..."
    return shortened
