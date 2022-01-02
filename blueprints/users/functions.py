from flask import flash, render_template, g, session
from .forms import EditPasswordForm
from gamehunter.db import db
from datetime import datetime

##########################################################################################################################################

def verify_password_match(original_pass=None, new_password=None, new_password_confirm=None):
    """Checks the new password aginst the new password verification field to prevent 
    foul play."""
    
    if new_password != new_password_confirm:
        flash('Password must match, please resubmit.', 'danger')
        return False
    
    if original_pass == new_password:
        flash("New password is the old password. Please select another.", 'danger')
        return False
        
    return True

##########################################################################################################################################

def login(user: object):
    """Saves the user in the flask session."""
    
    user.active = True
    db.session.commit()
    session['curr_user'] = user.id
    
    
##########################################################################################################################################
    
def logout():
    """Logs out user by removing from session."""
    
    now = datetime.utcnow()
    g.user.last_active = now
    g.user.active = False
    db.session.commit()
    session.pop('curr_user')
    
    
##########################################################################################################################################