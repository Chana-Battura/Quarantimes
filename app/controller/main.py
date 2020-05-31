from flask import (
    Blueprint, render_template
)
import imdb
from flask import current_app as app


from flask_socketio import SocketIO
socketio = SocketIO(app._get_current_object())


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
