# Personal-Movie-Blog

Welcome to my Personal Movie Blog project! This application is a dynamic and interactive movie blog where users can add, rate, and review their favorite movies. Built using Flask, it also integrates with the TMDB API to fetch movie details and images.

## Features

* Add Movies: Search for movies using the TMDB API and add them to your collection.
* Rate and Review: Update ratings and reviews for the movies in your collection.
* Delete Movies: Remove movies from the collection.
* Dynamic Rankings: Movies are ranked based on their ratings.

## Tech Stack

* Backend: Flask, Flask-SQLAlchemy, Flask-Bootstrap, Flask-WTF
* Frontend: HTML, CSS (Bootstrap and custom styles)
* Database: SQLite
* API Integration: TMDB (The Movie Database) API
* Environment Management: Python-dotenv
* Version Control: Git

## Project Structure
```
- instance/
  - movies.db              # SQLite database
- static/
  - css/
    - styles.css           # Custom CSS for styling
- templates/
  - add.html               # Add movie form page
  - base.html              # Base HTML template
  - edit.html              # Edit movie rating and review
  - index.html             # Homepage to display movies
  - select.html            # Movie selection from API results
- main.py                  # Flask application entry point
- .env                     # Environment variables (e.g., API key)
- requirements.txt         # Dependencies for the project
```
## Installation

* Clone the repository:
```
git clone https://github.com/Dexter135790/Personal-Movie-Blog
cd personal-movie-blog
```

* Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

* Install dependencies:
```
pip install -r requirements.txt
```

* Add your TMDB API key:

    * Create a .env file in the project root.
    * Add the following line:
    ```
    MOVIE_API_KEY=your_tmdb_api_key
    ```

* Initialize the database:
```
python main.py
```
* Run the application:
```
flask run
```

## Project demonstration
[Demonstration](https://drive.google.com/file/d/11mpUDhdlurlwtE7PQcxktN61IvBIBlPa/view?usp=sharing)

## How It Works
* Homepage:

    * Displays the list of movies stored in the database, ranked by their ratings.
* Adding Movies:

    * Search for a movie using the TMDB API.
    * Select a movie from the search results to add it to the database.
* Editing Movies:

    * Update the rating and review of a movie.
    * Rankings are updated dynamically based on ratings.
* Deleting Movies:

    * Remove a movie from the database.

## Future Enhancements
* User Authentication: Add user accounts for personalized movie collections.
* Advanced Search: Filter and sort movies by genre, release year, or rating.
* Responsive Design: Improve mobile and tablet compatibility.


