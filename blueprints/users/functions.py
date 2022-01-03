from flask import flash, g, session
from ...gamehunter.db import db
from datetime import datetime
from .models import User
import threading
from sqlalchemy import and_

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

def update_user_active_status():
    threading.Timer(150.0, lambda: update_user_active_status()).start()
    five_min_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    users = User.query.filter(and_(User.last_active < five_min_ago, User.active == True)).all()
    if(len(users) > 0):
        for user in users: 
            user.active = False
            db.session.add(user)
        db.session.commit()
        

##########################################################################################################################################