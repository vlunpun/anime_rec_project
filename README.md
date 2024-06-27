# Anime Recommendation Project

This project fetches information about an anime and its recommendations using the Jikan API and stores the data in a SQLite database using Python.

## Setup Instructions

### Prerequisites

Make sure you have the following libraries installed:

- requests
- pandas
- SQLAlchemy

You can install these libraries using pip:

```
pip install requests pandas sqlalchemy
```
## API Information
This project uses the Jikan API, a RESTful API that provides data from MyAnimeList.net. This API does not require authentication for endpoints.

## Overview of anime_rec_project Folder

### Project.txt
A text file that shows our thought process of coming up with this project

### animejson.py
This file is just used to understand the parsing of these JSON dictionaries and understanding what is returned.

### animesketch.py
This file is the main file where all the functionality of this project is shown.

1. get_anime_by_title(anime_title) 
- Description: Fetches anime data from the Jikan API by the provided anime title and returns the anime's information.
- Workflow:
    - Constructs the API request URL using the provided title.
    - Sends a GET request to the Jikan API.
    - Parses the JSON response to extract the anime's data.
    - Returns the anime's data if found, otherwise returns None.

2. get_similar_anime(anime_id)
- Description: Fetches similar anime recommendations from the Jikan API using the provided anime ID.

- Workflow: 
    - Constructs the API request URL using the provided mal_id.
    - Sends a GET request to the Jikan API.
    - Parses the JSON response to extract the similar anime recommendations.
    - Returns the recommendations if found, otherwise returns None.

3. collect_similar_anime(anime_id)
- Description: Collects similar anime data and stores it in a SQLite database.
- Workflow:
    - Calls get_similar_anime to fetch similar anime data.
    - Extracts necessary information from the response and stores it in a list of dictionaries.
    - Converts the list of dictionaries to a pandas DataFrame.
    - Creates a SQLite database engine.
    - Stores the DataFrame in the SQLite database.

4. load_similar_anime()
- Description: Loads similar anime data from the SQLite database.
- Workflow:
    - Creates a SQLite database engine.
    - Reads data from the SQLite database into a pandas DataFrame.
    - Returns the DataFrame.

5. get_user_favorite_anime()
Description: Gets user input for their favorite anime title.
- Workflow:
    - Prompts the user to enter their favorite anime title.
    - Calls get_anime_by_title to fetch the anime's data.
    - If the anime is found, returns the data.
    - If the anime is not found, prompts the user to try again.

6. display_recommendations(recommendations)
- Description: Displays the recommended similar anime.
- Workflow:
    - Iterates through the DataFrame.
    - Prints the title and URL of each recommended anime.

7. main()
- Description: Main function to execute the steps of the project.
- Workflow:
    - Calls functions 5, 3, 4, 6 (successively)


![Deploy Badge](https://github.com/vlunpun/anime_rec_project/actions/workflows/style.yaml/badge.svg