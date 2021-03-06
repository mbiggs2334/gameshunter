#
# Initiates the app and sets configurations
#

from gamehunter import create_app, db
app = create_app()

from flask_socketio import SocketIO
from flask_mail import Mail
from flask import session, g
from flask_cors import CORS
from flask_moment import Moment
from datetime import timedelta
import datetime, threading
import gevent

CORS(app)
moment = Moment(app)
mail = Mail(app)
socketio = SocketIO(app=app, async_mode='gevent')


### Imports blueprints
from blueprints.blueprints import authenticate_bp, message_bp, index_bp, email_handler_bp, forum_bp, games_bp, news_bp, users_bp
 
### Registers blueprints
app.register_blueprint(authenticate_bp)
app.register_blueprint(message_bp)
app.register_blueprint(email_handler_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(games_bp)
app.register_blueprint(news_bp)
app.register_blueprint(index_bp)
app.register_blueprint(users_bp)

from blueprints.users.models import User
@app.before_request
def add_user_to_global():
    """Adds user to flask global if logged in"""
    if 'curr_user' in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=24)
        session.modified = True
        now = datetime.datetime.utcnow()
        g.user = User.query.get_or_404(session['curr_user'])
        g.user.active = True
        g.user.last_active = now
        db.session.commit()
        
    else:
        g.user = None

from blueprints.users.functions import update_user_active_status
threading.Timer(3.0, lambda: update_user_active_status).start()

# Starts SocketIO.
if __name__ == '__main__':
    socketio.run(app)