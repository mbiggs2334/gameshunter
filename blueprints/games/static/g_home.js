// Prevents CSS transitions from happening immediately on page load
$(document).ready(function () {
    $(".css-transitions-only-after-page-load").each(function (index, element) {
        setTimeout(function () { $(element).removeClass("css-transitions-only-after-page-load") }, 10);
    });
});

let gameForm = document.getElementById('game-search');
let searchInput = document.getElementById('game-search-input');
let curSearch = document.getElementById('user-search');
let curSearchDiv = document.getElementById('user-search-div');
let noResDiv = document.getElementById('no-results-div');
let noRes = document.getElementById('no-results');

// Adds an event listener to the form that then reaches out to an api for search results and displays them on the page.
gameForm.addEventListener('submit', e => {
    e.preventDefault();
    searchInput.value.trim();
    if(searchInput.value === ''){
        return
    };
    getRawgRequest(searchInput.value);
});

// Reaches out to an internal endpoint
async function getRawgRequest(searchTerm){
    const resp = await axios.get(`${window.location.href}/search/${searchTerm}`);
    $("[data-game-cont='game-container']").remove();
    searchInput.value = '';
    if(resp.data.results.length === 0){
        curSearchDiv.classList.add('d-none');
        noResDiv.classList.remove('d-none');
        noRes.innerText = searchTerm;
        return
    }
    noResDiv.classList.add('d-none')
    curSearch.innerText = searchTerm;
    curSearchDiv.classList.remove('d-none')
    generateMarkup(resp);
};

// Generates markup for API response and appends it to the page
function generateMarkup(data){
    for(let game of data.data.results){
        if(game.background_image === null){
             game.background_image = 'https://gamehunter.s3.us-east-2.amazonaws.com/static/images/default-image.jpg'
        }
        $('#all-games').append(`
        <div id='${game.id}' data-game-cont='game-container'  class='light-round-all css-transitions-only-after-page-load shadow m-3 px-0 overflow-hidden'>
                                <div style="background-image: url('${game.background_image}');
                                background-position: center;
                                background-size: cover; min-height: 400px; max-height: 400px;
                                min-width: 285px; max-width: 285px" 
                                class='shadow h-100'>
                                    <div id='hide-' class='css-transitions-only-after-page-load black-half h-100 position-relative px-md-3 px-1 py-3' >
                                        <div class='d-flex justify-content-end flex-column align-items-center h-100'>
                                            <div class=''>
                                                <h1 style='font-size: 2rem;' class='w-100 text-center text-light m-0 p-0 mb-2'>${game['name']}</h1>
                                            </div>
                                            <div class='align-self-center'>
                                                <a class='btn-outline-light btn btn-sm mb-1' href="/games/${game.id}">Game Details</a>
                                                <form method='POST' action='/forum/post/new/${game.id}' class='text-center mb-4'>
                                                    <input type="hidden" name='name' value='${game.name}'>
                                                    <input type="hidden" name='background_image' value='${game.background_image}'>
                                                    <input type="hidden" name='release_date' value='${game.released}'>
                                                    <button class='btn-outline-light btn btn-sm m-0' href="/games/news/${game.id}">Talk about it</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
        `);
    };
};
