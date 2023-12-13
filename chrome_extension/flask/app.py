from flask import Flask, request, session
from sentiment_analysis import analyze_movie
import json

app = Flask(__name__, static_url_path='/static')

app.secret_key = "cs410-final-project-chrome-extension"

@app.route('/')

def index():

    movie_id = session['movie_id']
    reviews = session['reviews']

    movie_sentiment = json.loads(analyze_movie(movie_id, int(reviews)))

    return movie_sentiment

@app.route('/process_data', methods=['POST'])

def process_data():

    data = request.get_json()
    movie_id, reviews = data

    session['movie_id'] = movie_id
    session['reviews'] = reviews

    return 'Data Received'


if __name__ == '__main__':
    app.run(debug=True)
