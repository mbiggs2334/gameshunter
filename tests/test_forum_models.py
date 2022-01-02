import os, warnings
from re import S
from unittest import TestCase
from flask import g
from app import app
from gamehunter.db import db
from blueprints.users.models import User
from blueprints.forum.models import Post, Comment, UpvoteComment, UpvotePost
from blueprints.games.models import Games



os.environ['DATABASE_URL'] = "postgresql:///gamehunters_db_test"

db.drop_all()

class ForumModelTestCase(TestCase):
    """Tests the GamesHunter Forum Model methods."""


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
            new_post = Post(
                user_id = g.user.id,
                game_id = 12020,
                title = 'Hello There.',
                content = 'Banana baked beans.',
                datetime_added = '12/12/2022',
                last_active = '12/12/2022')
            new_game = Games(rawg_id=12020, title='Left 4 Dead 2')
            db.session.add(new_game)
            db.session.add(new_post)
            db.session.commit()
            new_comment = Comment(
                user_id = g.user.id,
                post_id = new_post.id,
                content = 'Nice :)', 
                datetime_added = '12/12/2022'
            )
            db.session.add(new_comment)
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
        
    
    def test_post_model(self):
        """Tests the Post Model."""
        
        ### Tests the create_new_post method
        with app.app_context():
            g.user = User.query.get_or_404(1)
            Post.create_new_post(game_id=12020, title='blueberry', content='more blueberries')
        
        post = Post.query.get_or_404(2)
        self.assertIsInstance(post, Post)
        self.assertTrue(Post.query.get_or_404(1))
        self.assertTrue(post.title == 'blueberry')
        self.assertTrue(post.content == 'more blueberries')
        
        ### Tests the edit_post method
        Post.edit_post(post=post, title='new title', content='new content')
        self.assertIsInstance(post, Post)
        self.assertTrue(post.title == 'new title')
        self.assertTrue(post.content == 'new content')
        
        ### Tests the remove_post method with CORRECT User
        with app.app_context():
            g.user = User.query.get_or_404(1)
            post_removed = Post.remove_post(post=post)
        
        self.assertTrue(post_removed)
        
        ### Tests the remove_post method with INCORRECT User
        with app.app_context():
            # adds new post with different user
            g.user = User.query.get_or_404(1)
            Post.create_new_post(game_id=12020, title='blueberry', content='more blueberries')
            post = Post.query.get_or_404(3)
            # attempts to remove with incorrect User
            g.user = User.query.get_or_404(2)
            post_removed = Post.remove_post(post=post)
            
        self.assertFalse(post_removed)
        
    
    def test_comment_model(self):
        """Tests the Comment Model."""

        ### Tests the create_new_comment method
        with app.app_context():
            g.user = User.query.get_or_404(1)
            post = Post.query.get_or_404(1)
            Comment.create_new_comment(post=post, content='hello')

        comment = Comment.query.get_or_404(2)
        self.assertIsInstance(comment, Comment)
        self.assertTrue(comment.content == 'hello')
        self.assertTrue(comment.post_id == 1)
        
        
        ### Tests the edit_comment method
        with app.app_context():
            g.user = User.query.get_or_404(1)
            Comment.edit_comment(comment=comment, content='new comment')
        
        comment = Comment.query.get_or_404(2)
        self.assertTrue(comment.content == 'new comment')
        self.assertIsInstance(comment, Comment)
        
        
        ### Tests the remove_comment method with CORRECT User
        with app.app_context():
            g.user = User.query.get_or_404(1)
            comment_removed = Comment.remove_comment(id=2)
            
        self.assertTrue(comment_removed)
        
        ### Tests the remove_comment method with INCORRECT User
        with app.app_context():
            # adds new comment with different user
            g.user = User.query.get_or_404(1)
            post = Post.query.get_or_404(1)
            comment = Comment.create_new_comment(post=post, content='goodbye')
            # attempts to remove with incorrect User
            g.user = User.query.get_or_404(2)
            comment_removed = Comment.remove_comment(comment=comment)
            
        self.assertFalse(comment_removed)
        
        
    def test_upvote_comment(self):
        """Tests the UpVote Comment Model."""

        with app.app_context():
            g.user = User.query.get_or_404(1)
            comment = Comment.query.get_or_404(1)
            new_like = UpvoteComment.create_new_comment_upvote(comment_id=comment.id)
        
        comment = Comment.query.get_or_404(1)
        user = User.query.get_or_404(1)
        
        self.assertTrue(new_like)
        self.assertTrue(len(comment.upvotes) > 0)
        self.assertTrue(len(user.comments[0].upvotes) > 0)
        
    
    def test_upvote_post(self):
        """Tests the UpVote Post Model."""

        with app.app_context():
            g.user = User.query.get_or_404(1)
            post = Post.query.get_or_404(1)
            new_like = UpvotePost.create_new_post_upvote(post_id=post.id)
        
        post = Post.query.get_or_404(1)
        user = User.query.get_or_404(1)
        
        self.assertTrue(new_like)
        self.assertTrue(len(post.upvotes) > 0)
        self.assertTrue(len(user.posts[0].upvotes) > 0)
        
    