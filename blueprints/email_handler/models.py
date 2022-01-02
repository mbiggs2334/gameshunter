from flask import url_for, g, session
from app import mail
from flask_mail import Message
from blueprints.authenticate_handler.models import SerializeEmail
import datetime


##########################################################################################################################################

class MailHandler:
    """The MailHandler class handles sending emails either to users or internal support staff."""

    @classmethod
    def send_confirmation_email(self, email):
        """Sends an account confirmation link to the email specified during account
        creation. """
        
        token = SerializeEmail.serialize_confirm_email(email)
        
        msg = Message('GamesHunter account confirmation', sender='gamehunter@gmail.com', recipients=[email])
    
        link = url_for('authenticate_bp.authenticate_email', token=token, _external=True)

        msg.body = f"""Thanks for registering. Please click the link below to complete your registration. If you are not expecting this email, please disregard. This link will expire in 30 minutes.

                    {link}"""
                    
        try:
            mail.send(msg)
        except:
            return False
        return True
    
    
##########################################################################################################################################
    
    @classmethod
    def send_password_reset_email(self, email):
        """Sends a password reset email to the email specified """
        
        token = SerializeEmail.serialize_pass_reset_email(email)
        
        msg = Message('GamesHunter Password Reset', sender='gamehunter@gmail.com', recipients=[email])

        link = url_for('authenticate_bp.authenticate_email_pass', token=token, _external=True )

        msg.body = f"""Please click the link below to reset your password. If you did not request this, please disregard.
        
                    {link}"""

        try: 
            mail.send(msg)
        except:
            return False
        return True
    
    
##########################################################################################################################################
        
    @classmethod
    def send_report_email(self, msg_content=None, reported_user_email=None):
        """Sends an email containing information from a User report via the report button on a User profile."""
        
        msg = Message('Reported User', sender='gameshunter@gmail.com', recipients=['gamehunters2334@gmail.com'])

        msg.body = f"""Reported User Email: {reported_user_email}
                        
                        Reported By: {g.user.email}

                        Reported: {datetime.datetime.utcnow()}
                        
                        Reason: {msg_content}"""
        
        session.pop('reportMessage')
        try: 
            mail.send(msg)
        except:
            return False
        return True
    
    
##########################################################################################################################################

    @classmethod
    def send_feedback_or_report_email(self, email=None, content=None, channel=None):
        """Sends an email containing information from User Feedback/Reports via the Support section of the web app.
        """
        msg = Message(f'User {channel}', sender='gameshunter@gmail.com', recipients=['gamehunters2334@gmail.com'])
        
        msg.body = f"""User email: {email}

                        Message: {content}"""

        session.pop('email')
        session.pop('content')
        session.pop('channel')
        try:
            mail.send(msg)
        except:
            return False
        
        return True
    
    
##########################################################################################################################################