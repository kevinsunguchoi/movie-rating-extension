// Movie URL of the IMDb Website
let movie_url = window.location.href

let movie_name = document.querySelector('.sc-7f1a92f5-1.benbRT').textContent
let num_reviews = document.querySelector('.sc-bde20123-3.gPVQxL').textContent

let message = {
    url: movie_url,
    name: movie_name,
    review: num_reviews
}

chrome.runtime.sendMessage(message)


// alert([movie_url])