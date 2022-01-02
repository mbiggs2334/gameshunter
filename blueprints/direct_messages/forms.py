from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class SendMessageForm(FlaskForm):
    """A form for sending Direct Messages from one user to another.
    
    Contains only a single 'StringField' named 'content'."""
    content = StringField('Send a message...', validators=[InputRequired(), Length(max=500)])