import requests
from bs4 import BeautifulSoup
import nltk

from nltk.sentiment import SentimentIntensityAnalyzer
import json

unwanted = nltk.corpus.stopwords.words("english")
unwanted.extend([w.lower() for w in nltk.corpus.names.words()])


def get_reviews(movie_id, review_amount):
    url = 'https://www.imdb.com/title/' + movie_id + '/reviews/_ajax?ref_=undefined&paginationKey={}'
    key = ''
    movie_reviews = []
    while True:
        response = requests.get(url.format(key))
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination_key = soup.find("div", class_="load-more-data")
        if not pagination_key:
            break
        key = pagination_key["data-key"]
        for title, review in zip(soup.find_all(class_="title"), soup.find_all(class_="text show-more__control")):
            movie_reviews.append({'title': title.get_text(), 'review': review.get_text()})
            if len(movie_reviews) == review_amount:
                return movie_reviews
    return movie_reviews


def get_movie_sentiments(movie_reviews):
    mean_compound = 0
    positive_reviews = []
    neutral_reviews = []
    negative_reviews = []
    sia = SentimentIntensityAnalyzer()
    for review_dict in movie_reviews:
        title = review_dict.get('title')
        review = review_dict.get('review')
        title_sentiment = sia.polarity_scores(title)
        first_sentence_sentiment = sia.polarity_scores(review.partition('.')[0])
        review_sentiment = sia.polarity_scores(title)
        # Formula for the score is weighted by the title, first sentence, and the entire review
        compound = title_sentiment["compound"] * 0.5 + first_sentence_sentiment["compound"] * 0.3 + review_sentiment["compound"] * 0.2
        mean_compound = mean_compound + compound
        # As compound can be from [-0.5, 0.5], if the score falls between the middle 30%, it will be considered as a neutral review
        if compound > 0.15:
            positive_reviews.append(review)
        elif compound < -0.15:
            negative_reviews.append(review)
        else:
            neutral_reviews.append(review)
    mean_compound = mean_compound / (1.0 * len(movie_reviews))
    return mean_compound, positive_reviews, negative_reviews, neutral_reviews


def skip_unwanted(pos_tuple):
    word, tag = pos_tuple
    # Omits stopwords and non-alphabet words
    if not word.isalpha() or word.lower() in unwanted:
        return False
    if tag.startswith("NN"):
        return False
    return True


def get_words(positive_reviews, negative_reviews):
    positive_words_list = [word for sentence in positive_reviews for word in sentence.split()]
    positive_words = [word for word, tag in filter(
        skip_unwanted,
        nltk.pos_tag(positive_words_list)
    )]

    negative_words_list = [word for sentence in negative_reviews for word in sentence.split()]
    negative_words = [word for word, tag in filter(
        skip_unwanted,
        nltk.pos_tag(negative_words_list)
    )]

    positive_fd = nltk.FreqDist(positive_words)
    negative_fd = nltk.FreqDist(negative_words)
    # Remove words present in both positive and negative lists
    common_set = set(positive_fd).intersection(negative_fd)
    for word in common_set:
        del positive_fd[word]
        del negative_fd[word]

    top_100_positive = {word for word, count in positive_fd.most_common(100)}
    top_100_negative = {word for word, count in negative_fd.most_common(100)}

    sia = SentimentIntensityAnalyzer()

    positive_words_output = []
    for word in top_100_positive:
        sentiment_score = sia.polarity_scores(word)
        if sentiment_score['compound'] > 0.30:
            positive_words_output.append(word)

    negative_words_output = []
    for word in top_100_negative:
        sentiment_score = sia.polarity_scores(word)
        if sentiment_score['compound'] < -0.30:
            negative_words_output.append(word)
    return positive_words_output[:5], negative_words_output[:5]


def transpose_score(score):
    return (score + 0.5) * 10


def analyze_movie(movie_id, num_reviews):
    movie_reviews = get_reviews(movie_id, num_reviews)
    score, positive_reviews, negative_reviews, neutral_reviews = get_movie_sentiments(movie_reviews)
    positive_words, negative_words = get_words(positive_reviews, negative_reviews)
    json_string = {
        "score": transpose_score(score),
        "num_positive_reviews": len(positive_reviews),
        "num_neutral_reviews": len(neutral_reviews),
        "num_negative_reviews": len(negative_reviews),
        "positive_words": positive_words,
        "negative_words": negative_words
    }
    return json.dumps(json_string)


# NECESSARY TO DO WHEN RUNNING FOR THE FIRST TIME
if __name__ == '__main__':
    nltk.download('stopwords')
    nltk.download('names')
    nltk.download('vader_lexicon')
    nltk.download('averaged_perceptron_tagger')
