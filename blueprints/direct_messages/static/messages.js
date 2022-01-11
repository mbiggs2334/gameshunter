let messageDiv = document.getElementById("message-box");
messageDiv.scrollTop = messageDiv.scrollHeight;

let conversationRoom = document.getElementById('conversation').value;
let chatInput = document.querySelector('#content');
chatInput.focus();


let gUserId = document.querySelector('#g-user-id').value;
let gUserUsername = document.querySelector('#g-user-username').value;
let otherUserId = document.querySelector('#other-user-id').value;
let otherUserUsername = document.querySelector('#other-user-username').value;

//Connects to the IO Socket
let chatSocket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

//Tells the server to place the User in the specified room, which happens to be the Conversation ID in this case.
chatSocket.on('connect', () => {
    chatSocket.emit('join', {channel : conversationRoom, user: gUserId});
});

//Adds an event listener to the Message Input field. Tells the Socket to send the Message off to the server along with User information.
document.querySelector('form').addEventListener('submit', e => {
    e.preventDefault();
    chatSocket.emit('message', {
        gUserId,
        sentBy: gUserUsername,
        otherUserId,
        sentTo: otherUserUsername,
        message : document.querySelector('#content').value,
        channel : conversationRoom
    });
    document.querySelector('#content').value = '';
});


//Listens for a ping for the server marked as an incoming message, then appends the message to the DOM
chatSocket.on('response', msg => {
    if(msg.sentBy === gUserUsername){
            $('#message-box').append(`<div class="row m-0 p-0 message">
            <div class='d-inline-flex justify-content-end align-items-end flex-column'>
                <span class='primary fw-bold fs-5 mb-1'>@${msg.sentBy}</span>
                <p class='primary text-break m-0 text-end'>${msg.message}</p>
                </div>
            </div>`);
    } else {
        $('#message-box').append(`<div class="row m-0 p-0 message align-items-center">
        <div class='d-inline-flex justify-content-start align-items-start flex-column'>
            <span class='secondary fw-bold fs-5 mb-1'>@${msg.sentBy}</span>
            <p class='secondary text-break m-0'>${msg.message}</p>
            </div>
        </div>`)};
    messageDiv.scrollTop = messageDiv.scrollHeight;
});

//Adds an event listener to the Message input and emits a ping on the chat socket that a user is currently typing, when user input is detected
chatInput.addEventListener('input', (e) => {
    chatSocket.emit('user_typing', {
        username : gUserUsername,
        channel : conversationRoom
    });
});

//Listens for a ping from server that a user in the room is currently typing and appends a Message on the DOM of who is currently typing
//also sets off a Timeout function to remove the 'who is typing' message
chatSocket.on('is_typing', data => {
    let typer = document.getElementById('typer');
    if(!typer){
        if(data.username !== gUserUsername){
            $('#user-typing').append(`<span id='typer' class='text-light'>${data.username} is typing...</span>`);
            typingTimeouts();
        };
    };
});

//function to clear the typing timeout function if it exists, else it runs the *removeTyper* function
function typingTimeouts(){
    if(typingTimeout){
        clearTimeout(typingTimeout);
        var typingTimeout = null;
    }
    var typingTimeout = setTimeout(removeTyper, 1000);
}

//Removes the 'who is typing' message from the DOM
function removeTyper() {
    $('#typer').remove();
    var typingTimeout = null;
};


//sets the User's active status to null on page load
let activePing = null;

//If the User is marked as active, a ping is sent via the ChatSocket to let the server know the User is currently active every 30 seconds
//Sets the active status of the User to Inactive every 30 seconds
let activeInterval = setInterval(() => {
    if(activePing !== null){
        chatSocket.emit('user_active', {channel: conversationRoom, user: gUserId, otherUser: otherUserId});
    };
    activePing = null;
}, 30000);

//Sets the User status to active on mousemove
window.addEventListener('mousemove', () => {
    if(activePing !== 'active'){
        activePing = 'active';
    };
});

//Sets the User status to active on screen touch
window.addEventListener('touchmove', () => {
    if(activePing !== 'active'){
        activePing = 'active';
    };
});