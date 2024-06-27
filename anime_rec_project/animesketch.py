import requests
import pandas as pd
import sqlalchemy as db

# Function to get anime data from Jikan API by title
def get_anime_by_title(anime_title):
    """
    Get anime data from Jikan API by title.
    Returns the anime's ID which will be used in the get_similar_anime function.
    """
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"  # Construct the API URL
    response = requests.get(url)  # Make the API request
    if response.status_code == 200 and response.json()['data']:  # Check if the response is successful and data is available
        return response.json()["data"][0]  # Return the first result
    return None  # Return None if the request was unsuccessful or no data found

# Function to fetch similar anime data from Jikan API
def get_similar_anime(anime_id):
    """
    Fetch similar anime data from Jikan API.
    """
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"  # Construct the API URL
    response = requests.get(url)  # Make the API request
    if response.status_code == 200:  # Check if the response is successful
        return response.json()['data']  # Return the data
    return None  # Return None if the request was unsuccessful

# Function to collect similar anime data and store it in a SQLite database
def collect_similar_anime(anime_id):
    """
    Collect similar anime data and store it in a SQLite database.
    """
    similar_anime_data = get_similar_anime(anime_id)  # Fetch similar anime data
    if similar_anime_data:  # Check if there is data
        anime_list = []  # Initialize an empty list to store anime information
        for anime in similar_anime_data:  # Iterate through each similar anime
            anime_info = anime['entry']  # Get the anime entry
            anime_list.append({
                'id': anime_info['mal_id'],
                'title': anime_info['title'],
                'url': anime_info['url']
            })  # Append anime info to the list
        
        df = pd.DataFrame(anime_list)  # Convert list to DataFrame
        engine = db.create_engine('sqlite:///similar_anime_database.db')  # Create a SQLite database engine
        df.to_sql('similar_anime', con=engine, if_exists='replace', index=False)  # Write DataFrame to the SQLite database

# Function to load similar anime data from the SQLite database
def load_similar_anime():
    """
    Load similar anime data from the SQLite database.
    """
    engine = db.create_engine('sqlite:///similar_anime_database.db')  # Create a SQLite database engine
    df = pd.read_sql('similar_anime', con=engine)  # Read data from the SQLite database into a DataFrame
    return df  # Return the DataFrame

# Function to get user input for favorite anime
def get_user_favorite_anime():
    """
    Get user input for favorite anime.
    """
    while True:
        print("\nEnter your favorite anime title:")  # Prompt user for their favorite anime
        user_input = input()  # Get user input
        favorite_anime = get_anime_by_title(user_input)  # Fetch anime data by title
        if favorite_anime:  # Check if anime data is found
            return favorite_anime  # Return the favorite anime data
        else:
            print(f"\nAnime '{user_input}' not found. Please try again.")  # Prompt again if anime not found

# Function to display recommendations
def display_recommendations(recommendations):
    """
    Display recommended similar anime.
    """
    print("\nRecommended Similar Anime:\n")
    for _, anime in recommendations.iterrows():  # Iterate through the DataFrame
        print(f"Title: {anime['title']}")  # Print anime title
        print(f"More Info: {anime['url']}\n")  # Print URL for more information

# Main function to execute the steps
def main():
    """
    Main function to execute the steps.
    """
    print("\nGetting user favorite anime...")
    favorite_anime = get_user_favorite_anime()  # Get user favorite anime
    
    anime_id = favorite_anime['mal_id']  # Extract anime ID
    print(f"\nFetching similar anime for '{favorite_anime['title']}'...")
    collect_similar_anime(anime_id)  # Collect similar anime data
    
    print("\nLoading similar anime data...")
    df = load_similar_anime()  # Load similar anime data from the database
    
    print("\nDisplaying recommendations...")
    display_recommendations(df)  # Display the recommendations

if __name__ == "__main__":
    main()  # Run the main function
