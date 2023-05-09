import re
import requests
from requests.exceptions import SSLError, ReadTimeout, ConnectionError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .constants import *


def get_cover_gg(title: str, authors: str) -> str:
    gg_service = build("customsearch", "v1", developerKey=GG_CUSTOM_SEARCH_API)
    
    try:
        result_list = gg_service.cse().list(
            q=f"book {title} {authors}",
            cx=GG_CUSTOM_SEARCH_ENGINE_ID,
            searchType="image",
            imgSize="LARGE",
            fileType="jpg",
            num="10",
        ).execute()

        print(result_list)
        for result in result_list["items"]:
            if result["image"]["width"] < result["image"]["height"]:
                return result["link"]
    except (KeyError, HttpError):
        print("ERROR!")
        return ""
    return ""


def get_cover_luh(query) -> str:
    return ""


def save_cover(cover_url: str, isbn: str) -> str:
    if cover_url == "":
        return UNAVAILABLE_COVER_URL
    response = requests.get(cover_url, timeout=3, verify=True)
    if response.status_code == 200:
        cover_path = f"./media/{COVERS_DIR}/{isbn}.jpg"
        with open(cover_path, 'wb') as f:
            f.write(response.content)
    else:
        return UNAVAILABLE_COVER_URL
    return f"{COVERS_DIR}/{isbn}.jpg"
