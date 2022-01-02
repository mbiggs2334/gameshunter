import os, warnings
from unittest import TestCase
from flask import g
from app import app
from gamehunter.db import db
from blueprints.users.models import Conversation, User, Message


os.environ['DATABASE_URL'] = "postgresql:///gamehunters_db_test"

db.drop_all()

class ForumViewTestCase(TestCase):
    """Tests the GamesHunter Forum Views."""


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
        u3 = User.signup('testUser3', 'test3@testuser.com', 'HASHED_PASSWORD')
        u1.email_confirmed = True
        u2.email_confirmed = True
        u3.email_confirmed = True
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        with app.app_context():
            g.user = u1
            Conversation.start_new_conversation(other_user = u2)
            Message.new_message(sent_by=1, sent_to=2, convo_id=1, content='hello')
        
        
        
    
    
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

    def login_for_test_3rd_user(self):
        """Logs a user into the test enviornment"""
        self.client.post('/users/login',
                        data = dict(email="test3@testuser.com", password="HASHED_PASSWORD", form='')
                        )
        
        
    
    def test_index_page(self):
        """Tests the home page of the Direct Messages blueprint."""

        ### Tests when NOT logged in
        resp = self.client.get('/messages', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        self.login_for_test()
        
        resp = self.client.get('/messages', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('hello', html)
        self.assertIn('testUser2', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    
    def test_conversation_page(self):
        """Tests the Conversation_page endpoint."""

        ### Tests when NOT logged in
        resp = self.client.get('/messages/conversation/1', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when user is not in Conversation
        self.login_for_test_3rd_user()
        
        resp = self.client.get('/messages/conversation/1', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Access unautorized. You are not a part of this conversation.', html)
        self.assertIn('testUser3', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')

        ### Tests when logged in and in Conversation
        self.login_for_test()
        
        resp = self.client.get('/messages/conversation/1', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('hello', html)
        self.assertIn('testUser2', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        

    
    def test_start_new_conversation(self):
        """Tests the endpoint to start a new Conversation between users."""

        ### Tests when NOT logged in
        resp = self.client.get('/messages/conversation/1/new', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests for already existing conversation
        self.login_for_test_2nd_user()
        
        resp = self.client.get('/messages/conversation/1/new', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You already have a conversation with testUser1.', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        ### Tests when logged in
        self.login_for_test_3rd_user()
        
        resp = self.client.get('/messages/conversation/1/new', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        convo = Conversation.query.get_or_404(2)
        self.assertTrue(resp.status_code == 200)
        self.assertIsInstance(convo, Conversation)
        self.assertTrue(convo.started_by == 3)