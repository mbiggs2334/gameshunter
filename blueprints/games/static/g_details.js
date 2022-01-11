// Resizes all images to fit.
let origHeight = 330;
let origWidth = 526;
let images = document.querySelectorAll('[data-img]');
let imgDivs = document.querySelectorAll('.carousel-item')

//appends carousel indicator buttons
for(let i = 1; i < images.length; i++ ){
    $('#carouselIndicatorButtons').append(`<button type="button" data-bs-target="#carouselIndicators" data-bs-slide-to="${i}" aria-label="Slide ${i+1}"></button>
    `)
}

for (let image of images) {
    image.style.objectFit = 'cover';
    image.style.minHeight = origHeight + 'px';
    image.style.maxHeight = origHeight + 'px';
    image.style.width = origWidth + 'px';
};

for(let div of imgDivs){
    div.style.minHeight = origHeight + 'px';
    div.style.maxHeight = origHeight + 'px';
}

let bigGameDeats = document.getElementById('big-game-details');
let smallGameDeats = document.getElementById('small-game-details');
if($(window).width() >= 1200){
    bigGameDeats.classList.remove('d-none');
} else {
    smallGameDeats.classList.remove('d-none')
};



//saves values for form and the form itself
let favForm = document.getElementById('add_favorites_form')
let gameId = document.getElementById('game_id').getAttribute('value');
let gameName = document.getElementById('game_name').getAttribute('value');
let backgroundImage = document.getElementById('background_image').getAttribute('value');
let releaseDate = document.getElementById('release_date').getAttribute('value');


// Adds an event listener to the window and listens for resize. Changes all image heights accordingly.
window.addEventListener('resize', ImageResize);
function ImageResize(){
    let images = document.querySelectorAll('[data-img]');
    let currImage = document.getElementsByClassName('carousel-item active')[0].children[0];
    let newWidth = currImage.width;
    for (let image of images) {
        image.style.minHeight = (origHeight / origWidth) * newWidth + 'px';
        image.style.maxHeight = (origHeight / origWidth) * newWidth + 'px';
    };
    for (let div of imgDivs) {
        div.style.minHeight = (origHeight / origWidth) * newWidth + 'px';
        div.style.maxHeight = (origHeight / origWidth) * newWidth + 'px';
    };
    
};

// Grabs the src of the image clicked on and sends it to the modal image.
let modalImg = document.getElementById('modal-image');
let carouselImages = document.getElementById('carousel-images');
carouselImages.addEventListener('click', e => {
    modalImg.src = e.target.src;
});

// Sends to previous page
let backButton = document.getElementById('backBtn');
backButton.addEventListener('click', () => {
    window.history.go(-1); 
    return false;
});

// Adds an event listenr to the favorites button
favForm.addEventListener('submit', e => {
    e.preventDefault();
    if($('#fav_button').text() === 'Add to Favorites'){
        addFavorites(gameId, gameName, backgroundImage, releaseDate) ;
    };
    if($('#fav_button').text() === 'Remove Favorite'){
        removeFavorites(gameId);
    };
});

//sends game information to server and appends a message to DOM on success or failure of task
//on success it alters the 'Add to Favorites' button to say 'Remove from favorites'
async function addFavorites(id, name, image, rDate){
    resp = await axios.get(`https://${window.location.host}/games/favorites/add?game_id=${id}&game_name=${name}&game_image=${image}&release_date=${rDate}`, { withCredentials: true});
    $('#flashed_message').remove();
    $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                    <div class='text-center'>
                                        ${resp.data.message}
                                    </div>
                                    </div>
                                    `);
    if (resp.data.category == 'success'){
        $('#fav_button').text('Remove Favorite');
        $('#fav_button').removeClass('btn-outline-dark');
        $('#fav_button').addClass('btn-outline-light');
    };
};

//sends game information to server and appends a message to DOM on success or failure of task
//on success it alters the 'Remove from favorites' button to say 'Add to favorites'
async function removeFavorites(id){
    resp = await axios.get(`https://${window.location.host}/games/favorites/remove?game_id=${id}`, { withCredentials: true});
    $('#flashed_message').remove();
    $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                    <div class='text-center'>
                                        ${resp.data.message}
                                    </div>
                                    </div>
                                    `);
    $('#fav_button').text('Add to Favorites');
    $('#fav_button').removeClass('btn-outline-light');
    $('#fav_button').addClass('btn-outline-dark');
};

//reaches out to the sever with the Game Name to see if any News articles from the Steam API can be found
//runs on page load
async function getNews(){
    resp = await axios.get(`https://${window.location.host}/news/${gameName}`, { withCredentials: true});
    if(resp.data.message === 'None'){
        return;
    } else {
    $('#game-page-container').append(`<div class="row">
    <div class="col-sm-11 col-md-10 col-lg-9 col-xl-8 col-xxl-7 col-12 mx-auto dark-gray rounded shadow p-3">
        <div id='news-col'  class="row">
            <div class="col">
                <div id='news-heading' class="row">

                </div>
                <div class="row">
                    <div class='col mx-auto'>
                        <div id='news' class='d-flex flex-wrap'>

                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>`);
    $('#news-heading').append(`<div class="row w-100 mb-2 mx-auto">
    <h1 class='text-center'>News for ${gameName}</h1>
    </div>`);
    for(let story of resp.data.appnews.newsitems){
    $('#news').append(`<div class='w-100'>
                        <a class='link-dark' href="${story.url}">
                            <h5 class='text-truncate'>${story.title}</h5>
                        </a>    
                        <span>By: <b>${story.author}</b></span>
                        <p>${story.contents}</p>
                        </div><hr class='w-100 bg-light border border-light'>`);
                    };
    };
};

window.addEventListener('resize', gameDeatsChange);

//alters the DOM appearance based on the window size
function gameDeatsChange(){
    if($(window).width() >= 1200){
        smallGameDeats.classList.add('d-none');
        bigGameDeats.classList.remove('d-none');

    } else {
        bigGameDeats.classList.add('d-none');
        smallGameDeats.classList.remove('d-none');
    };
};

getNews();