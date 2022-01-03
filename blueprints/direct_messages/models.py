from flask import redirect, flash
from gamehunter.db import db
from app import socketio
from flask_socketio import join_room, leave_room
from blueprints.users.models import Message

##########################################################################################################################################

@socketio.on('user_typing')
def user_typing(data):
    """Listens for a User typing and will Emit a response of which User is currently typing to the other User."""

    room = data['channel']
    socketio.emit('is_typing', data, room=room)


##########################################################################################################################################

@socketio.on('message')
def handle_message(data):
    """Listens for a message sent by a User and Emits a response to the connected sockets containing that message.
    
    Will also create a new Message object and commit it to the Database."""

    room = data['channel']
    message_sent = Message.new_message(sent_by=data['gUserId'],sent_to=data['otherUserId'], convo_id=room, content=data['message'])
    if message_sent:
        socketio.emit('response', data, room=room)
    else:
        flash('Something went wrong. Please try again later.', 'danger')
        return redirect(f'/messages/conversation/{room}')
    
    
##########################################################################################################################################
    
@socketio.on('join')
def user_join_room(data):
    """Listens for when a user opens a Direct Message from another User and opens a Live Chat room for that particular conversation."""

    channel = data['channel']
    join_room(channel)


##########################################################################################################################################
 
@socketio.on('disconnect')
def user_leave_room(data):
    """Listens for when a user leaves the Direct Message conversation and removes them from the Live Chat room."""

    channel = data['channel']
    leave_room(channel)

##########################################################################################################################################

@socketio.on('user_active')
def user_is_active(data):
    messages = Message.query.filter(Message.sent_by_id==data['otherUser'],
                                    Message.sent_to_id==data['user'],
                                    Message.seen_by_user==False).all()
    
    for message in messages:
        message.seen_by_user = True
        db.session.add(message)
    db.session.commit()