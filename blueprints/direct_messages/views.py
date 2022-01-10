from flask import flash, render_template, redirect, g
from blueprints.users.models import User, Conversation, Message
from .forms import SendMessageForm
from blueprints.blueprints import message_bp

##########################################################################################################################################

@message_bp.route('/')
def inbox():
    """Renders the User's Direct Messages Inbox."""
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/users/login')
    return render_template('direct_messages/inbox.html')


##########################################################################################################################################

@message_bp.route('conversation/<int:conv_id>')
def conversation_page(conv_id):
    """Renders the conversation page and marks any unseen messages as seen. """
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/')
    
    conv = Conversation.query.get_or_404(conv_id)
    if g.user.id != conv.started_by and g.user.id != conv.received_by:
        flash('Access unautorized. You are not a part of this conversation.', 'danger')
        return redirect('/')
    
    other_user = Conversation.get_other_user_of_conversation(conv.started_by_user, conv.received_by_user)
    form = SendMessageForm()
    Message.mark_message_as_seen(message_obj=conv.messages)
    
    return render_template('direct_messages/conversation.html', form=form, conversation=conv, other_user=other_user)
    

##########################################################################################################################################

@message_bp.route('/conversation/<int:user_id>/new', methods=['GET', 'POST'])
def start_new_conversation(user_id):
    """Route will take the param User ID and see if there is an existing Conversation already. Will redirect to existing conversation if True,
    Else will create a new Conversation and redirect to the new Conversation message page."""
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/')
    user = User.query.get_or_404(user_id)
    has_convo = Conversation.check_for_existing_conversation(other_user=user)
    if has_convo:
        flash(f'You already have a conversation with {user.username}.', 'danger')
        return redirect(f'/users/{user.id}/profile')
    else:
        new_convo = Conversation.start_new_conversation(other_user=user)
        if new_convo:
            return redirect(f'/messages/conversation/{new_convo.id}')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect(f'/users/{user.id}/profile')