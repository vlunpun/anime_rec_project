import requests
import pandas as pd
import sqlalchemy as db
import json


def fetch_anime_by_title(anime_title):
    """
    Fetch anime data from Jikan API by title and return the anime ID.
    """
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["data"][0]["mal_id"]
        if data:
            return data
    return None


def get_similar_anime(anime_id):
    """
    Fetch similar anime data from Jikan API by anime ID.
    """
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        if data:
            print(json.dumps(data, indent=4))
    return None


get_similar_anime(fetch_anime_by_title("One Punch Man"))
