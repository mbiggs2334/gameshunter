let comments = document.querySelectorAll('[data-comment]');
for (let comment of comments){
    comment.addEventListener('click', e => {
        if(e.target.dataset['plusComment']){
            upvoteComment(e, comment.id);
        }
        if(e.target.dataset['minusComment']){
            downvoteComment(e, comment.id);
        };
        if(e.target.dataset['editComment']){
            editComment(e, comment.id);
        };
        if(e.target.type === 'submit'){
            postCommentChange(comment.id);
        };
        if(e.target.type === ""){
            window.location.href = e.target.href;
        };
    });
};



$('#user-post-controls').mouseenter(() => {
    $('#user-post-controls-arrow').removeClass('fa-chevron-left');
    $('#user-post-controls-arrow').addClass('fa-chevron-right');
    document.getElementById('user-post-controls').style.transform = 'translateX(0px)';
}).mouseleave(() => {
    $('#user-post-controls-arrow').removeClass('fa-chevron-right');
    $('#user-post-controls-arrow').addClass('fa-chevron-left');
    document.getElementById('user-post-controls').style.transform = 'translateX(80px)';
});



$("textarea").each(function () {
    this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
    }).on("input", function () {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});
let textArea = document.querySelector('textarea')
    textArea.style.resize = 'vertical';
    textArea.style.maxHeight = '500px';
    textArea.style.whiteSpace = 'pre-wrap';



async function upvoteComment(event, id){
    let counter = event.target.nextElementSibling;
    let originalValue = parseInt(counter.innerText);
    if($(`#${id} #minus-comment`).hasClass('red-text')){
        counter.innerText = parseInt(counter.innerText) + 1;
    };
    if($(`#${id} #plus-comment`).hasClass('central-blue-text')){
        alreadyUpvotedComment(id, originalValue, counter);
    } else {
        freshUpvotedComment(id, originalValue, counter);
    };
};


async function alreadyUpvotedComment(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) - 1;
        $(`#${id} #plus-comment`).removeClass('central-blue-text');
        $(`#${id} #minus-comment`).removeClass('red-text');
        resp = await axios.get(`https://${window.location.host}/forum/comment/${id}/like/remove`);
        $('#flashed_message').remove();
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                            <div class='text-center'>
                                                ${resp.data.message}
                                            </div>
                                            </div>`);
            counter.innerText = originalValue
            $(`#${id} #plus-comment`).addClass('central-blue-text');
        };
};

async function freshUpvotedComment(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) + 1;
        $(`#${id} #plus-comment`).addClass('central-blue-text');
        $(`#${id} #minus-comment`).removeClass('red-text');
        resp = await axios.get(`https://${window.location.host}/forum/comment/${id}/like/add`);
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                            <div class='text-center'>
                                                ${resp.data.message}
                                            </div>
                                            </div>`);
            counter.innerText = originalValue
            $(`#${id} #plus-comment`).removeClass('central-blue-text');
        };
};

async function downvoteComment(event, id){
    let counter = event.target.previousElementSibling;
    let originalValue = parseInt(counter.innerText);
    if($(`#${id} #plus-comment`).hasClass('central-blue-text')){
        counter.innerText = parseInt(counter.innerText) - 1;
    }
    if($(`#${id} #minus-comment`).hasClass('red-text')){
        alreadyDownVotedComment(id, originalValue, counter);
    } else {
        freshDownVoteComment(id, originalValue, counter);
    };
};

async function alreadyDownVotedComment(id, originalValue, counter){
    counter.innerText = parseInt(counter.innerText) + 1;
    $(`#${id} #minus-comment`).removeClass('red-text');
    $(`#${id} #plus-comment`).removeClass('central-blue-text');
    resp = await axios.get(`https://${window.location.host}/forum/comment/${id}/dislike/remove`);
    $('#flashed_message').remove();
    if (resp.data.category === 'danger'){
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
        counter.innerText = originalValue;
        $(`#${id} #minus-comment`).addClass('red-text');
    };
};

async function freshDownVoteComment(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) - 1;
        $(`#${id} #minus-comment`).addClass('red-text');
        $(`#${id} #plus-comment`).removeClass('central-blue-text');
        resp = await axios.get(`https://${window.location.host}/forum/comment/${id}/dislike/add`);
        $('#flashed_message').remove();
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                            <div class='text-center'>
                                                ${resp.data.message}
                                            </div>
                                            </div>`);
        counter.innerText = originalValue;
        $(`#${id} #minus-comment`).removeClass('red-text');
        };
};



document.getElementById('post-counter').addEventListener('click', e => {
    e.preventDefault();
    let postId =  document.getElementById('post-counter').dataset.post;
    if(e.target.dataset['plusPost']){
        upvotePost(e, postId);
    };
    if(e.target.dataset['minusPost']){
        downvotePost(e, postId);
    };
});



