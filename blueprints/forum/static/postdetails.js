let comments = document.querySelectorAll('[data-comment]');
for (let comment of comments){
    comment.addEventListener('click', e => {
        e.preventDefault;
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
            postCommentChange(comment.id)
        }
    });
};

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
    resp = await axios.get(`http://${window.location.host}/forum/comment/${id}/like`);
    if (resp.data.message === 'Add Successful.') {
        let counter = event.target.nextElementSibling;
        event.target.remove();
        $(`#${id}-counter-box`).prepend(`<i data-minus-comment='minus-upvote' class="fas fa-minus fs-5"></i>`);
        counter.innerText = parseInt(counter.innerText) + 1;
    };
    if (resp.data.category === 'danger'){
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
    };
};

async function downvoteComment(event, id){
    resp = await axios.get(`http://${window.location.host}/forum/comment/${id}/unlike`);
    if (resp.data.message === 'Remove Successful.') {
        let counter = event.target.nextElementSibling;
        event.target.remove();
        $(`#${id}-counter-box`).prepend(`<i data-plus-comment='plus-upvote' class="fas fa-plus fs-5"></i>`);
        counter.innerText = parseInt(counter.innerText) - 1;
    };
    if (resp.data.category === 'danger'){
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
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
    resp = await axios.get(`http://${window.location.host}/forum/post/${id}/like`);
    if (resp.data.message === 'Add Successful.') {
        let counter = event.target.previousElementSibling;
        event.target.remove();
        $(`#post-counter`).append(`<i data-minus-post='minus-upvote' class="fas fa-minus fs-5"></i>`);
        counter.innerText = parseInt(counter.innerText) + 1;
    }
    if (resp.data.category === 'danger'){
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
    };
};

async function downvotePost(event, id){
    resp = await axios.get(`http://${window.location.host}/forum/post/${id}/unlike`);
    if (resp.data.message === 'Remove Successful.') {
        let counter = event.target.previousElementSibling;
        event.target.remove();
        $(`#post-counter`).append(`<i data-plus-post='plus-upvote' class="fas fa-plus fs-5"></i>`);
        counter.innerText = parseInt(counter.innerText) - 1;
    }
    if (resp.data.category === 'danger'){
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                        <div class='text-center'>
                                            ${resp.data.message}
                                        </div>
                                        </div>`);
    };
};

let commentBox = document.getElementById('comment-box');
let rmvCmntBtn = document.getElementById('remove-comment-btn');

commentBox.addEventListener('click', e => {
    e.preventDefault();
    if(e.target.dataset['removeBtn']){
        removeComment(e);
    }
});


function removeComment(event){
    if(event.target.type !== undefined){
        let commentId = event.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id;
        rmvCmntBtn.href = `/forum/post/${event.target.dataset['removeBtn']}/comment/remove/${commentId}`;
    } else {
        let commentId = event.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id;
        rmvCmntBtn.href = `/forum/post/${event.target.dataset['removeBtn']}/comment/remove/${commentId}`;
    };
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
}

async function postCommentChange(id){
    content = $(`#${id} #comment-input`).val()
    resp = await axios.post(`http://${window.location.host}/forum/comment/${id}/edit?content=${content}`);
    let oldText = $(`#${id} #old-comment-text`).val()
    removeEditCommentForm(id);
    if(resp.data.category){
        $('#flashed_message').remove();
        $('#flashed_messages').append(`<div id='flashed_message' class="border-bottom border-dark alert alert-${resp.data.category} m-0">
                                    <div class='text-center'>
                                        ${resp.data.message}
                                    </div>
                                    </div>
                                    `);
        $(`#${id} #comment-info`).append(`<p class='text-break'>${oldText}<p>`)
    } else {
        $('#flashed_message').remove();
        $(`#${id} #comment-info`).append(`<p class='text-break'>${resp.data.content}<p>`)
    };
};