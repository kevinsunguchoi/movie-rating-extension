from flask import Flask, request, session
from sentiment_analysis import analyze_movie
import json

app = Flask(__name__, static_url_path='/static')

app.secret_key = "cs410-final-project-chrome-extension"

@app.route('/')

def index():

    # Initialize session keys if they don't exist
    session.setdefault('movie_id', None)
    session.setdefault('reviews', None)

    # Receive session from /process_data
    movie_id = session['movie_id']
    reviews = session['reviews']

    # Object received from sentiment_analysis.py script
    movie_sentiment = json.loads(analyze_movie(movie_id, int(reviews)))

    return movie_sentiment

@app.route('/process_data', methods=['POST'])

def process_data():

    # Receive movie_id and reviews from javascript frontend
    data = request.get_json()
    movie_id, reviews = data

    # Record the movie_id and reviews into session variable
    session['movie_id'] = movie_id
    session['reviews'] = reviews

    return 'Data Received'


if __name__ == '__main__':
    app.run(port=5001)