async function upvotePost(event, id){
    let counter = event.target.nextElementSibling;
    let originalValue = parseInt(counter.innerText);
    if($('#minus-post').hasClass('red-text')){
        counter.innerText = parseInt(counter.innerText) + 1;
    };
    if($('#plus-post').hasClass('central-blue-text')){
        counter.innerText = parseInt(counter.innerText) - 1;
        $('#plus-post').removeClass('central-blue-text');
        $('#minus-post').removeClass('red-text');
        resp = await axios.get(`https://${window.location.host}/forum/post/${id}/like/remove`);
        $('#flashed_message').remove();
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
            counter.innerText = originalValue;
            $('#plus-post').addClass('central-blue-text');
        };
    } else {
        counter.innerText = parseInt(counter.innerText) + 1;
        $('#plus-post').addClass('central-blue-text');
        $('#minus-post').removeClass('red-text');
        resp = await axios.get(`https://${window.location.host}/forum/post/${id}/like/add`);
        $('#flashed_message').remove();
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
            counter.innerText = originalValue;
            $('#plus-post').removeClass('central-blue-text');
        };
    };
};



async function downvotePost(event, id){
    let counter = event.target.previousElementSibling;
    let originalValue = parseInt(counter.innerText);
    if($('#plus-post').hasClass('central-blue-text')){
        counter.innerText = parseInt(counter.innerText) - 1;
    }
    if($('#minus-post').hasClass('red-text')){
        counter.innerText = parseInt(counter.innerText) + 1;
        $('#minus-post').removeClass('red-text');
        $('#plus-post').removeClass('central-blue-text');
        resp = await axios.get(`https://${window.location.host}/forum/post/${id}/dislike/remove`);
        $('#flashed_message').remove();
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                            <div class='text-center'>
                                                ${resp.data.message}
                                            </div>
                                            </div>`);
        counter.innerText = parseInt(counter.innerText) - 1;
        $('#minus-post').addClass('red-text');
        };
    } else {
        let counter = event.target.previousElementSibling;
        counter.innerText = parseInt(counter.innerText) - 1;
        $('#minus-post').addClass('red-text');
        $('#plus-post').removeClass('central-blue-text');
        resp = await axios.get(`https://${window.location.host}/forum/post/${id}/dislike/add`);
        $('#flashed_message').remove();
        if (resp.data.category === 'danger'){
            $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                            <div class='text-center'>
                                                ${resp.data.message}
                                            </div>
                                            </div>`);
        counter.innerText = originalValue;
        $('#minus-post').removeClass('red-text');
        };
    };
};



let commentBox = document.getElementById('comment-box');
let rmvCmntBtn = document.getElementById('remove-comment-btn');

commentBox.addEventListener('click', e => {
    e.preventDefault();
    if(e.target.dataset['removeBtn']){
        removeComment(e);
    };
});

function removeComment(event){
        let commentId = event.target.dataset['commentId']
        rmvCmntBtn.href = `/forum/post/${event.target.dataset['removeBtn']}/comment/remove/${commentId}`;
};



function editComment(event, id){
    let commentText;
    let pTag;
    if(event.target.type === undefined){
        pTag = event.target.parentElement.parentElement.parentElement.parentElement.parentElement.children[2];
        commentText = pTag.innerText;
    } else {
        pTag = event.target.parentElement.parentElement.parentElement.parentElement.children[2];
        commentText = pTag.innerText;
    }
    editCommentDomChangesPrePost(id, commentText, pTag);
};



function editCommentDomChangesPrePost(id, commentText, pTag){
    $(pTag).remove();
    $(`#${id} #comment-info`).append(`
    <form style='z-index: 999;' id='edit-comment-form' action method='POST'>
        <div class='input-group shadow-sm mb-1'>
            <input id='comment-input' value="${commentText}" type='text' class='form-control border border-dark' />
            <button type='submit' class='border border-dark btn btn-sm btn-primary'>Save Changes</button>
            <input id='old-comment-text' type='hidden' value="${commentText}" />
        </div>
    </form>`);
    $(`#${id} #edit-comment-btn`).remove();
    $(`#${id} #comment-button-box`).prepend(`<div id='remove-comment-edit' class='d-inline'>
                                                <a href="#"  class='m-0 d-inline  btn btn-sm btn-danger border border-dark' title='Cancel edit'><i class="fs-5 fas fa-times m-0"></i></a>
                                            </div>`);
    $(`#${id} #remove-comment-edit`).on('click', () => {
        removeEditCommentForm(id, pTag);
    });
};



function removeEditCommentForm(id, pTag){
    $(`#${id} #remove-comment-edit`).remove();
    $(`#${id} #comment-button-box`).prepend(`<div id='edit-comment-btn' class='d-inline'>
    <a href="#" data-edit-comment='#' class='d-inline btn btn-sm btn-primary border border-dark' title='Edit comment'><i data-edit-comment='#' class="far fa-edit"></i></a>
    </div>`);
    $(`#${id} #edit-comment-form`).remove();
    $(`#${id} #comment-info`).append(pTag);
};



async function postCommentChange(id){
    content = $(`#${id} #comment-input`).val()
    resp = await axios.post(`https://${window.location.host}/forum/comment/${id}/edit?content=${content}`);
    let oldText = $(`#${id} #old-comment-text`).val()
    removeEditCommentForm(id);
    $('#flashed_message').remove();
    if(resp.data.category){
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                    <div class='text-center'>
                                        ${resp.data.message}
                                    </div>
                                    </div>
                                    `);
        $(`#${id} #comment-info`).append(`<p class='text-break'>${oldText}<p>`);
    } else {
        $(`#${id} #comment-info`).append(`<p class='text-break'>${resp.data.content}<p>`);
    };
};