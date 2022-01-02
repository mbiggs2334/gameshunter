let messageDiv = document.getElementById("message-box");
messageDiv.scrollTop = messageDiv.scrollHeight;

let conversationRoom = document.getElementById('conversation').value;
let chatInput = document.querySelector('#content');
chatInput.focus();


let gUserId = document.querySelector('#g-user-id').value;
let gUserUsername = document.querySelector('#g-user-username').value;
let otherUserId = document.querySelector('#other-user-id').value;
let otherUserUsername = document.querySelector('#other-user-username').value;

let chatSocket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


chatSocket.on('connect', () => {
    chatSocket.emit('join', {channel : conversationRoom, user: gUserId});
});

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



chatSocket.on('response', msg => {
    if(msg.sentBy === gUserUsername){
        $('#message-box').append(`<div class="row m-0 p-0 message">
        <div class='d-inline-flex justify-content-end align-items-end flex-column'>
            <span class='primary fw-bold fs-5 mb-1'>@${msg.sentBy}</span>
            <p class='primary text-break m-0'>${msg.message}</p>
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

chatInput.addEventListener('input', (e) => {
    chatSocket.emit('user_typing', {
        username : gUserUsername,
        channel : conversationRoom
    });
});

chatSocket.on('is_typing', data => {
    let typer = document.getElementById('typer');
    if(!typer){
        if(data.username !== gUserUsername){
            $('#user-typing').append(`<span id='typer' class='text-light'>${data.username} is typing...</span>`);
            typingTimeouts();
        };
    };
});

function typingTimeouts(){
    if(typingTimeout){
        clearTimeout(typingTimeout);
        var typingTimeout = null;
    }
    var typingTimeout = setTimeout(removeTyper, 1000);
}

function removeTyper() {
    $('#typer').remove();
    var typingTimeout = null;
};

let activePing = null;

let activeInterval = setInterval(() => {
    if(activePing !== null){
        chatSocket.emit('user_active', {channel: conversationRoom, user: gUserId, otherUser: otherUserId});
    };
    activePing = null;
}, 30000);

window.addEventListener('mousemove', () => {
    if(activePing !== 'active'){
        activePing = 'active';
    };
});