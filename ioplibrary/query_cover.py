import re
import requests
from requests.exceptions import SSLError, ReadTimeout, ConnectionError
from duckduckgo_search import ddg_images
from .parameters import *


def compare_content(string1, string2):
    list_1 = set(word.lower() for word in re.findall(r'\b\w+\b', string1)) - EXCLUSION_SET
    list_2 = set(word.lower() for word in re.findall(r'\b\w+\b', string2)) - EXCLUSION_SET
    print(list_1)
    print(list_2)
    print(list_2.issubset(list_1))
    for instance in SKIP_SET:
        if instance in list_1:
            return False
    return list_2.issubset(list_1)


def get_cover_ddg(**query):
    for q in query.values():
        ddg_query = ddg_images(
            keywords=q,
            region="us-en",
            safesearch='on',
            size='Medium',
            color=None,
            type_image=None,
            layout='Tall',
            license_image=None,
            max_results=20,
            download=False
        )

        for result in ddg_query:
            print(q)
            print(result)
            if compare_content(result['title'], query['title']):
                try:
                    response = requests.head(result['image'], timeout=3, verify=False)
                    if response.status_code == 200:
                        return result['image']
                except (SSLError, ConnectionError, ReadTimeout):
                    continue
            print()
    return ""


def get_cover_luh(query):
    return ""


def save_cover(cover_url, isbn):
    if cover_url == "":
        return UNAVAILABLE_COVER_URL
    response = requests.get(cover_url, timeout=3, verify=False)
    print(f"Response Code: {response.status_code}")
    if response.status_code == 200:
        cover_path = f"./media/{COVERS_DIR}/{isbn}.jpg"
        with open(cover_path, 'wb') as f:
            f.write(response.content)
    return f"{COVERS_DIR}/{isbn}.jpg"
