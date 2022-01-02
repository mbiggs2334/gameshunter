import os, warnings
from unittest import TestCase
from flask import g
from app import app
from gamehunter.db import db
from blueprints.users.models import User
from blueprints.forum.models import Post, Comment, UpvoteComment, UpvotePost
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
        
    def test_forum_index_page(self):
        """Tests the Forum Index Page."""

        ### Tests when NOT logged in.
        resp = self.client.get('/forum/1')
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        self.assertIn('Hello There.', html)
        
        ### Tests when logged in.
        self.login_for_test()
        resp = self.client.get('/forum/1')
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        self.assertIn('Hello There.', html)
        
        
    
    def test_new_post_page(self):
        """Tests the Post submission page."""
        
        ##### Tests when NOT logged in.
        
        ### Tests GET request
        resp = self.client.get('/forum/post/new/12020', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You must be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
         ### Tests POST request
        resp = self.client.post('/forum/post/new/12020', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You must be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)


        ##### Tests when logged in.
        self.login_for_test()
        
        ### Tests GET through inproper channels.
        resp = self.client.get('/forum/post/new/4835', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn("Please create a post through the appropriate channels.", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        ### Tests GET with new Game.
        resp = self.client.get('/forum/post/new/4835', data=dict(name='Banana Nut Muffin Man'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Banana Nut Muffin Man', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        ### Tests GET with existing Game.
        resp = self.client.get('/forum/post/new/12020', data=dict(name='Left 4 Dead 2'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Left 4 Dead 2', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        
        ### Tests POST
        resp = self.client.post('/forum/post/new/12020', data=dict(title='Left 4 Dead is good.', content='Left 4 dead is nice.'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Post successfully created', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        
    def test_post_details_page(self):
        """Tests the Post details page."""

        ### Tests non existing Post
        resp = self.client.get('/forum/post/23')
        self.assertTrue(resp.status_code == 404)
        
        resp = self.client.post('/forum/post/23')
        self.assertTrue(resp.status_code == 404)

        
        ##### Tests when NOT logged in.
        
        ### Tests GET request
        resp = self.client.get('/forum/post/1')
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Banana baked beans.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests POST request
        resp = self.client.post('/forum/post/1', data=dict(comment='Cat.'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        
        ##### Tests when logged in.
        self.login_for_test()
        
        ### Tests GET request
        resp = self.client.get('/forum/post/1')
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Banana baked beans.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        ### Tests POST request
        resp = self.client.post('/forum/post/1', data=dict(comment='Cat.'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn("<p class='text-break'>Cat.</p>", html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    
    def test_like_comment(self):
        """Tests the Like Comment logic."""

        ### Tests when NOT logged in.
        resp = self.client.get('/forum/comment/1/like')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', json)
        self.assertIn('danger', json)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/forum/comment/1/like')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Add Successful.', json)
    
    
    
    def test_unlike_comment(self):
        """Tests the Unlike Comment logic."""
        
        ### Tests when NOT logged in.
        resp = self.client.get('/forum/comment/1/like')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', json)
        self.assertIn('danger', json)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/forum/comment/1/unlike')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Remove Successful.', json)
        
        
    
    def test_like_post(self):
        """Tests the Like Post logic."""

        ### Tests when NOT logged in.
        resp = self.client.get('/forum/post/1/like')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', json)
        self.assertIn('danger', json)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/forum/post/1/like')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Add Successful.', json)
        
        
        
    def test_unlike_post(self):
        """Tests the Unlike Post logic."""

        ### Tests when NOT logged in.
        resp = self.client.get('/forum/post/1/unlike')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', json)
        self.assertIn('danger', json)
        
        ### Tests when logged in.
        self.login_for_test()
        
        resp = self.client.get('/forum/post/1/unlike')
        json = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('Remove Successful.', json)
        
    
    
    def test_remove_post(self):
        """Tests the Remove Post logic."""

        ### Tests when NOT logged in.
        resp = self.client.get('/forum/post/remove/2', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        
        ### Tests when trying to remove a post that doesn't belong to user.
        self.login_for_test_2nd_user()
        resp = self.client.get('/forum/post/remove/1', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You cannot remove somebody else', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        
        ### Tests when logged in.
        self.login_for_test()
        
        self.client.post('/forum/post/new/12020', data=dict(title='Left 4 Dead is good.', content='Left 4 dead is nice.'))
        self.assertTrue(len(Post.query.all()) == 3)
        
        resp = self.client.get('/forum/post/remove/3', follow_redirects=True)
        self.assertFalse(len(Post.query.all()) == 3)
        
    
    
    def test_remove_comment(self):
        """Tests the remove Comment logic."""

        ### Tests when not logged in.
        resp = self.client.get('/forum/post/1/comment/remove/1', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Tests when trying to remove a comment that doesn't belong to user.
        self.login_for_test_2nd_user()
        resp = self.client.get('/forum/post/1/comment/remove/1', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You cannot remove somebody else', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        
        ### Tests when logged in.
        self.login_for_test()
        
        self.client.post('/forum/post/1', data=dict(comment='Cat.'), follow_redirects=True)
        self.assertTrue(len(Comment.query.all()) == 3)
        
        resp = self.client.get('/forum/post/1/comment/remove/2', follow_redirects=True)
        self.assertFalse(len(Post.query.all()) == 3)
        
    
    
    def test_edit_post(self):
        """Tests the Edit Post Logic."""

        ##### Tests when not logged in.
        
        ### Test GET request
        resp = self.client.get('/forum/post/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        ### Test POST request
        resp = self.client.post('/forum/post/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        
        ##### Tests trying to Edit a non owned Post
        
        ### Test GET request
        self.login_for_test_2nd_user()
        
        resp = self.client.get('/forum/post/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You can only edit your own posts.', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')

        ### Test POST request
        self.login_for_test_2nd_user()
        
        resp = self.client.post('/forum/post/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertTrue(resp.status_code == 200)
        self.assertIn('You can only edit your own posts.', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')

        ##### Tests when logged in
        self.login_for_test()
        
        ### Test GET request
        resp = self.client.get('/forum/post/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Banana baked beans.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
        ### Test POST request
        resp = self.client.post('/forum/post/1/edit', data=dict(content='Vanilla Bean.'), follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Vanilla Bean.', html)
        self.assertIn('testUser1', html)
        self.assertIn('Logout', html)
        
    
    
    def test_edit_comment(self):
        """Tests the Edit Comment logic."""

        ### Tests when not logged in
        resp = self.client.post('/forum/comment/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You need to be logged in to do that.', html)
        self.assertIn('Login', html)
        self.assertIn('Signup', html)
        
        
        ### Tests when trying to edit another User's comment
        self.login_for_test_2nd_user()
        
        resp = self.client.post('/forum/comment/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('You can only edit your own comments.', html)
        self.assertIn('testUser2', html)
        self.assertIn('Logout', html)
        
        self.client.get('/users/logout')
        
        ### Tests when logged in
        self.login_for_test()
        
        resp = self.client.post('/forum/comment/1/edit', query_string={'content':'Orange Banana'}, follow_redirects=True)
        json = resp.get_data(as_text=True)
        
        self.assertTrue(resp.status_code == 200)
        self.assertIn('Success', json)
        self.assertIn('Orange Banana', json)
        self.assertIn('testUser1', html)