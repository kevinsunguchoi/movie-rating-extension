chrome.runtime.onMessage.addListener(receiver)

window.movie_name = "Not an IMDb Website"

function receiver(request, sender, sendResponse) {
    window.movie_name = request.name
    window.review = request.review
    window.url = request.url
}