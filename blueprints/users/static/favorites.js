let allDivs = document.querySelectorAll('[data-pos]');
let favForm = document.querySelector('#fav-form')

if(favForm){
    favForm.addEventListener('click', e => {
        if(e.target.id === 'move-up'){
            moveUp(e);
        };
        if(e.target.id === 'move-down'){
            moveDown(e);
        };
        if(e.target.id === 'remove-btn'){
            e.preventDefault();
            removeElement(e);
        };
    });
};

//changes the DOM to move the selected Favorite 'Up' in the order
function moveUp(event){
    let target = event.target.parentElement.parentElement;
    let targetNewPos = parseInt(target.getAttribute('data-pos')) - 1;
    let oldTargetPos = parseInt(target.getAttribute('data-pos'));
    target.dataset['pos'] = targetNewPos;
    target.children[0].value = targetNewPos;
    target.previousElementSibling.dataset['pos'] = oldTargetPos;
    target.previousElementSibling.children[0].value = oldTargetPos;

    let $newUpDivs = $('[data-pos]');
    let sortedDivs = $newUpDivs.sort(sortDivs);

    changeDomDivs(sortedDivs);
};

//changes the DOM to move the selected Favorite 'Down' in the order
function moveDown(event){
    let target = event.target.parentElement.parentElement;
    let targetNewPos = parseInt(target.getAttribute('data-pos')) + 1;
    let oldTargetPos = parseInt(target.getAttribute('data-pos'));
    target.dataset['pos'] = targetNewPos;
    target.children[0].value = targetNewPos;
    target.nextElementSibling.dataset['pos'] = oldTargetPos;
    target.nextElementSibling.children[0].value = oldTargetPos;

    let $newDownDivs = $('[data-pos]');
    let sortedDivs = $newDownDivs.sort(sortDivs);
    changeDomDivs(sortedDivs);
};

//sorts the selected inputs based on the given data position
function sortDivs(a, b){
    return ($(b).data('pos')) < ($(a).data('pos')) ? 1 : -1;    
};

//alters the DOM to refelect the changes to the order of the favorites
function changeDomDivs(sortedArray){
    if(sortedArray.length === 1){
        sortedArray.children('#arrow-box').empty();
    } else {
        //adds the 'move-up' or 'move-down' arrows depending on div position in the order
        sortedArray.children('#arrow-box').empty();
        sortedArray.children('#arrow-box').first().append(`<i id='move-down' class="fs-2 red-text fas fa-arrow-down"></i>`);
        sortedArray.children('#arrow-box').last().append(`<i id='move-up' class="text-info fs-2 fas fa-arrow-up"></i>`);
        sortedArray.children('#arrow-box').not(':first').not(':last').append(`<i id='move-up' class="mb-3 text-info fs-2 fas fa-arrow-up"></i>
        <i id='move-down' class="red-text fs-2 fas fa-arrow-down"></i>`);
    };

    for (let i = 0; i < sortedArray.length; i++){
        sortedArray.children().children('#game-position-header')[i].innerText = i + 1 + '.'
    };

    $('#fav-form').empty();
    $('#fav-form').append(sortedArray);
};

//function to remove the selected game from favorites
//adds a hidden input with game information that will be pushed along with form submission
function removeElement(event){
    let target = event.target.parentElement.parentElement.parentElement.parentElement;
    $('#form-row').append(`<input type='hidden' form='fav-form' value='removed' name='${target.children[0].name}'/>`)
    target.remove();
    let $currDivs = $('[data-pos]');
    changeDomDivs($currDivs);
    changeDataAfterRemoval($currDivs);
};

//changes the 'position' number when a game has been removed from favorites
function changeDataAfterRemoval(Array){
    for (let i = 0; i < Array.length; i++){
        Array[i].dataset['pos'] = i + 1;
        Array[i].children[0].value = i + 1;
    };
};

