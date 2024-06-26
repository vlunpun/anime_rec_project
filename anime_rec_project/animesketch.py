import requests
import pandas as pd
import sqlalchemy as db

# Function to get anime data from Jikan API by title
def get_anime_by_title(anime_title):
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['data']:
        # Returns the anime's ID which will be used in the get_similar_anime function
        return response.json()["data"][0]
    return None

# Function to fetch similar anime data from Jikan API
def get_similar_anime(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    return None

# Function to collect similar anime data and store it in a SQLite database
def collect_similar_anime(anime_id):
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
        df.to_sql('similar_anime', con=engine, if_exists='replace', index=False)

# Function to load similar anime data from the SQLite database
def load_similar_anime():
    engine = db.create_engine('sqlite:///similar_anime_database.db')
    df = pd.read_sql('similar_anime', con=engine)
    return df

# Function to get user input for favorite anime
def get_user_favorite_anime():
    while True:
        print("\nEnter your favorite anime title:")
        user_input = input()
        favorite_anime = get_anime_by_title(user_input)
        if favorite_anime:
            return favorite_anime
        else:
            print(f"\nAnime '{user_input}' not found. Please try again.")

# Function to display recommendations
def display_recommendations(recommendations):
    print("\nRecommended Similar Anime:\n")
    for _, anime in recommendations.iterrows():
        print(f"Title: {anime['title']}")
        print(f"More Info: {anime['url']}\n")

# Main function to execute the steps
def main():
    print("\nGetting user favorite anime...")
    favorite_anime = get_user_favorite_anime()
    
    anime_id = favorite_anime['mal_id']
    print(f"\nFetching similar anime for '{favorite_anime['title']}'...")
    collect_similar_anime(anime_id)
    
    print("\nLoading similar anime data...")
    df = load_similar_anime()
    
    print("\nDisplaying recommendations...")
    display_recommendations(df)

if __name__ == "__main__":
    main()
