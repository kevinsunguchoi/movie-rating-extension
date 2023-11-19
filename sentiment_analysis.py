import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

unwanted = nltk.corpus.stopwords.words("english")
unwanted.extend([w.lower() for w in nltk.corpus.names.words()])


def get_reviews(url):
    movie_reviews = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    reviews = soup.find_all('div', class_='text show-more__control')
    for review in reviews:
        print(review.get_text())
        movie_reviews.append(review.get_text())
    return movie_reviews


def get_movie_sentiments(text_reviews):
    mean_compound = 0
    positive_reviews = []
    negative_reviews = []
    sia = SentimentIntensityAnalyzer()
    for text_review in text_reviews:
        sentiment = sia.polarity_scores(text_review)
        mean_compound = mean_compound + sentiment["compound"]
        if sentiment["compound"] > 0:
            positive_reviews.append(text_review)
        else:
            negative_reviews.append(text_review)
    mean_compound = mean_compound / (1.0 * len(text_reviews))
    return mean_compound, positive_reviews, negative_reviews


def skip_unwanted(pos_tuple):
    word, tag = pos_tuple
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

    #TODO - need to adjust thresholds to output how many words for each sentiment
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
    return positive_words_output, negative_words_output


if __name__ == '__main__':
    # sample URL, we should move this to another method for us to call in the pyscript
    url = 'https://www.imdb.com/title/tt0111161/reviews'
    movie_reviews = get_reviews(url)
    score, positive_reviews, negative_reviews = get_movie_sentiments(movie_reviews)
    positive_words, negative_words = get_words(positive_reviews, negative_reviews)
