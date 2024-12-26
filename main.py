from wsgiref.validate import validator
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# movie api's links
MOVIE_API = 'https://api.themoviedb.org/3/search/movie'
MOVIE_API_KEY = os.getenv('MOVIE_API_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Rating form to update the rating and review for the movies
class ratingForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')

# Form to add a new movie
class addMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

# Base for forms
class Base(DeclarativeBase):
    pass

# Database configurations
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)

# CREATE DB schema
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)

# CREATE TABLE
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    """
    Showing all movies from the database on hte hime page
    """
    result = db.session.execute(db.select(Movie).order_by(desc(Movie.rating)))
    all_movies = result.scalars().all()
    for index, movie in enumerate(all_movies):
        movie.ranking = index + 1
    db.session.commit()
    return render_template("index.html", movies=all_movies[::-1])

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    """
    Edit the rating and review of the movies
    """
    form = ratingForm()
    id = request.args.get('id')
    if form.validate_on_submit():
        movie_to_update = db.get_or_404(Movie, id)
        movie_to_update.rating = request.form['rating']
        movie_to_update.review = request.form['review']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form)

@app.route('/delete', methods=['GET'])
def delete():
    """
    Delete the movie from the database
    """
    id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Search the movie form the TMDB api using query
    """
    form = addMovieForm()
    if form.validate_on_submit():
        query = request.form['title']

        # Get related movies using the query
        header = {
            "accept": "application/json",
        }
        params = {
            'api_key': MOVIE_API_KEY,
            'query': query,
        }
        response = requests.get(MOVIE_API, params=params, headers=header)
        movie_data = response.json()
        movie_data = movie_data['results']
        return render_template('select.html', movies=movie_data)
    return render_template('add.html', form=form)

@app.route('/find')
def add_movie():
    """
    Add the movie details from the api to the database
    """
    movie_id = request.args.get('movie_id')

    # Get movie data from the api
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    header = {
        "accept": "application/json",
    }
    params={
        'api_key': MOVIE_API_KEY,
    }
    response = requests.get(url, params=params, headers=header)
    data = response.json()

    # Exception handing for none poster path
    poster_url = data.get('poster_path')
    if not poster_url:
        poster_url = 'https://via.placeholder.com/500x750?text=No+Image+Available'
    else:
        poster_url = 'https://image.tmdb.org/t/p/w500'+data['poster_path']

    # Movie object for adding to database
    movie = Movie(
        title=data['title'],
        year=data['release_date'][:4],
        img_url=poster_url,
        description=data['overview']
    )
    db.session.add(movie)
    db.session.flush()
    movie_db_id = movie.id
    db.session.commit()
    return redirect(url_for('edit', id=movie_db_id))

if __name__ == '__main__':
    app.run(debug=True)
