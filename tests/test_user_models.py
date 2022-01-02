import os, warnings
from unittest import TestCase
from flask import g, session
from app import app
from gamehunter.db import db
from blueprints.users.models import User, Message, Conversation, Block, Follow, FavoriteGames, PastUsernames
from blueprints.users.forms import EditProfileForm
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
        
        self.client = app.test_client()
        
        u1 = User.signup('testUser1', 'test@testuser.com', 'HASHED_PASSWORD')
        u2 = User.signup('testUser2', 'test2@testuser.com', 'HASHED_PASSWORD')
        u1.email_confirmed = True
        u2.email_confirmed = True
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        with app.app_context():
            g.user = u1
            Conversation.start_new_conversation(other_user=u2)
        
    
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
        
    
    def test_message_model(self):
        """Tests the Message Model methods."""

        ### Tests the new_message method
        message_created = Message.new_message(sent_by=1, sent_to=2, convo_id=1, content='hello')
        
        self.assertTrue(message_created)
        
        message = Message.query.get_or_404(1)
        
        self.assertIsInstance(message, Message)
        
        ### Tests the mark_message_as_seen method
        self.assertTrue(message.seen_by_user == False)
        
        messages = Message.query.all()
        
        Message.mark_message_as_seen(message_obj=messages)
        
        message = Message.query.get_or_404(1)
        
        self.assertTrue(message.seen_by_user == True)
        
    
    
    def test_block_model(self):
        """Tests the Block Model methods."""

        ### Tests the create_new_block method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        
        with app.app_context():
            g.user = user1
            block_created = Block.create_new_block(user=user2)
        
        self.assertTrue(block_created)
        
    
    
    def test_follow_model(self):
        """Tests the Follow Model methods."""
        
        ### Tests the create_new_follow method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        
        with app.app_context():
            g.user = user1
            follow_created = Follow.create_new_follow(other_user=user2)
        
        follow = Follow.query.get_or_404(1)
        self.assertIsInstance(follow, Follow)
        self.assertTrue(follow.user_following_id == 1)
        self.assertTrue(follow.user_being_followed_id == 2)
        
        ## Tests check_if_following method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        
        with app.app_context():
            g.user = user1
            is_following = Follow.check_if_following(other_user=user2)
        
        self.assertTrue(is_following)
        
        ### Tests remove_follow method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        
        with app.app_context():
            g.user = user1
            follow_removed = Follow.remove_follow(other_user=user2)
            is_following = Follow.check_if_following(other_user=user2)
            
        self.assertTrue(follow_removed)
        self.assertFalse(is_following)

        
    def test_user_model(self):
        """Tests the User Model methods."""

        ### Tests the Signup method
        user = User.signup('singupTest', 'signup@test.com', 'HASHED_PASSWORD')
        user_query = User.query.get_or_404(3)

        self.assertIsInstance(user, User)
        self.assertIsInstance(user_query, User)
        
        
        ### Tests the authenticate_user method
        new_user = User.authenticate_user(email='signup@test.com', password='HASHED_PASSWORD')
        user1 = User.authenticate_user(email='test@testuser.com', password='HASHED_PASSWORD')
        user2 = User.authenticate_user(email='test2@testuser.com', password='HASHED_PASSWORD')

        self.assertIsInstance(new_user, User)
        self.assertIsInstance(user1, User)
        self.assertIsInstance(user2, User)
        
    
        ### Tests the check_if_g_user_blocked method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        
        with app.app_context():
            g.user = user2
            is_blocked = User.check_if_g_user_blocked(1)
            self.assertTrue(is_blocked)
            
            g.user = user1
            is_blocked = User.check_if_g_user_blocked(2)
            self.assertFalse(is_blocked)
        
        
        ### Tests check_if_g_user_blocking method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        
        with app.app_context():
            g.user = user2
            is_blocking = User.check_if_g_user_blocking(1)
            self.assertFalse(is_blocking)
            
            g.user = user1
            is_blocking = User.check_if_g_user_blocking(2)
            self.assertTrue(is_blocking)
            
        ### Tests update_user_info method
        user1 = User.query.get_or_404(1)
        
        with app.app_context():
            form = EditProfileForm()
            form.username.data = 'changedUsername'
            form.bio.data = 'Oranges'
            g.user = user1
            with app.test_request_context():
                User.update_user_info(form=form)
                self.assertEqual('changedUsername', g.user.username)
                self.assertEqual('Oranges', g.user.bio)
                
        
        ### Tests change_password method
        user1 = User.query.get_or_404(1)
        new_password = 'NOT_HASHED_PASSWORD'
        user1.change_password(new_password=new_password)

        old_pass_auth = User.authenticate_user(email='test@testuser.com', password='HASHED_PASSWORD')
        new_pass_auth = User.authenticate_user(email='test@testuser.com', password='NOT_HASHED_PASSWORD')

        self.assertTrue(new_pass_auth)
        self.assertFalse(old_pass_auth)
        
        ### Tests delete_account method
        user3 = User.query.get_or_404(3)
        
        with app.app_context():
            g.user = user3
            with app.test_request_context():
                session['curr_user'] = 3
                account_delete = user2.delete_account()
                self.assertTrue(account_delete)
                null = User.query.get(3)
                self.assertEqual(null, None)
            
        
    def test_favorite_game_model(self):
        """Tests the FavoriteGames Model methods."""

        ### Tests the create_new_favorite method
        user1 = User.query.get_or_404(1)
        Games.create_new_game(rawg_id=12020, title='Left 4 Dead 2')
        
        with app.app_context():
            g.user = user1
            favorite_created = FavoriteGames.create_new_favorite(game_id=12020, position=1)
            self.assertTrue(favorite_created)
            
            favorite = FavoriteGames.query.get_or_404(1)
            self.assertIsInstance(favorite, FavoriteGames)
            
        
        ### Tests the check_for_favorite method
        user1 = User.query.get_or_404(1)
        Games.create_new_game(rawg_id=140, title='New Game')
        
        with app.app_context():
            g.user = user1
            in_favorites1 = FavoriteGames.check_for_favorite(game_id=12020)
            in_favorites2 = FavoriteGames.check_for_favorite(game_id=140)

            self.assertTrue(in_favorites1)
            self.assertFalse(in_favorites2)
            
        
            
    def test_conversation_model(self):
        """Tests the Conversation Model methods."""
        User.signup('testUser4', 'test4@testuser.com', 'HASHED_PASSWORD')
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        user3 = User.query.get_or_404(3)
        false_user = User.query.get(4)
        
        ### Tests the start_new_conversation method
        with app.app_context():
            g.user = user1
            convo_started = Conversation.start_new_conversation(other_user=user2)
            self.assertIsInstance(convo_started, Conversation)
            
            convo_started = Conversation.start_new_conversation(other_user=false_user)
            self.assertFalse(convo_started)
            
        ### Tests the get_other_user_of_conversation method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        user3 = User.query.get_or_404(3)
        with app.app_context():
            g.user = user1
            other_user = Conversation.get_other_user_of_conversation(user1, user2)
            self.assertEqual('testUser2', other_user.username)
            
            g.user = user2
            other_user = Conversation.get_other_user_of_conversation(user1, user2)
            self.assertEqual('testUser1', other_user.username)
            
            
            # Tests with user not in Conversation
            g.user = user3
            other_user = Conversation.get_other_user_of_conversation(user1, user2)
            self.assertFalse(other_user)
            
            
        ### Tests the check_for_existing_conversation method
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)
        user3 = User.query.get_or_404(3)
        with app.app_context():
            g.user = user1
            prev_conv = Conversation.check_for_existing_conversation(other_user=user2)
            self.assertTrue(prev_conv)

            prev_conv = Conversation.check_for_existing_conversation(other_user=user3)
            self.assertFalse(prev_conv)
    
    
    def test_past_usernames_model(self):
        """Tests the PasUsernames Model method."""

        ### Tests the store_old_username method
        user1 = User.query.get_or_404(1)
        with app.app_context():
            g.user = user1
            username_stored = PastUsernames.store_old_username('banana')
            self.assertTrue(username_stored)
            
            past_username = PastUsernames.query.get_or_404(1)
            self.assertEqual('banana', past_username.old_username)
            self.assertEqual(g.user.id, past_username.user_id)
            self.assertEqual(g.user.email, past_username.email)