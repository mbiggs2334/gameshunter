from flask import render_template, redirect, session
from .forms import Feedback_Report_Form
from ...blueprints.blueprints import index_bp
from ...blueprints.games.models import Games
from ...blueprints.forum.models import Post

##########################################################################################################################################

@index_bp.route('/')
def home_page():
    """Endpoint for the home page and queries for 4 of the most recently active posts and the 4 games with the most activity."""
    
    posts = Post.query.order_by(Post.last_active.desc()).limit(4)
    
    games = Games.query.order_by(Games.activity.desc()).limit(4)
    
    return render_template('index/index.html', posts=posts, games=games)


##########################################################################################################################################

@index_bp.route('/privacypolicy')
def privacy_policy():
    """Endpoint for the Privacy Policy page"""
    
    return render_template('index/privacy_policy.html')


##########################################################################################################################################

@index_bp.route('/tos')
def terms_of_service():
    """Endpoint for the Terms of Service page."""
    return render_template('index/tos.html')


##########################################################################################################################################

@index_bp.route('/support')
def support_page():
    """Endpoint for the Support page."""
    return render_template('index/support.html')


##########################################################################################################################################

@index_bp.route('/faq')
def faq_page():
    """Endpoint for the FAQ."""

    return render_template('index/faq.html')


##########################################################################################################################################

@index_bp.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    """Endpoint for the Feedback form in the Suppot section of the web app.
    
    Accepts both a GET and POST request.
    
    GET requests will render the Feedback page along with a Form.
    
    POST requests will pass the information into the Flask Session temporarily and redirect to
    an email endpoint to send the information to the Support email."""

    form = Feedback_Report_Form()
    if form.validate_on_submit():
        email = form.email.data
        feedback = form.info.data
        session['email'] = email
        session['content'] = feedback
        session['channel'] = 'Feedback'
        return redirect('/emails/feedbackreport')
    
    return render_template('index/feedback.html', form=form)
    

##########################################################################################################################################

@index_bp.route('/report', methods=['GET', 'POST'])
def report_page():
    """Endpoint for the Report form in the Suppot section of the web app.
    
    Accepts both a GET and POST request.
    
    GET requests will render the Report page along with a Form.
    
    POST requests will pass the information into the Flask Session temporarily and redirect to
    an email endpoint to send the information to the Support email."""
    
    form = Feedback_Report_Form()
    if form.validate_on_submit():
        email = form.email.data
        report = form.info.data
        session['email'] = email
        session['content'] = report
        session['channel'] = 'Report'
        return redirect('/emails/feedbackreport')
    
    return render_template('index/report.html', form=form)
    
   
########################################################################################################################################## 