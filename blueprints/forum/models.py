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
    
    likes = db.Column(db.Integer, nullable=False, default=0)
    
    user = db.relationship('User')
    
    game = db.relationship('Games')

    comments = db.relationship('Comment', cascade='all,delete')
        

    @classmethod
    def create_new_post(self, game_id=None, title=None, content=None):
        """Accepts a Game ID and Form data to create a new Post and commit it to the DB.
        
        Returns the new Post object on a successful Post creation, else returns False."""

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
        
        
    @classmethod
    def add_post_like(self, post=None, id=None):
        """Adds a Like to the specified Post.
            
        Returns True on successful commit, else returns False."""

        if id:
            post = Post.query.get_or_404(id)
                
        post.likes = post.likes + 1
            
        try:
            db.session.add(post)
            db.session.commit()
        except:
            return False
            
        return True
        
        
    @classmethod
    def subtract_post_like(self, post=None, id=None):
        """Subtracts a Like from the specified Post.
            
        Returns True on successful commit, else returns False."""

        if id:
            post = Post.query.get_or_404(id)
                
        post.likes = post.likes - 1
            
        try:
            db.session.add(post)
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

    likes = db.Column(db.Integer, nullable=False, default=0)
    
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
    
    
    @classmethod
    def add_comment_like(self, comment=None, id=None):
        """Adds a Like to the specified Comment.
        
        Returns True on successful commit, else returns False."""

        if id:
            comment = Comment.query.get_or_404(id)
            
        comment.likes = comment.likes + 1
        
        try:
            db.session.add(comment)
            db.session.commit()
        except:
            return False
        
        return True
    
    
    @classmethod
    def subtract_comment_like(self, comment=None, id=None):
        """Subtracts a Like from the specified Comment.
        
        Returns True on successful commit, else returns False."""

        if id:
            comment = Comment.query.get_or_404(id)
            
        comment.likes = comment.likes - 1
        
        try:
            db.session.add(comment)
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

        already_liked = UpvoteComment.query.filter(UpvoteComment.comment_id==comment_id, UpvoteComment.user_id==g.user.id).first()
        if already_liked != None:
            return False
        
        new_like = UpvoteComment(
        user_id = g.user.id,
        comment_id = comment_id
        )
        
        has_past_downvote = DownvoteComment.query.filter(DownvoteComment.comment_id==comment_id, DownvoteComment.user_id==g.user.id).first()
        if has_past_downvote != None:
            downvote_removed = DownvoteComment.remove_comment_downvote(comment_id=comment_id)
        
        like_added_to_comment = Comment.add_comment_like(id=comment_id)
        
        try:
            db.session.add(new_like)
            db.session.commit()
        except:
            return False
        return new_like
    
    
    @classmethod
    def remove_comment_upvote(self, comment_id=None):
        """Deletes a UpvoteComment object and commits it to the DB.
        
        Returns True on successful deletion and commit, else returns False."""

        comment_upvote = UpvoteComment.query.filter(UpvoteComment.comment_id==comment_id, UpvoteComment.user_id==g.user.id).first()

        if comment_upvote == None:
            return False
        
        like_removed_from_comment = Comment.subtract_comment_like(id=comment_id)
        
        try:
            db.session.delete(comment_upvote)
            db.session.commit()
        except:
            return False
        return True
    
    
