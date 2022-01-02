import os, warnings
from re import S
from unittest import TestCase
from app import app
from gamehunter.db import db
from blueprints.users.models import User
from blueprints.games.models import Games



os.environ['DATABASE_URL'] = "postgresql:///gamehunters_db_test"

db.drop_all()

class GamesViewsTestCase(TestCase):
    """Tests the GamesHunter Games Views."""


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
        
    
    def test_game_home_page(self):
        """Tests the index page of the Game module."""

        ### Tests when NOT logged in
        resp = self.client.get('/games', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        self.login_for_test()
        
        resp = self.client.get('/games', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
       
    
    
    def test_game_details_page(self):
        """Tests the Game Details page."""

        ### Tests when NOT logged in
        resp = self.client.get('/games/12020', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('<b>Developers</b>', html)
        
        ### Tests when logged in
        self.login_for_test()
        
        resp = self.client.get('/games/12020', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('<b>Developers</b>', html)
        
    
    
    def test_search_results(self):
        """Tests the Endpoint for the Games Search Query."""

        resp = self.client.get('/games/search/call+of+duty')
        
        self.assertTrue(resp.status_code == 200)
        
    
    def test_user_game_favorites_add(self):
        """Tests adding a Game to User favorites."""

        ### Tests when NOT logged in
        resp = self.client.get('/games/favorites/add')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', json)

        ### Tests when logged in
        self.login_for_test()
        
        resp = self.client.get('/games/favorites/add', query_string={'game_id':'12020'})
        json = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Game successfully added to your favorites.', json)
        
        ### Tests adding an already added game
        resp = self.client.get('/games/favorites/add', query_string={'game_id':'12020'})
        json = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You already have this game in your favorites.', json)
    
    
    def test_user_game_favorites_remove(self):
        """Tests removing a Game from User favorites."""

        ### Tests when NOT logged in
        resp = self.client.get('/games/favorites/remove')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', json)
        
        ### Tests when logged in
        self.login_for_test()
        
        resp = self.client.get('/games/favorites/remove', query_string={'game_id':'12020'})
        json = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Game successfully removed from your favorites.', json)