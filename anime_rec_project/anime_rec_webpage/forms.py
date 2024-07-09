from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AnimeForm(FlaskForm):
    anime_title = StringField('Favorite Anime Title', validators=[DataRequired()])
    submit = SubmitField('Get Recommendations')
