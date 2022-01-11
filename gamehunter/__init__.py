from flask import Flask
from .db import db
import os

def create_app():
    """Creates an app and sets up app config."""
    
    app = Flask(__name__,
                static_folder='../static')
    app.config.from_pyfile('config.cfg')
    
    uri = os.environ.get('DATABASE_URL', 'postgresql:///gamehunters_db')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', app.config['SECRET_KEY'])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.app = app
    db.init_app(app)
    
    return app