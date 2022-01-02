import os, warnings
from re import S
from unittest import TestCase
from flask import g
from app import app
from gamehunter.db import db
from blueprints.users.models import User
from blueprints.games.models import Games



os.environ['DATABASE_URL'] = "postgresql:///gamehunters_db_test"

db.drop_all()

class GamesModelTestCase(TestCase):
    """Tests the GamesHunter Games Model methods."""



    @classmethod
    def setUpClass(self):
        """Creates test client, adds sample data."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        db.create_all()
        
        User.query.delete()
        
        self.client = app.test_client()
        
        u1 = User.signup('testUser1', 'test@testuser.com', 'HASHED_PASSWORD')
        u2 = User.signup('testUser2', 'test2@testuser.com', 'HASHED_PASSWORD')
        u1.email_confirmed = True
        u2.email_confirmed = True
        
        new_game = Games(rawg_id=12020, title='Left 4 Dead 2')
        
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(new_game)
        db.session.commit()
        
        
    
    
    @classmethod
    def tearDownClass(self):
        db.drop_all()
        app.config['TESTING'] = False
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = True
        
        
    def setUp(self):
        warnings.filterwarnings(action="ignore",
                                message="unclosed",
                                category=ResourceWarning)
        warnings.filterwarnings(action="ignore",
                                message="unclosed",
                                category=DeprecationWarning)
        
        
        
    def tearDown(self):
        self.client.get('/users/logout')
        warnings.filterwarnings(action="ignore",
                                message="unclosed",
                                category=ResourceWarning)
        warnings.filterwarnings(action="ignore",
                                message="unclosed",
                                category=DeprecationWarning)
    
    
    
    def login_for_test(self):
        """Logs a user into the test enviornment"""
        self.client.post('/users/login',
                        data = dict(email="test@testuser.com", password="HASHED_PASSWORD", form='')
                        )
        
        
    def login_for_test_2nd_user(self):
        """Logs a user into the test enviornment"""
        self.client.post('/users/login',
                        data = dict(email="test2@testuser.com", password="HASHED_PASSWORD", form='')
                        )
        
    
    def test_check_for_game_in_db(self):
        """Tests the check_for_game_in_db method on the Games Model."""
        
        ### Checks for existing Game
        is_game = Games.check_for_game_in_db(game_id=12020)
        
        self.assertTrue(is_game)
        
        ### Checks for non-existing Game
        is_game = Games.check_for_game_in_db(game_id=15480)
        
        self.assertFalse(is_game)
    
    
    def test_create_new_game(self):
        """Tests the create_new_game method on the Games Model."""

        ### Create game with all parameters entered
        new_game = Games.create_new_game(rawg_id=123, title='bananas',
                                         background_img='null', release_date='12/12/2021')
        
        self.assertTrue(new_game)
        
        ### Create game with missing parameter entered
        new_game = Games.create_new_game(rawg_id=456,
                                         background_img='null', release_date='12/12/2021')
        
        self.assertFalse(new_game)

