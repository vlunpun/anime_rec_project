import requests
import pandas as pd
import sqlalchemy as db


def get_anime_by_title(anime_title):
    """
    Get anime data from Jikan API by title.
    Returns the anime's ID which will be used in get_similar_anime.
    """
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['data']:
        return response.json()["data"][0]
    return None


def get_similar_anime(anime_id):
    """
    Fetch similar anime data from Jikan API.
    """
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    return None


def collect_similar_anime(anime_id):
    """
    Collect similar anime data and store it in a SQLite database.
    """
    similar_anime_data = get_similar_anime(anime_id)
    if similar_anime_data:
        anime_list = []
        for anime in similar_anime_data:
            anime_info = anime['entry']
            anime_list.append({
                'id': anime_info['mal_id'],
                'title': anime_info['title'],
                'url': anime_info['url']
            })

        df = pd.DataFrame(anime_list)
        engine = db.create_engine('sqlite:///similar_anime_database.db')
        df.to_sql('similar_anime', con=engine, if_exists='replace', index=False
                  )


def load_similar_anime():
    """
    Load similar anime data from the SQLite database.
    """
    engine = db.create_engine('sqlite:///similar_anime_database.db')
    df = pd.read_sql('similar_anime', con=engine)
    return df


def get_user_favorite_anime():
    """
    Get user input for favorite anime.
    """
    while True:
        print("\nEnter your favorite anime title (or 'q' to quit):")
        user_input = input()
        if user_input.lower() == 'q':
            return None
        favorite_anime = get_anime_by_title(user_input)
        if favorite_anime:
            return favorite_anime
        else:
            print(f"\nAnime '{user_input}' not found. Please try again.")


def display_recommendations(recommendations):
    """
    Display recommended similar anime.
    """
    print("\nRecommended Similar Anime:\n")
    for _, anime in recommendations.iterrows():
        print(f"Title: {anime['title']}")
        print(f"More Info: {anime['url']}\n")


def main():
    """
    Main function to execute the steps.
    """
    while True:
        print("\nGetting user favorite anime...")
        favorite_anime = get_user_favorite_anime()
        if favorite_anime is None:
            print("\nYou chose to quit. Exiting the program. Goodbye!")
            break

        anime_id = favorite_anime['mal_id']
        print(f"\nFetching similar anime for '{favorite_anime['title']}'...")
        collect_similar_anime(anime_id)

        print("\nLoading similar anime data...")
        df = load_similar_anime()

        print("\nDisplaying recommendations...")
        display_recommendations(df)


if __name__ == "__main__":
    main()
