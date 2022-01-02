import os, warnings
from unittest import TestCase
from flask import g
from app import app
from gamehunter.db import db
from blueprints.users.models import User



os.environ['DATABASE_URL'] = "postgresql:///gamehunters_db_test"

db.drop_all()

class IndexViewTestCase(TestCase):
    """Tests the GamesHunter Index Views."""


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
        db.session.add(u1)
        db.session.add(u2)
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
    
    
    
    def test_index_home(self):
        """Tests the GamesHunter home page."""

        ### Tests when NOT logged in.

        resp = self.client.get('/')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Popular Games', html)
        self.assertIn('Active Posts', html)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Popular Games', html)
        self.assertIn('Active Posts', html)
    
    
    
    def test_privacy_policy_page(self):
        """Tests the Privacy Policy Page."""

        ### Tests when NOT logged in.

        resp = self.client.get('/privacypolicy')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', html)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/privacypolicy')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', html)
        
    
    
    def test_tos_page(self):
        """Tests the Terms of Service Page."""

        ### Tests when NOT logged in.

        resp = self.client.get('/privacypolicy')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Vivamus laoreet a ex a tincidunt.', html)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/privacypolicy')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Vivamus laoreet a ex a tincidunt.', html)
        
    
    def test_support_page(self):
        """Tests the Support Page."""

        ### Tests when NOT logged in.

        resp = self.client.get('/support')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Feedback', html)
        self.assertIn('FAQ', html)
        self.assertIn('Report', html)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/support')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Feedback', html)
        self.assertIn('FAQ', html)
        self.assertIn('Report', html)
        
    
    
    def test_faq_page(self):
        """Tests the FAQ Page."""

        ### Tests when NOT logged in.

        resp = self.client.get('/faq')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('How do I make a forum post?', html)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/faq')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('How do I make a forum post?', html)
        
    
    
    def test_feedback_page(self):
        """Tests the Feedback page."""

        ##### Tests when NOT logged in.
        
        ### Tests GET reqeust 
        
        resp = self.client.get('/feedback')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Having some thoughts?', html)

        ### Tests POST request
        
        resp = self.client.post('/feedback',data=dict(email='test@testuser.com',
                                                       info='BananaNutMuffin.'),
                                            follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("received your submission. Thank you.", html)
        
        ##### Tests when logged in.
        self.login_for_test()
        
        ### Tests GET reqeust 
        
        resp = self.client.get('/feedback')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Having some thoughts?', html)

        ### Tests POST request
        
        resp = self.client.post('/feedback',data=dict(email='test@testuser.com',
                                                       info='BananaNutMuffin.'),
                                            follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn("received your submission. Thank you.", html)
        
        

def test_report_page(self):
        """Tests the Report page."""

        ##### Tests when NOT logged in.
        
        ### Tests GET reqeust 
        
        resp = self.client.get('/report')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Having an issue?', html)

        ### Tests POST request
        
        resp = self.client.post('/report',data=dict(email='test@testuser.com',
                                                       info='BananaNutMuffin.'),
                                            follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("received your submission. Thank you.", html)
        
        ##### Tests when logged in.
        self.login_for_test()
        
        ### Tests GET reqeust 
        
        resp = self.client.get('/report')
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Having an issue?', html)

        ### Tests POST request
        
        resp = self.client.post('/report',data=dict(email='test@testuser.com',
                                                       info='BananaNutMuffin.'),
                                            follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn("received your submission. Thank you.", html)