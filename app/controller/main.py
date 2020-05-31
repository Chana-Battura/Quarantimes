from flask import (
    Blueprint, render_template
)
import imdb
from flask import current_app as app


from flask_socketio import SocketIO
socketio = SocketIO(app._get_current_object())

import requests


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='Flask-PWA')

@bp.route('/news')
def news():
    key = '6c7384f5ff6c451ea22f00e0aea9cb60'
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': 'COVID-19',
        'pageSize': 12,
        'apiKey' : key
    }
    response = requests.get(url, params=parameters)
    response_json = response.json()

    return render_template('main/news.html',response_json = response_json['articles'] )


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

@bp.route('/blog')
def blog():
    x = [["https://www.allrecipes.com/recipes/1642/everyday-cooking/", "https://www.kingarthurflour.com/sites/default/files/recipe_legacy/20-3-large.jpg", "cooking", "recipes to daily food"],

["https://www.healthline.com/health/fitness-exercises/definitive-guide-to-yoga", "https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/article_thumbnails/reference_guide/the_health_benefits_of_yoga_ref_guide/650x350_the_health_benefits_of_yoga_ref_guide.jpg", "yoga", "Many people begin practicing yoga as a way to cope with feelings of anxiety"],

["https://www.miraclegro.com/en-us/library/gardening-basics/10-top-gardening-tips-beginners", "https://gardenerspath.com/wp-content/uploads/2016/08/square-foot-garden-FB.jpg", "10 Top Gardening Tips for Beginners", "Wondering how to start a garden? Find your confidence with these expert gardening tips."],

["https://www.bookbub.com/blog/best-book-series-publishers-blurbs", "https://theknow.denverpost.com/wp-content/uploads/2020/04/GettyImages-1089392442.jpg", "The Best Book Series of All Time: An Ultimate List", "Reading is important because it develops our thoughts, gives us endless knowledge and lessons while keeping our minds active"],

["https://theinspirationgrid.com/category/art/", "https://mymodernmet.com/wp/wp-content/uploads/2019/03/elements-of-art-6.jpg", "Art Inspiration", "Love art, but have no inspiration? Check out this website!"]]
    return render_template('main/blog.html', things = x )

@bp.route('/chat')
def chat():
    socketio.run(app._get_current_object(), '127.0.0.1', debug=True, port=5000)
    return render_template('main/session.html')

def messageReceived(methods=['GET', 'POST']):
    with app.app_context():
        print('Yo')
        print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    with app.app_context():
        print('received my event: ' + str(json))
        socketio.emit('my response', json, callback=messageReceived)
