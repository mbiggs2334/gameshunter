import os, warnings
from re import A
import unittest
from unittest import TestCase
from flask import g, session
from app import app
from gamehunter.db import db
from blueprints.users.models import User, Follow, Block, FavoriteGames
from blueprints.games.models import Games


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
        Follow.query.delete()
        Block.query.delete()
        FavoriteGames.query.delete()
        
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
        Follow.query.delete()
        Block.query.delete()
        FavoriteGames.query.delete()
        db.session.commit()
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
        
    
    def test_user_signup(self):
        """Tests the User Signup Endpoint."""
        ##### Tests when NOT logged in
        
        ### Tests GET request
        resp = self.client.get('/users/signup', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Register', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)

        ### Tests POST request
        # Tests taken email
        resp = self.client.post('/users/signup', data=dict(username='testUser3',
                                                           email='test@testuser.com',
                                                           password='HASHED_PASSWORD',
                                                           confirm='HASHED_PASSWORD'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Email is already in use. Please make another selection.', html)
        
        # Tests taken username
        resp = self.client.post('/users/signup', data=dict(username='testUser1',
                                                           email='test3@testuser.com',
                                                           password='HASHED_PASSWORD',
                                                           confirm='HASHED_PASSWORD'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('That username is already in use. Please make another selection.', html)
        
        #### SENDS EMAIL ####
        # Tests appropirate register
        # resp = self.client.post('/users/signup', data=dict(username='testUser3',
        #                                                    email='test3@testuser.com',
        #                                                    password='HASHED_PASSWORD',
        #                                                    confirm='HASHED_PASSWORD'), follow_redirects=True)
        # html = resp.get_data(as_text=True)
        
        # self.assertIn('Thanks for registering. You will recieve an email shortly containing a link to verify your account.', html)

        ##### Tests when logged in
        
        ### Tests GET request
        self.login_for_test()
        resp = self.client.get('/users/signup', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You already have an account.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        ### Tests POST request
        self.login_for_test()
        
        resp = self.client.post('/users/signup', data=dict(username='testUser3',
                                                           email='test@testuser.com',
                                                           password='HASHED_PASSWORD',
                                                           confirm='HASHED_PASSWORD'), follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('You already have an account.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    
    def test_user_login(self):
        """Tests the User Login endpoint."""

        ##### Tests when NOT logged in

        ### Tests GET request
        resp = self.client.get('/users/login', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests POST request
        resp = self.client.post('/users/login', data=dict(email='test@testuser.com',
                                                         password='HASHED_PASSWORD'),follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('Welcome back, testUser1!', html)
        self.assertIn('Logout', html)
        self.assertIn('Profile', html)
        
        self.client.get('/users/logout')
        
        ##### Tests when logged in
        
        ### Tests GET request
        self.login_for_test()
        
        resp = self.client.get('/users/login', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You&#39;re already logged in.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        ### Tests POST request
        self.login_for_test()
        
        resp = self.client.post('/users/login', data=dict(email='test@testuser.com',
                                                         password='HASHED_PASSWORD'),follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('You&#39;re already logged in.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    def test_user_logout(self):
        """Tests the User Logout endpoint."""

        ### Tests when NOT logged in
        resp = self.client.get('/users/logout', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('Access unauthorized. You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        self.login_for_test()
        resp = self.client.get('/users/logout', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Successly logged out.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
    def test_user_profile(self):
        """Tests the User Profile endpoint."""

        ### Tests when NOT logged in
        resp = self.client.get('/users/1/profile', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in and unfollowed
        self.login_for_test()
        
        resp = self.client.get('/users/2/profile', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('testUser1', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        self.assertIn('Follow', html)
        
        self.client.get('/users/logout')
        
        ### Tests when logged in and followed
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        with app.app_context():
            g.user = user1
            Follow.create_new_follow(other_user=user2)
            
        self.login_for_test()
        resp = self.client.get('/users/2/profile', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('testUser1', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        self.assertIn('Unfollow', html)
        
        self.client.get('/users/logout')
        
        ### Tests when logged in and blocked
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        with app.app_context():
            g.user = user2
            Block.create_new_block(user=user1)
            
        self.login_for_test()
        resp = self.client.get('/users/2/profile', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Access unauthorized. This user has blocked you.', html)
    
        
    def test_user_profile_edit(self):
        """Tests the Edit User Profile endpoint."""    

        ##### Tests when NOT logged in
        
        ### Tests GET request
        resp = self.client.get('/users/1/profile/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests POST request
        resp = self.client.post('/users/1/profile/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ##### Tests when logged in
        
        ### Tests GET request
        
        # Tests incorrect profile edit attempt
        self.login_for_test()
        
        resp = self.client.get('/users/2/profile/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Access unauthorized.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        
        # Tests correct profile
        self.login_for_test()
        
        resp = self.client.get('/users/1/profile/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('testUser1', html)
        self.assertIn('test@testuser.com', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        ### Tests POST request
        
        # Tests incorrect profile edit attempt
        self.login_for_test()
        
        resp = self.client.post('/users/2/profile/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Access unauthorized.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        # Tests correct profile
        resp = self.client.post('/users/1/profile/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('testUser1', html)
        self.assertIn('test@testuser.com', html)
        self.assertIn('Logout', html)
        
    
    def test_resend_verify_email(self):
        """Tests the endpoint that resends a verification email."""
    
        ##### Tests when NOT logged in
        
        ### Tests GET request
        resp = self.client.get('/users/login/verify', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Verify Email', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)

        ### Tests POST request
        
        # Tests already verified email
        resp = self.client.post('/users/login/verify', data=dict(email='test@testuser.com') ,follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('If there is an account associated with this email address, you will receive a verification link shortly.', html)

        #### SENDS EMAIL ####
        ## Tests unverified email
        # User.signup('testUserVerify', 'verify@testuser.com', 'HASHED_PASSWORD')
        
        # resp = self.client.post('/users/login/verify', data=dict(email='verify@testuser.com') ,follow_redirects=True)
        # html = resp.get_data(as_text=True)
        
        # self.assertIn('If there is an account associated with this email address, you will receive a verification link shortly.', html)

        ## Tests non-existing email
        resp = self.client.post('/users/login/verify', data=dict(email='NotAnEmail@fake.com') ,follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('If there is an account associated with this email address, you will receive a verification link shortly.', html)


    
    def test_edit_password(self):
        """Tests the Edit Password endpoint."""

        ##### Tests when NOT logged in
        
        ### Test GET request
        resp = self.client.get('/users/account/password/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests POST request
        resp = self.client.post('/users/account/password/edit', data=dict(password='HASHED_PASSWORD',
                                                                         new_password='HASHED_PASSWORD2') ,follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ##### Tests when logged in
        
        ### Tests GET request
        self.login_for_test_2nd_user()
        
        resp = self.client.get('/users/account/password/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        ### Tests POST request
        # Tests INCORRECT password
        resp = self.client.post('/users/account/password/edit', data=dict(password='HASHED_PASSWORD_FALSE',
                                                                         new_password='HASHED_PASSWORD2',
                                                                         new_password_confirm='HASHED_PASSWORD2') ,follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Invalid credentials. Please assure you&#39;ve entered the information correctly.', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        # Tests CORRECT password
        resp = self.client.post('/users/account/password/edit', data=dict(password='HASHED_PASSWORD',
                                                                         new_password='HASHED_PASSWORD2',
                                                                         new_password_confirm='HASHED_PASSWORD2') ,follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Password successfully changed!', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
    
    
    def test_forgot_password(self):
        """Tests the Forgot Password endpoint."""
        
        ### Tests GET request
        resp = self.client.get('/users/forgotpassword', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('Reset Password', html)
        self.assertIn('Send Email', html)
        
        ### Tests POST request
        #### SENDS EMAIL ####
        # resp = self.client.post('/users/forgotpassword', data=dict(email='test@testuser.com'), follow_redirects=True)
        # html = resp.get_data(as_text=True)
        
        # self.assertIn('If there is an account associated with this email address, a reset link will be sent.', html)
        
    
    def test_user_favorites(self):
        """Tests the endpoint for the User Favorites page."""
        ### Adds Game and User Favorite
        Games.create_new_game(rawg_id=12020, title='Left 4 Dead 2')
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        with app.app_context():
            g.user = user1
            FavoriteGames.create_new_favorite(game_id=12020, position=1)

            g.user = user2
            FavoriteGames.create_new_favorite(game_id=12020, position=1)
            
        ##### Tests when NOT logged in

        ### Tests GET request
        resp = self.client.get('/users/1/favorites', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Left 4 Dead 2', html)
        self.assertIn('testUser1', html)
        
        ### Tests POST request
        resp = self.client.post('/users/1/favorites', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Access Unauthorized.', html)
        self.assertIn('Left 4 Dead 2', html)
        self.assertIn('testUser1', html)
        
        ##### Tests when logged in
        
        ### Test GET request
        self.login_for_test()
        
        # Tests own profile
        resp = self.client.get('/users/1/favorites', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Left 4 Dead 2', html)
        self.assertIn('testUser1', html)
        self.assertIn('Save Favorites', html)
        self.assertIn('Remove', html)
        
        # Tests outside profile
        resp = self.client.get('/users/2/favorites', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Left 4 Dead 2', html)
        self.assertIn('testUser1', html)
        self.assertIn('testUser2', html)
        self.assertNotIn('Save Favorites', html)
        self.assertNotIn('Remove', html)
        
    
    def test_block_user(self):
        """Tests the Block User endpoint."""

        ### Tests when NOT logged in
        resp = self.client.get('/users/2/block', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        self.login_for_test()
        
        # Tests self-block attempt
        resp = self.client.get('/users/1/block', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("You shouldn&#39;t block yourself you goober.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        # Tests legitimate block
        resp = self.client.get('/users/2/block', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("You are now blocking this user.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        
        # Tests blocking an already blocked User
        resp = self.client.get('/users/2/block', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("You&#39;re already blocking this user.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        # Tests blocking User A when User B has already been blocked.
        self.login_for_test_2nd_user()
        
        resp = self.client.get('/users/1/block', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("This user is already blocking you.", html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
    
    def test_unblock_user(self):
        """Tests the Unblock User endpoint."""
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        User.signup('testUser5', 'unblock@testuser.com', 'HASHED_PASSWORD')
        with app.app_context():
            g.user = user1
            Block.create_new_block(user=user2)
        
        ### Tests when NOT logged in
        resp = self.client.get('/users/2/unblock', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        self.login_for_test()
        
        # Tests 'unblocking' yourself
        resp = self.client.get('/users/1/unblock', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("You aren&#39;t blocking yourself.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        # Tests unblocking User
        resp = self.client.get('/users/2/unblock', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("User unblocked.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        # Tests unblocking NOT blocked User
        user3 = User.query.filter_by(email='unblock@testuser.com').first()
        resp = self.client.get(f'/users/{user3.id}/unblock', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn("You haven&#39;t blocked this user.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
    
    def test_user_follow(self):
        """Tests the Follow User endpoint."""

        ### Tests when NOT logged in
        resp = self.client.get('/users/2/follow', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        
        # Tests FOLLOWING a User
        self.login_for_test()
        
        resp = self.client.get('/users/2/follow', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You are now following this user.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        # Tests FOLLOWING an already FOLLOWED User
        resp = self.client.get('/users/2/follow', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You are already following this user.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    def test_user_unfollow(self):
        """Tests the Unfollow User endpoint."""
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        User.signup('unfollowUser', 'unfollow@testuser.com', 'HASHED_PASSWORD')
        with app.app_context():
            g.user = user1
            Follow.create_new_follow(other_user=user2)
            
        ### Tests when NOT logged in
        resp = self.client.get('/users/2/unfollow', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when logged in
        
        # Tests UNFOLLOWING a FOLLOWED User
        self.login_for_test()
        
        resp = self.client.get('/users/2/unfollow', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You are no longer following this user.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        # Tests UNFOLLOWING an already UNFOLLOWED User
        user3 = User.query.filter_by(email='unfollow@testuser.com').first()
        resp = self.client.get(f'/users/{user3.id}/unfollow', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You aren&#39;t following this user.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    def test_delete_account(self):
        """Tests the Account Deletion endpoint."""
        
        ##### Tests when NOT logged in
        
        ### Tests GET request
        resp = self.client.get('/users/account/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests POST request
        resp = self.client.post('/users/account/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ##### Tests when logged in 
        user = User.signup('deleteAccount', 'delete@testuser.com', 'HASHED_PASSWORD')
        user.email_confirmed = True
        db.session.commit()
        self.client.post('/users/login', data=dict(email='delete@testuser.com', password='HASHED_PASSWORD'))

        ### Tests GET request
        resp = self.client.get('/users/account/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('in the box below and hit "Delete Account"', html)
        self.assertIn('deleteAccount', html)
        self.assertIn('Logout', html)
        
        ### Tests POST request
        resp = self.client.post('/users/account/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Account successfully deleted.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        
    def test_report_user(self):
        """Tests the Report User endpoint."""

        ##### Tests when NOT logged in
        
        ### Tests GET request
        resp = self.client.get('/users/2/report', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests POST request
        resp = self.client.post('/users/2/report', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ##### Tests when logged in
        self.login_for_test()
        
        ### Tests GET request
        resp = self.client.get('/users/2/report', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertIn('Please give as many details as possible about the situation', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        #### SENDS EMAIL ####
        ### Tests POST request
        # resp = self.client.post('/users/2/report', data=dict(report_message='oof') ,follow_redirects=True)
        # html = resp.get_data(as_text=True)
        
        # self.assertIn('Report submitted successfully.', html)
        # self.assertIn('testUser1', html)
        # self.assertIn('Logout', html)
        