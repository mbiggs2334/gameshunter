from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length

##########################################################################################################################################

class NewPostForm(FlaskForm):
    """A form for the User to create a new Post."""

    title = StringField('Title', validators=[InputRequired(),  Length(max=100)])
    
    content = TextAreaField("What's on your mind?", validators=[InputRequired(), Length(max=500)])

##########################################################################################################################################
    
class NewCommentForm(FlaskForm):
    """A form for the User to create a new Comment."""
    
    content = TextAreaField('', name='comment', validators=[InputRequired(), Length(max=350)])

##########################################################################################################################################