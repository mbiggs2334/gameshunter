from flask import session, redirect, flash, Markup, g
from .models import MailHandler
from ...blueprints.users.models import User
from ...blueprints.blueprints import email_handler_bp

##########################################################################################################################################

@email_handler_bp.route('/confirm/send')
def send_confirmation_email():
    """Endpoint to send the confirmation email to the email specified by the user."""
    
    if 'email' not in session:
        flash(Markup("Need another verification email? Please click '<a href='/users/login/verify' class='link-light'>Having trouble logging in?</a>' on the main <a class='link-light' href='/users/login'>login</a> page."), 'info')
        return redirect('/')
    email = session['email']
    mail_sent = MailHandler.send_confirmation_email(email)
    if mail_sent:
        flash('Thanks for registering. You will recieve an email shortly containing a link to verify your account.', 'success')
        return redirect('/')
    else:
        flash(Markup('Something went wrong. Please try again by re-entering you email <a href="/users/login/verify" class="link-light">here</a>.'), 'danger')
        return redirect('/')


##########################################################################################################################################
    
@email_handler_bp.route('/confirm/resend')
def resend_confirmation_email():
    """Route to send the confirmation email to the email specified by the user."""
    if 'email' not in session:
        flash(Markup("Need another verification email? Please click '<a href='/users/login/verify' class='link-light'>Having trouble logging in?</a>' on the main <a class='link-light' href='/users/login'>login</a> page."), 'central-blue')
        return redirect('/')
    email = session['email']
    mail_sent = MailHandler.send_confirmation_email(email)
    if mail_sent:
        flash('If there is an account associated with this email address, you will receive a verification link shortly.', 'central-blue')
        return redirect('/')
    else:
        flash(Markup('Something went wrong. Please try again by re-entering you email <a href="/users/login/verify" class="link-light">here</a>.'), 'danger')
        return redirect('/')  


##########################################################################################################################################
    
@email_handler_bp.route('/resetpassword')
def send_reset_password_email():
    """Route to send a password to resent email
    Will not send link if associated account does not exist in the DB
    """
    if 'email' not in session:
        flash(Markup("Need to reset your password? Please click '<a href='/users/forgotpassword' class='link-light'>Forgot password?</a>' on the main <a class='link-light' href='/users/login'>login</a> page."), 'central-blue')
        return redirect('/')
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if user:
        mail_sent = MailHandler.send_password_reset_email(email)
        if mail_sent:
            flash('If there is an account associated with this email address, a reset link will be sent.', 'central-blue')
            return redirect('/')
        else:
            flash('Something went wrong. Please try again later.', 'danger')
            return redirect('/')
    else:     
        flash('If there is an account associated with this email address, a reset link will be sent.', 'central-blue')
        return redirect('/')


##########################################################################################################################################

@email_handler_bp.route('/report/<int:user_id>')
def send_report_email(user_id):
    """Endpoint to send an email about a User reported User via User profile. """
    if not g.user:
        flash('You need to be logged in to do that.', 'danger')
        return redirect('/')
    reported_user = User.query.get_or_404(user_id)
    report_message = session.get('reportMessage')
    mail_sent = MailHandler.send_report_email(msg_content=report_message, reported_user_email=reported_user.email)
    if mail_sent:
        flash("Report submitted successfully. We'll take a look into the matter, thank you!", 'success')
        return redirect('/')
    else:
        flash("Something went wrong. Please try again later.", 'danger')
        return redirect(f'/users/{user_id}/profile')
    
    
##########################################################################################################################################
    
@email_handler_bp.route('/feedbackreport')
def send_feedback_report_email():
    """Endpoint to send an email to support staff about User reported issues or feedback via the Support page."""
    mail_sent = MailHandler.send_feedback_or_report_email(email=session.get('email'), content=session.get('content'), channel=session.get('channel'))
    if mail_sent:
        flash(f"We've received your submission. Thank you.", 'success')
        return redirect('/support')
    else:
        flash('Something went wrong. Please try again later.', 'danger')
        return redirect('/support')
    

##########################################################################################################################################