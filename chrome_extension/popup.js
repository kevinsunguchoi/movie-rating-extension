// Initialize local backend url for Flask app
var backend_url = "http://127.0.0.1:5001/" // Change this variable to match the local url the Flask app runs on
var backend_post_url = backend_url + "process_data"

// Variable for movie id
var movie_id = ""

function getMovieInfo() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        var currentTab = tabs[0];
        var tabUrl = currentTab.url;

        if (!tabUrl.includes("imdb.com")) {
            document.getElementById('imdb').style.display = 'none'

            var wrong_page = document.createElement('div')
            wrong_page.id = "wrong-page"
            var wrong_page_message = document.createElement('h3')
            wrong_page_message.textContent = "This website does not seem to be an IMDB website. Please use the IMDB website to use this extension. Thank you!"

            wrong_page.appendChild(wrong_page_message)

            document.getElementById('main-container').appendChild(wrong_page)
        }
        var url = tabUrl + "reviews";
        movie_id = tabUrl.split("/")[4];
        var movie_name = currentTab.title.split("-")[0];

        // Update HTML elements
        document.getElementById("movie-name-v").textContent = movie_name;

        // Set the value next to input range to show number of reviews as the slider changes
        document.getElementById('reviews').oninput = function(){
            document.getElementById('reviews-output').value = document.getElementById('reviews').value;
        }
    })
}

async function sendMovieUrl(id) {
    document.getElementById('generate').textContent = 'Loading...'

    let reviews = String(document.getElementById('reviews-output').value)

    let movie_info = [id, reviews]

    try {
        const response = await fetch(backend_post_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(movie_info),
        });

        console.log(movie_info)

        const result = await response.text();
        console.log('Result from server:', result);

        // After sendMovieUrl is complete, call getData
        getData().then(() => {
            document.getElementById('generate').textContent = "Generate Movie Rating"
            document.getElementById('generate').style.backgroundColor = "#EA4C89"
        });

        

    } catch (error) {
        console.error('Error:', error);
    }
}

function getData() {
    return fetch(backend_url)
    .then(response => response.json())
    .then(data => {
        // Set the score and the number of positive, neutral, and negative words
        document.getElementById("sentiment-score").textContent = String(data['score'].toFixed(2)) + " / 10"
        document.getElementById("positive-reviews").textContent = data['num_positive_reviews']
        document.getElementById("neutral-reviews").textContent = data['num_neutral_reviews']
        document.getElementById("negative-reviews").textContent = data['num_negative_reviews']

        // Create list element for positive words and negative words
        let positive_list = document.getElementById("positive-words")
        positive_list.innerHTML = ""
        let negative_list = document.getElementById("negative-words")
        negative_list.innerHTML = ""

        if (data['positive_words'].length == 0) {
            positive_list.innerHTML = "No Positive Reviews"
        }
        else {
            // Set the list of positive words
            for (i = 0; i < data['positive_words'].length; i++) {
                let li = document.createElement('li')
                li.innerText = data['positive_words'][i]
                positive_list.appendChild(li)
            }
        }
        if (data['negative_words'].length == 0) {
            negative_list.innerHTML = "No Negative Reviews"
        }
        else {
            // Set the list of negative words
            for (i = 0; i < data['negative_words'].length; i++) {
                let li = document.createElement('li')
                li.innerText = data['negative_words'][i]
                negative_list.appendChild(li)
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

//// Run when chrome extension opens
window.onload = getMovieInfo()

// Call to request sentiment analysis from python script
document.addEventListener("DOMContentLoaded", function() {
    // Attach the sendMovieUrl function to the button click event
    document.getElementById("generate").addEventListener("click", function() {
        // Call sendMovieUrl with the desired id
        sendMovieUrl(movie_id);
    });
});
