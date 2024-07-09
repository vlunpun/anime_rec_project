from flask import Flask, render_template, url_for, flash, redirect, request
from forms import AnimeForm
import requests
import pandas as pd
import sqlalchemy as db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def get_anime_by_title(anime_title):
    url = f"https://api.jikan.moe/v4/anime?q={anime_title}&limit=1"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['data']:
        return response.json()["data"][0]
    return None

def get_similar_anime(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    return None

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

def load_similar_anime():
    engine = db.create_engine('sqlite:///similar_anime_database.db')
    df = pd.read_sql('similar_anime', con=engine)
    return df

@app.route("/", methods=['GET', 'POST'])
def home():
    form = AnimeForm()
    if form.validate_on_submit():
        anime_title = form.anime_title.data
        favorite_anime = get_anime_by_title(anime_title)
        if favorite_anime:
            anime_id = favorite_anime['mal_id']
            collect_similar_anime(anime_id)
            return redirect(url_for('recommendations'))
        else:
            flash(f"Anime '{anime_title}' not found. Please try again.", 'danger')
    return render_template('home.html', form=form)

@app.route("/recommendations")
def recommendations():
    df = load_similar_anime()
    recommendations = df.to_dict(orient='records')
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
