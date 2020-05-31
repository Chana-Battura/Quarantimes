from flask import (
    Blueprint, render_template
)
import imdb

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='Flask-PWA')

@bp.route('/movies')

def movies():

    ia = imdb.IMDb()

    # getting top 250 movies
    search = ia.get_top250_movies()

    # printing only first 10 movies title
    movies = []
    x = search[:6]
    for i in range(len(x)):
        print(i)
        movie = ia.get_movie(str(x[i].getID()))
        movies.append(movie)

    return render_template('main/movies.html', movies = movies )
