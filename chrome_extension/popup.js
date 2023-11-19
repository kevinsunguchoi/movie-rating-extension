let bgpage = chrome.extension.getBackgroundPage();
let movie_name = bgpage.movie_name
let num_reviews = bgpage.review
let url = bgpage.url

console.log(url)
console.log(url.includes("imdb.com"))

if (url.includes("imdb.com") == true) {
    document.getElementById('generate').addEventListener('click', genRating)
}

function genRating() {
    document.getElementById('movie-h').innerHTML = "Movie Name:"
    document.getElementById('movie-name').innerHTML = movie_name
    document.getElementById('review-h').innerHTML = "Number of Reviews"
    document.getElementById('num-reviews').innerHTML = num_reviews
}