##########################################################################################################################################

    
class DownvoteComment(db.Model):
    """Creates the 'downvote_comments' table. Responsible for keeping track of Comments downvoted by Users."""
    
    __tablename__ = 'down_comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='cascade'))

    comment = db.relationship('Comment', overlaps='downvotes')
    
    __table_args__ = (UniqueConstraint('user_id', 'comment_id', name='user_disliked_comments_constraint'),)
    
    
    @classmethod
    def create_new_comment_downvote(self, comment_id=None):
        """Creates a new UpvoteComment object and commits it to the DB.
        
        Returns UpvoteComment object on successful creation and commit, else returns False."""

        already_downvoted = DownvoteComment.query.filter(DownvoteComment.comment_id==comment_id, DownvoteComment.user_id==g.user.id).first()
        if already_downvoted != None:
            return False
        
        new_dislike = DownvoteComment(
        user_id = g.user.id,
        comment_id = comment_id
        )
        
        has_comment_upvote = UpvoteComment.query.filter(UpvoteComment.comment_id==comment_id, UpvoteComment.user_id==g.user.id).first()
        if has_comment_upvote != None:
            upvote_removed = UpvoteComment.remove_comment_upvote(comment_id=comment_id)
            
        like_removed_from_comment = Comment.subtract_comment_like(id=comment_id)
        
        try:
            db.session.add(new_dislike)
            db.session.commit()
        except:
            return False
        return new_dislike

    @classmethod
    def remove_comment_downvote(self, comment_id=None):
        """Deletes a DownvoteComment object and commits it to the DB.
        
        Returns True on successful deletion and commit, else returns False."""

        comment_downvote = DownvoteComment.query.filter(DownvoteComment.comment_id==comment_id, DownvoteComment.user_id==g.user.id).first()

        if comment_downvote == None:
            return False
        
        like_added_to_comment = Comment.add_comment_like(id=comment_id)
        
        try:
            db.session.delete(comment_downvote)
            db.session.commit()
        except:
            return False
        return True


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
        
        
        has_post_downvote = DownvotePost.query.filter(DownvotePost.post_id==post_id, DownvotePost.user_id==g.user.id).first()
        if has_post_downvote != None:
            downvote_removed = DownvotePost.remove_post_downvote(post_id=post_id)

        like_added_to_post = Post.add_post_like(id=post_id)
        
        try:
            db.session.add(new_like)
            db.session.commit()
        except:
            return False
        return new_like
    
    
    @classmethod
    def remove_post_upvote(self, post_id=None):
        """Removes an UpvotePost Object and commits it to the DB.
        
        Returns True on successful creation and commit, else returns False."""

        post_upvote = UpvotePost.query.filter(UpvotePost.post_id==post_id, UpvotePost.user_id==g.user.id).first()
        
        like_removed_from_post = Post.subtract_post_like(id=post_id)
        
        try:
            db.session.delete(post_upvote)
            db.session.commit()
        except:
            return False
        return True


##########################################################################################################################################
    
class DownvotePost(db.Model):
    """Creates the 'downvote_posts' table. Responsible for keeping track of Posts downvoted by Users."""

    __tablename__ = 'downvote_posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'))

    post = db.relationship('Post', backref='downvotes')
    
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='user_disliked_post_const'),)
    
    
    @classmethod
    def create_new_post_downvote(self, post_id=None):
        """Creates a new UpvotePost object and commits it to the DB.
        
        Also Removes on 'Like' from the Post Object
        
        Returns UpvotePost object on successful creation and commit, else returns False."""

        new_dislike = DownvotePost(
        user_id = g.user.id,
        post_id = post_id
        )
        
        has_post_upvote = UpvotePost.query.filter(UpvotePost.post_id==post_id, UpvotePost.user_id==g.user.id).first()
        if has_post_upvote != None:
            upvote_removed = UpvotePost.remove_post_upvote(post_id=post_id)

        like_removed_from_post = Post.subtract_post_like(id=post_id)
        
        
        try:
            db.session.add(new_dislike)
            db.session.commit()
        except:
            return False
        return new_dislike
    
    
    
    @classmethod
    def remove_post_downvote(self, post_id=None):
        """Removes the DownvotePost object and commits it to the DB.
        
        Returns True on successful creation and commit, else returns False."""

        post_downvote = DownvotePost.query.filter(DownvotePost.post_id==post_id, DownvotePost.user_id==g.user.id).first()
        
        like_added_to_post = Post.add_post_like(id=post_id)
        
        if like_added_to_post:
            try:
                db.session.delete(post_downvote)
                db.session.commit()
            except:
                return False
            return True
        return False
