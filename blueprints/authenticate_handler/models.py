from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

##########################################################################################################################################

class SerializeEmail:
    """Repsonsible for serializing any emails sent to the User to assure validity of User identity."""
    
    ######################################################################################################################################
    
    @classmethod    
    def serialize_confirm_email(self, email):
        """Serializes the confirmation email sent to the user during account creation."""
        
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps(email, salt='confirm-email')
        return token   
        
     ######################################################################################################################################
        
    @classmethod
    def confirm_email(self, token):
        """Validates the confirmation email link sent to the User during account creation."""
        
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            s.loads(token, salt='confirm-email', max_age=900)
        except SignatureExpired:
            return False
        return True
    
    ######################################################################################################################################
    
    @classmethod
    def serialize_pass_reset_email(self, email):
        """Serializes the email sent to the User when a password reset link is requested."""
        
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps(email, salt='pass-reset')
        return token
    
    ######################################################################################################################################
    
    
    @classmethod
    def confirm_email_pass(self, token):
        """Validates the link sent to the User after requesting a password reset."""
        
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            s.loads(token, salt='pass-reset', max_age=900)
        except SignatureExpired:
            return False
        return True
        
    ######################################################################################################################################