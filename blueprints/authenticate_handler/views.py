from flask import render_template, redirect, session, flash, g, Markup
from ...blueprints.users.forms import EditPasswordEmailForm
from ...blueprints.users.models import User
from .models import SerializeEmail
from ...gamehunter.db import db
from ...blueprints.users.functions import login
from ...blueprints.blueprints import authenticate_bp

##########################################################################################################################################

@authenticate_bp.route('/emails/<string:token>')
def authenticate_email(token):
    """Checks to make sure the token from the account confirmation email link is valid.
    
    If valid, will change User 'email_confirmed' to True and log the User into the site."""
    if g.user:
        flash("Your account is already verified.", 'danger')
        return redirect('/')
    try:
        SerializeEmail.confirm_email(token)
    except:
        flash(Markup("Looks like the link has expired or was entered incorrectly. Please resubmit another request <a class='link-light' href='/users/login/verify'>here</a>."), 'danger')
        return redirect('/')
    user = User.query.filter(User.email==session['email']).first()
    user.email_confirmed = True
    db.session.add(user)
    db.session.commit()
    login(user)
    session.pop('email')
    flash('Thanks for registering! Your account has been successfully created and confirmed.', 'success')
    return redirect('/')
    

##########################################################################################################################################

@authenticate_bp.route('/password/reset/<string:token>', methods=['GET', 'POST'])
def authenticate_email_pass(token):
    """Accepts both a GET and Post request.
    
    A GET request will validate the token sent to the User after a requested Password Reset email.
    Upon a valid token the user will be directed to a form to submit their new password.
    
    A POST request will take the User's new password and store it in the DB."""
    form = EditPasswordEmailForm()
    if form.validate_on_submit():
        password = form.new_password.data
        user = User.query.filter_by(email=session['email']).first()
        session.pop('email')
        if user:
            pass_changed = user.change_password(password)
            if pass_changed:
                flash('Password changed successfully', 'success')
                return redirect('/users/login')
            else:
                flash('Something went wrong. Please try again later.', 'danger')
                return redirect('/')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect('/')
    auth = SerializeEmail.confirm_email_pass(token)
    if not auth:
        flash(Markup("Looks like the link has expired or was entered incorrectly. Please resubmit another request <a class='link-light' href='/users/forgotpassword'>here</a>."), 'danger')
        return redirect('/')
    else:
        return render_template('authenticate_handler/good_confirm_pass.html', form=form)
    

##########################################################################################################################################