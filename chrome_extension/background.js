// function receiver(request, sender, sendResponse) {
//     window.movie_name = request.name
//     window.review = request.review
//     window.url = request.url
// }

// chrome.runtime.onMessage.addListener(receiver)

console.log("hello")

// chrome.tabs.onUpdated.addListener((tabId, tab) => {
//     console.log(tab.url)
//     if(tab.url && tab.url.includes("imdb.com/title")) {
//         const queryParameters = tab.url.split("/")[2]
//         console.log(queryParameters)
//     }
// })

// chrome.browserAction.onClicked.addListener(buttonClicked);

// function buttonClicked(tab) {
//     console.log(tab)
//     let msg = {
//         text: "hello"
//     }
//     chrome.tabs.sendMessage(tab.id, msg)
// }


// "default_popup": "movie_rating.html",