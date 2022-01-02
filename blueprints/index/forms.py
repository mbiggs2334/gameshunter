from flask_wtf import FlaskForm
import flask_wtf
from wtforms import EmailField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired, Length

##########################################################################################################################################

class Feedback_Report_Form(FlaskForm):
    """Form for the Feedback/Report section of the Support web application."""

    email = EmailField('Your Email Address', validators=[InputRequired()])

    info = TextAreaField('Details', validators=[InputRequired(), Length(max=500)])
    

##########################################################################################################################################