from flask import g
from gamehunter.db import db
from sqlalchemy import UniqueConstraint
from datetime import datetime

##########################################################################################################################################

class Post(db.Model):
    """A model used to make the table and requirements for a User Post"""
    
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    game_id = db.Column(db.Integer, db.ForeignKey('games.rawg_id'), nullable=False)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.String(500), nullable=False)

    datetime_added = db.Column(db.DateTime, nullable=False)
    
    last_active = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User')
    
    game = db.relationship('Games')

    comments = db.relationship('Comment', cascade='all,delete')
        

    @classmethod
    def create_new_post(self, game_id=None, title=None, content=None):
        """Accepts a Game ID and Form data to create a new Post and commit it to the DB.
        
        Returns True on a successful Post creation, else returns False."""

        now = datetime.utcnow()
        new_post = Post(
            user_id = g.user.id,
            game_id = game_id,
            title = title,
            content = content,
            datetime_added = now,
            last_active = now
        )
        
        try:
            db.session.add(new_post)
            db.session.commit()
        except:
            return False
        return new_post
        
        
    @classmethod
    def edit_post(self, post=None, title=None, content=None):
        """Accepts a Post object and makes the appropriate changes and submits it to the DB.
        
        Returns True on successfuly commit, else returns False."""

        post.title = title
        post.content = content
        try:
            db.session.add(post)
            db.session.commit()
        except:
            return False
        return True
    
    
    @classmethod
    def remove_post(self, post=None, id=None):
        """Accepts a Post object or Post ID and will remove the Post if found. 
        
        Returns True on successful Post removal, else returns False."""
        
        if id:
            post = Post.query.get_or_404(id)
        
        if post.user.id != g.user.id:
            return False
        
        post.game.activity = post.game.activity - 1
        try:
            db.session.add(post.game)
            db.session.delete(post)
            db.session.commit()
        except:
            return False
        
        return True
            
        
##########################################################################################################################################

class Comment(db.Model):
    """Creates the 'comments' table and requirements for a User Comment."""
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'), nullable=False)
    
    content = db.Column(db.String(350), nullable=False)

    datetime_added = db.Column(db.DateTime, nullable=False)

    post = db.relationship('Post', overlaps='comments')
    
    upvotes = db.relationship('UpvoteComment', cascade='all,delete')
    
    
    @classmethod
    def create_new_comment(self, post=None, content=None):
        """Accepts a Post object and the content from the Comment submit and creates a new Comment object and commits it to the DB.
        
        Returns Comment object on successful creation and commit, else returns False."""
        now = datetime.utcnow()
        new_comment = Comment(
            user_id = g.user.id,
            post_id = post.id,
            content = content,
            datetime_added = now
        )
        post.last_active = now
        try:
            db.session.add(new_comment)
            db.session.add(post)
            db.session.commit()
        except:
            return False
        return new_comment
    
    
    @classmethod
    def edit_comment(self, comment=None, content=None):
        """Accepts a Comment Object and the content from the Comment edit and commits the new changes.
        
        Returns True on successful commit, else returns False."""

        comment.content = content
        try:
            db.session.add(comment)
            db.session.commit()
        except:
            return False
        return True
    
    
    @classmethod
    def remove_comment(self, comment=None, id=None):
        """Accepts either a Comment object or Comment ID. Will remove the Comment from the DB. 
        
        Returns True on successful removal, else returns False."""
        
        if id:
            comment = Comment.query.get_or_404(id)
            
        if comment.user_id != g.user.id:
            return False
            
        db.session.delete(comment)
        try:
            db.session.commit()
        except:
            return False

        return True


##########################################################################################################################################

class UpvoteComment(db.Model):
    """Creates the 'upvote_comments' table. Responsible for keeping track of Comments upvoted by Users."""
    
    __tablename__ = 'upvote_comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='cascade'))

    comment = db.relationship('Comment', overlaps='upvotes')
    
    __table_args__ = (UniqueConstraint('user_id', 'comment_id', name='user_liked_comments_constraint'),)
    
    
    @classmethod
    def create_new_comment_upvote(self, comment_id=None):
        """Creates a new UpvoteComment object and commits it to the DB.
        
        Returns UpvoteComment object on successful creation and commit, else returns False."""

        new_like = UpvoteComment(
        user_id = g.user.id,
        comment_id = comment_id
        )
        
        try:
            db.session.add(new_like)
            db.session.commit()
        except:
            return False
        return new_like


##########################################################################################################################################
    
class UpvotePost(db.Model):
    """Creates the 'upvote_posts' table. Responsible for keeping track of Posts upvoted by Users."""

    __tablename__ = 'upvote_posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'))

    post = db.relationship('Post', backref='upvotes')
    
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='user_liked_post_const'),)
    
    
    @classmethod
    def create_new_post_upvote(self, post_id=None):
        """Creates a new UpvotePost object and commits it to the DB.
        
        Returns UpvotePost object on successful creation and commit, else returns False."""

        new_like = UpvotePost(
        user_id = g.user.id,
        post_id = post_id
        )
        
        try:
            db.session.add(new_like)
            db.session.commit()
        except:
            return False
        return new_like


##########################################################################################################################################\