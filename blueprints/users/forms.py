from flask_wtf import FlaskForm
from wtforms.fields.simple import EmailField, FileField, PasswordField, StringField, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Length, DataRequired


##########################################################################################################################################
class SignUpForm(FlaskForm):
    """A form for a user to sign up for an account"""
    
    username = StringField('Username', validators=[InputRequired(), Length(max=15)])
    
    email = EmailField('Email', validators=[InputRequired()])

    password = PasswordField('Password', validators=[Length(min=5, max=32), 
                                                     InputRequired(), 
                                                     EqualTo('confirm', 
                                                             message='Passwords must match.'),
                                                     DataRequired('Required')
                                                     ])
    
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])


##########################################################################################################################################
class LoginForm(FlaskForm):
    """A form for logging in a user"""
    
    email = EmailField('Email', validators=[InputRequired()])

    password = PasswordField('Password', validators=[InputRequired(),])
    
    
##########################################################################################################################################
    
class ReverifyEmailForm(FlaskForm):
    """A form for reverifying an email"""
    
    email = EmailField('Email', validators=[InputRequired()])
    
    
##########################################################################################################################################

class EditPasswordForm(FlaskForm):
    """A form to change password via *edit account* """
    
    password = PasswordField('Old password', validators=[Length(min=5, max=32), 
                                                     InputRequired(),
                                                     DataRequired('Required')
                                                     ])
    
    new_password = PasswordField('New password', validators=[Length(min=5, max=32), 
                                                     InputRequired(), 
                                                     EqualTo('new_password_confirm', 
                                                             message='Passwords must match.'),
                                                     DataRequired('Required')
                                                     ])
    
    new_password_confirm = PasswordField('Confirm new password', validators=[Length(min=5, max=32), 
                                                        InputRequired(), 
                                                        DataRequired('Required')
                                                        ])
    
    
##########################################################################################################################################

class EditPasswordEmailForm(FlaskForm):
    """A form to change password via *edit account* """
    
    new_password = PasswordField('New password', validators=[Length(min=5, max=32), 
                                                     InputRequired(), 
                                                     EqualTo('new_password_confirm', 
                                                             message='Passwords must match.'),
                                                     DataRequired('Required')
                                                     ])
    
    new_password_confirm = PasswordField('Confirm new password', validators=[ 
                                                        InputRequired(), 
                                                        DataRequired('Required')
                                                        ])
    
    
##########################################################################################################################################

class EditProfileForm(FlaskForm):
    """A form to edit the account via account settings page"""
    
    profile_image = FileField('Upload Profile Image')

    username = StringField('Username', validators=[InputRequired(), Length(max=30)])
    
    bio = TextAreaField('About me', validators=[Length(max=450)])
    
    
##########################################################################################################################################
   
class DeleteAccountForm(FlaskForm):
    """A form to delete account"""
    
    delete = StringField()
    

##########################################################################################################################################

class ReportUserForm(FlaskForm):
    """A form to report users. """
    
    report_message = TextAreaField('Reason:', validators=[InputRequired(), Length(max=300)])
    

##########################################################################################################################################