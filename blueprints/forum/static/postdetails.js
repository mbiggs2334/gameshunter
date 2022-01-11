let comments = document.querySelectorAll('[data-comment]');
//Adds event listenerss to all comments on the post
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

//creates Axios Instance
const axiosWithCookies = axios.create({
    withCredentials = true
});

//Manipulates the User Post controls to change DOM position
$('#user-post-controls').mouseenter(() => {
    $('#user-post-controls-arrow').removeClass('fa-chevron-left');
    $('#user-post-controls-arrow').addClass('fa-chevron-right');
    document.getElementById('user-post-controls').style.transform = 'translateX(0px)';
}).mouseleave(() => {
    $('#user-post-controls-arrow').removeClass('fa-chevron-right');
    $('#user-post-controls-arrow').addClass('fa-chevron-left');
    document.getElementById('user-post-controls').style.transform = 'translateX(80px)';
});


//Auto adjust scroll height on TextArea input detection
$("textarea").each(function () {
    this.setAttribute("style", "height:" + (this.scrollHeight) + "px;overflow-y:hidden;");
    }).on("input", function () {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

//Sets the maximum height on TextArea input
let textArea = document.querySelector('textarea')
    textArea.style.resize = 'vertical';
    textArea.style.maxHeight = '500px';
    textArea.style.whiteSpace = 'pre-wrap';


//Parent function for upvoting a comment
//Sets off two child functions depending on weather the User has already upvoted or downvoted a comment
async function upvoteComment(event, id){
    let counter = event.target.nextElementSibling;
    let originalValue = parseInt(counter.innerText);

    //for if the user has already downvoted the comment
    //changes the front end 'like' counter to immediately reflect changes
    if($(`#${id} #minus-comment`).hasClass('red-text')){
        counter.innerText = parseInt(counter.innerText) + 1;
    };

    //for if the User has already upvoted the comment
    if($(`#${id} #plus-comment`).hasClass('central-blue-text')){
        alreadyUpvotedComment(id, originalValue, counter);
    } else {

    //for if the User hasn't upvvoted or downvoted the comment
        freshUpvotedComment(id, originalValue, counter);
    };
};

//Child function for "upvoteComment"
//Function for if the User has already upvoted the comment. Takes the Comment ID, the original value of the likes on the comment, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has removed their 'like' from the comment
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function alreadyUpvotedComment(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) - 1;
        $(`#${id} #plus-comment`).removeClass('central-blue-text');
        $(`#${id} #minus-comment`).removeClass('red-text');
        resp = await axiosWithCookies.get(`https://${window.location.host}/forum/comment/${id}/like/remove`);
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

//Child function for "upvoteComment"
//Function for if the User has NOT already upvoted the comment. Takes the Comment ID, the original value of the likes on the comment, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has added a 'like' to the comment
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function freshUpvotedComment(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) + 1;
        $(`#${id} #plus-comment`).addClass('central-blue-text');
        $(`#${id} #minus-comment`).removeClass('red-text');
        resp = await axiosWithCookies.get(`https://${window.location.host}/forum/comment/${id}/like/add`);
        $('#flashed_message').remove();
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


//Parent function for downvoting a comment
//Sets off two child functions depending on weather the User has already upvoted or downvoted a comment
async function downvoteComment(event, id){
    let counter = event.target.previousElementSibling;
    let originalValue = parseInt(counter.innerText);

    //for if the user has already upvoted a comment
    //changes the front end 'like' counter to immediately reflect changes
    if($(`#${id} #plus-comment`).hasClass('central-blue-text')){
        counter.innerText = parseInt(counter.innerText) - 1;
    }

    //for if the User has already downvoted the comment
    if($(`#${id} #minus-comment`).hasClass('red-text')){
        alreadyDownVotedComment(id, originalValue, counter);
    } else {

    //for if the User has not downvoted the comment
        freshDownVoteComment(id, originalValue, counter);
    };
};

//Child function for "downvoteComment"
//Function for if the User has already downvoted the comment. Takes the Comment ID, the original value of the likes on the comment, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has removed their 'dislike' from the comment
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function alreadyDownVotedComment(id, originalValue, counter){
    counter.innerText = parseInt(counter.innerText) + 1;
    $(`#${id} #minus-comment`).removeClass('red-text');
    $(`#${id} #plus-comment`).removeClass('central-blue-text');
    resp = await axiosWithCookies.get(`https://${window.location.host}/forum/comment/${id}/dislike/remove`);
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

//Child function for "downvoteComment"
//Function for if the User has NOT downvoted the comment. Takes the Comment ID, the original value of the likes on the comment, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has added a 'dislike' to the comment
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function freshDownVoteComment(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) - 1;
        $(`#${id} #minus-comment`).addClass('red-text');
        $(`#${id} #plus-comment`).removeClass('central-blue-text');
        resp = await axiosWithCookies.get(`https://${window.location.host}/forum/comment/${id}/dislike/add`);
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


//Adds event listeners to the Post 'like' Counter
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


//Parent function for upvoting the post
//Sets off two child functions depending on weather the User has already upvoted or downvoted the post
async function upvotePost(event, id){
    let counter = event.target.nextElementSibling;
    let originalValue = parseInt(counter.innerText);

    //for if the User has already upvoted the post
    //changes the front end 'like' counter to immediately reflect changes
    if($('#minus-post').hasClass('red-text')){
        counter.innerText = parseInt(counter.innerText) + 1;
    };

    //for if the User already upvoted the post
    if($('#plus-post').hasClass('central-blue-text')){
        alreadyUpvotedPost(id, originalValue, counter);
    } else {

    //for if the User NOT upvoted the post
        freshUpvotedPost(id, originalValue, counter);
    };
};

//Child function for "upvotePost"
//Function for if the User has upvoted the post. Takes the Post ID, the original value of the likes on the post, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has removed a 'like' to the post
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function alreadyUpvotedPost(id, originalValue, counter){
        counter.innerText = parseInt(counter.innerText) - 1;
        $('#plus-post').removeClass('central-blue-text');
        $('#minus-post').removeClass('red-text');
        resp = await axiosWithCookies.get(`https://${window.location.host}/forum/post/${id}/like/remove`);
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
};

//Child function for "upvotePost"
//Function for if the User has NOT upvoted the post. Takes the Post ID, the original value of the likes on the post, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has added a 'like' to the post
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function freshUpvotedPost(id, originalValue, counter){
    counter.innerText = parseInt(counter.innerText) + 1;
        $('#plus-post').addClass('central-blue-text');
        $('#minus-post').removeClass('red-text');
        resp = await axiosWithCookies.get(`https://${window.location.host}/forum/post/${id}/like/add`);
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


//Parent function for downvoting the post
//Sets off two child functions depending on weather the User has already upvoted or downvoted the post
async function downvotePost(event, id){
    let counter = event.target.previousElementSibling;
    let originalValue = parseInt(counter.innerText);
    if($('#plus-post').hasClass('central-blue-text')){
        counter.innerText = parseInt(counter.innerText) - 1;
    }
    if($('#minus-post').hasClass('red-text')){
       
    } else {
       
    };
};

//Child function for "downvotePost"
//Function for if the User has already downvoted the post. Takes the Post ID, the original value of the likes on the post, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has removed their 'dislike' from the post
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function alreadyDownVotedPost(id, originalValue, counter){
    counter.innerText = parseInt(counter.innerText) + 1;
    $('#minus-post').removeClass('red-text');
    $('#plus-post').removeClass('central-blue-text');
    resp = await axiosWithCookies.get(`https://${window.location.host}/forum/post/${id}/dislike/remove`);
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
};

//Child function for "downvotePost"
//Function for if the User has NOT downvoted the post. Takes the Post ID, the original value of the likes on the post, and the 'like' counter DOM object
//Makes the appropriate DOM changes and tells the server that the User has added a 'dislike' to the post
//Reverts back to previous standing if receives an error from server and appends a message to the DOM letting the User know
async function freshDownVotedPost(id, originalValue, counter){
    counter.innerText = parseInt(counter.innerText) - 1;
    $('#minus-post').addClass('red-text');
    $('#plus-post').removeClass('central-blue-text');
    resp = await axiosWithCookies.get(`https://${window.location.host}/forum/post/${id}/dislike/add`);
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


let commentBox = document.getElementById('comment-box');
let rmvCmntBtn = document.getElementById('remove-comment-btn');

//Adds an event listener to the DIV holding the comments, listens for a specific DOM element being clicked
commentBox.addEventListener('click', e => {
    e.preventDefault();
    if(e.target.dataset['removeBtn']){
        removeComment(e);
    };
});

//Grabs the Comment ID and changes the Remove Comment button route to reflect which comment is being removed
//Button will only be availble for the comments owner
function removeComment(event){
        let commentId = event.target.dataset['commentId']
        rmvCmntBtn.href = `/forum/post/${event.target.dataset['removeBtn']}/comment/remove/${commentId}`;
};


//Function that grabs the comment information and passes it to the "editCommentDomChangesPrePost" function
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


//removes the comment <p> tag and appends a form to edit the comment, as well as trading the original 'edit comment' button for a 'cancel edit' button
//adds an event listener to the new 'cancel edit' button that runs a function on click
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
    
    //adds event listener to new 'cancel edit' button
    $(`#${id} #remove-comment-edit`).on('click', () => {
        removeEditCommentForm(id, pTag);
    });
};


//removes all the added DOM objects for editing a comment and returns it to it's original state
function removeEditCommentForm(id, pTag){
    $(`#${id} #remove-comment-edit`).remove();
    $(`#${id} #comment-button-box`).prepend(`<div id='edit-comment-btn' class='d-inline'>
    <a href="#" data-edit-comment='#' class='d-inline btn btn-sm btn-primary border border-dark' title='Edit comment'><i data-edit-comment='#' class="far fa-edit"></i></a>
    </div>`);
    $(`#${id} #edit-comment-form`).remove();
    $(`#${id} #comment-info`).append(pTag);
};


//grabs the new comment information and POSTs it to the server
//removes the 'edit comment' DOM objects and appends the newly edited comment if it receives no error from server
async function postCommentChange(id){
    let content = $(`#${id} #comment-input`).val()
    resp = await axiosWithCookies.post(`https://${window.location.host}/forum/comment/${id}/edit?content=${content}`);
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