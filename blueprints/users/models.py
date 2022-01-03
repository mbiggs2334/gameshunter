from flask import g, session, flash, current_app as app, request
from gamehunter.db import db
from datetime import datetime
from flask_bcrypt import Bcrypt
from blueprints.s3.models import S3Handler
from sqlalchemy import UniqueConstraint, and_, or_
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename

bcrypt = Bcrypt()

##########################################################################################################################################

class Message(db.Model):
    """Creates the 'messages' table."""
    
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    sent_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    sent_to_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    seen_by_user = db.Column(db.Boolean, nullable=False, default=False)
    
    content = db.Column(db.String(500), nullable=False)

    datetime_sent = db.Column(db.DateTime, nullable=False)
    
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    
    sent_by = db.relationship('User', foreign_keys=[sent_by_id])

    sent_to = db.relationship('User', foreign_keys=[sent_to_id])
    
    @classmethod
    def new_message(self, sent_by=None, sent_to=None, convo_id=None, content=None):
        """Creates a new Message object and commits it to the DB.
        
        Rerturns True on Successful creation and commit, else returns False."""
        
        now = datetime.utcnow()
        convo = Conversation.query.get_or_404(convo_id)
        new_message = Message(
            sent_by_id = int(sent_by),
            sent_to_id = int(sent_to),
            content = content,
            datetime_sent = now,
            conversation_id = convo_id
        )
        convo.last_active = now
        try:
            db.session.add(convo)
            db.session.add(new_message)
            db.session.commit()
        except:
            return False
        return True
    
    
    
    @classmethod
    def mark_message_as_seen(self, message_obj=None):
        """Accepts a message object containing unseen messages by User, and marks them as seen."""

        for message in message_obj:
            message.seen_by_user = True
            db.session.add(message)
        db.session.commit()


##########################################################################################################################################

class Block(db.Model):
    """Creates the 'blocks' table."""
    
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_who_blocked_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    user_who_is_blocked_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    
    blocked_user = db.relationship('User', foreign_keys=[user_who_is_blocked_id])

    user_who_blocked = db.relationship('User', foreign_keys=[user_who_blocked_id])
    
    @classmethod
    def create_new_block(self, user=None):
        """Accepts ONLY a User object and creates a new Block object and adds it to the DB.
        
        Returns True on successful creation and commit, else returns False."""
        
        new_block = Block(
            user_who_blocked_id = g.user.id,
            user_who_is_blocked_id = user.id
        )
        
        if user in g.user.following:
            Follow.remove_follow(other_user=user)
        
        if user in g.user.followers:
            follow = Follow.query.filter(Follow.user_following_id==user.id, Follow.user_being_followed_id==g.user.id).first()
            db.session.delete(follow)

        messages = Message.query.filter(or_(and_(Message.sent_to_id==user.id, Message.sent_by_id==g.user.id), and_(Message.sent_by_id==user.id, Message.sent_to_id==g.user.id)), Message.seen_by_user==False).all()
        Message.mark_message_as_seen(message_obj=messages)
        
        try:
            db.session.add(new_block)
            db.session.commit()
        except:
            return False
        
        return True
    
    @classmethod
    def remove_block(self, user=None, id=None):
        """Accepts a User object or User ID and removes the block associated with that user.
        
        Returns True on successful block removal, else returns False."""

        if id:
            user = User.query.get_or_404(id)
        
        block = Block.query.filter(Block.user_who_is_blocked_id==user.id, Block.user_who_blocked_id==g.user.id).first()
        
        try:
            db.session.delete(block)
            db.session.commit()
        except:
            return False
        
        return True
    
    
##########################################################################################################################################

class Follow(db.Model):
    """Creats the 'followers' table."""
    
    __tablename__ = 'followers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    user_following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    user_being_followed_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    datetime_followed = db.Column(db.DateTime, nullable=False)



    @classmethod
    def create_new_follow(self, other_user=None, id=None):
        """Takes a User ID or User object to create a new Follow and commit it to the DB.
        
        Will grab the User object if an ID is given.
        
        Returns the new Follow object on successful creation and commit, else returns False."""
        
        if id:
            other_user = User.query.get_or_404(id)
            
        now = datetime.utcnow()    
        
        new_follow = Follow(
            user_following_id = g.user.id,
            user_being_followed_id = other_user.id,
            datetime_followed = now
        )
        try:
            db.session.add(new_follow)
            db.session.commit()
        except:
            return False
        return new_follow
    
    
    @classmethod
    def check_if_following(self, other_user=None, id=None) -> object:
        """Takes a parameter of a User object or User ID and checks if g.user is 
        following the param user.
        
        Returns the param User object if True. Else returns False."""
        
        if id:
            other_user = User.query.get_or_404(id)
        
        if other_user.id == g.user.id:
            return False
        
        if other_user in g.user.following:
            return other_user
        
        return False
            
    
    
    @classmethod
    def remove_follow(self, other_user=None, id=None):
        """Takes a User ID or User object and will remove them from
        g.user's followings. 
        
        Will also grab the User object if the User ID is given.
        
        Returns True if successful, else returns False."""
        
        if id:
            other_user = User.query.get_or_404(id)
        
        if other_user.id == g.user.id:
            return False
        
        follow = Follow.query.filter(Follow.user_following_id==g.user.id, Follow.user_being_followed_id==other_user.id).first()
        
        try:
            db.session.delete(follow)
            db.session.commit()
        except:
            return False
        return True
        
        
    
   
    
##########################################################################################################################################

class User(db.Model):
    """ An individual user. """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(30), unique=True, nullable=False)

    email = db.Column(db.Text, unique=True, nullable=False)

    password = db.Column(db.Text, nullable=False)

    profile_image = db.Column(db.Boolean, default=False, nullable=False)
    
    profile_image_uploaded = db.Column(db.Boolean, default=False, nullable=False)
    
    bio = db.Column(db.String(500), nullable=True)

    date_joined = db.Column(db.Date, nullable=False)
    
    active = db.Column(db.Boolean, nullable=False, default=False)
    
    last_active = db.Column(db.DateTime, nullable=True)

    email_confirmation_sent_on = db.Column(db.Date, nullable=False)

    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)

    email_confirmed_on = db.Column(db.Date, nullable=True)
    
    favorites = db.relationship('FavoriteGames', cascade='all,delete')
    
    posts = db.relationship('Post', overlaps='user', cascade='all,delete')
    
    blocked = db.relationship('User', secondary='blocks', primaryjoin=(Block.user_who_blocked_id == id), secondaryjoin=(Block.user_who_is_blocked_id == id), overlaps="user_who_blocked, blocked_user")

    blocked_by = db.relationship('User', secondary='blocks', primaryjoin=(Block.user_who_is_blocked_id == id), secondaryjoin=(Block.user_who_blocked_id == id), overlaps='blocked, blocked_user, user_who_blocked')

    comments = db.relationship('Comment', cascade='all,delete', backref='user')
    
    upvoted_comments = db.relationship('UpvoteComment', cascade='all,delete', backref='user')

    upvoted_posts = db.relationship('UpvotePost', cascade='all,delete', backref='user')
    
    messages_sent = db.relationship('Message', cascade='all,delete', primaryjoin=(Message.sent_by_id == id), overlaps="sent_by")

    messages_received = db.relationship('Message', cascade='all,delete', primaryjoin=(Message.sent_to_id == id), overlaps="sent_to")

    unseen_messages = db.relationship('Message', cascade='all,delete', backref='user', primaryjoin="and_(Message.sent_to_id == User.id, " "Message.seen_by_user == False)", overlaps="messages_received, sent_to")

    conversations = db.relationship('Conversation', cascade='all,delete', primaryjoin="or_(Conversation.started_by == User.id, " "Conversation.received_by == User.id)")

    following = db.relationship('User', secondary='followers', primaryjoin=(Follow.user_following_id==id), secondaryjoin=(Follow.user_being_followed_id==id), overlaps="following")

    followers = db.relationship('User', secondary='followers', primaryjoin=(Follow.user_being_followed_id==id), secondaryjoin=(Follow.user_following_id==id), overlaps="following")
    
    def __repr__(self):
        return f'<User #{self.id}: {self.username}, {self.email}>'

    
    @classmethod
    def signup(self, username, email, password):
        """Signs up user. 
        
        Hashes password and adds to database """

        today = datetime.today()
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            date_joined=f'{today.month}/{today.day}/{today.year}',
            email_confirmation_sent_on=f'{today.month}/{today.day}/{today.year}'
        )
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            raise e
        
        S3Handler.create_user_image_storage_in_s3(user.id)
        
        return user
    
    
    
    @classmethod
    def authenticate_user(self, email=None, password=None):
        """Tries to find existing user.
        
        Validates credentials if user is found."""

        user = self.query.filter_by(email=email).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False
    
    
    
    @classmethod
    def check_if_g_user_blocked(self, id):
        """Checks if the param user is blocking g.user.
        
        Will return the user if the user is blocking g.user. """

        user = User.query.get(id)
        
        for blocked_user in user.blocked:
            
            if g.user.id == blocked_user.id:
                return user
            else:
                return False
            
            
            
    @classmethod
    def check_if_g_user_blocking(self, id):
        """Checks if g.user is blocking param user.
        
        Will return the param user if g.user is blocking param user."""

        user = User.query.get(id)
        
        for blocked_user in g.user.blocked:
            
            if user.id == blocked_user.id:
                return user
            else:
                return False
    
    
    @classmethod
    def change_user_image(self, file=None,):
        """Changes/Upload the User image."""

        g.user.profile_image = True
        g.user.profile_image_uploaded = True
        filename = secure_filename(f'{g.user.id}profile.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        S3Handler.upload_user_image(g.user.id)

    
    
    @classmethod
    def update_user_info(self, form=None):
        """Updates the User information. 
        
        Returns True on successful update, else returns False."""

        g.user.username = form.username.data
        g.user.bio = form.bio.data
        
        if request.form.getlist('check') == ['on']:
            g.user.profile_image = True
            if request.form.getlist('check') == ['on'] and not g.user.profile_image_uploaded:
                flash('You need to upload an image to enable custom profile photos.', 'danger')
        else:
            g.user.profile_image = False

        try:
            db.session.add(g.user)
            db.session.commit()
            
        except:
            db.session.rollback()
            flash('Username already taken. Please select another.', 'danger')
            return False
        
        return True
            
            

    def change_password(self, new_password):
        """Hashes the User's new password and stores it in the DB. """
        
        new_password = bcrypt.generate_password_hash(new_password).decode('UTF-8')
        self.password = new_password
        
        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        
        return True
    
    
    @classmethod
    def delete_account(self):
        """Deletes User Account. """

        session.pop('curr_user')
        db.session.delete(g.user)
        
        try:
            db.session.commit()
        except:
            flash('Something went wrong. Please try again later.', 'danger')
            return False
        
        flash('Account successfully deleted.', 'success')
        return True
    

##########################################################################################################################################

class FavoriteGames(db.Model):
    """Creates the 'user_game_favorites' table. """
    
    __tablename__ = 'user_game_favorites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    game_id = db.Column(db.Integer, db.ForeignKey('games.rawg_id', ondelete='cascade'))
    
    position = db.Column(db.Integer, nullable=True)
    
    __table_args__ = (UniqueConstraint('user_id', 'game_id', name='user_favorites_constraint'), )
        
    user = db.relationship('User', overlaps='favorites')
    
    game = db.relationship('Games')

    
    @classmethod
    def create_new_favorite(self, game_id: int, position: int):
        """Creates a new FavoriteGames object and adds it to the DB. 
        
        Returns FavoriteGames object on successful creation and commit, else returns False."""

        new_fav = FavoriteGames(
        user_id = g.user.id,
        game_id = game_id,
        position = position
        )
        
        try:
            db.session.add(new_fav)
            db.session.commit()
        except:
            return False
        return True
        
        
    @classmethod
    def check_for_favorite(self, game_id: int) -> bool:
        """Checks if the user already has the game as a favorite. 
        
        Returns True if the relation already exists"""
        
        check = FavoriteGames.query.filter(FavoriteGames.user_id==g.user.id, FavoriteGames.game_id==game_id ).first()
        
        if check == None:
            return False
        return True
    
        
    @classmethod
    def edit_user_favorites(self, form=None):
        """Modifies the User's favorites. 
        
        Returns True on successful edit and commit, else returns False."""
        
        for game in g.user.favorites:
            id = str(game.game_id)
            if form[id] == 'removed':
                db.session.delete(game)
            else:
                game.position = int(form.get(id))
                db.session.add(game)
                
            
            try:
                db.session.commit()
            except:
                return False
        return True


        
##########################################################################################################################################

class Conversation(db.Model):
    """Creates the 'conversations' table."""
    
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    started_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    received_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    started_on = db.Column(db.DateTime, nullable=True)
    
    last_active = db.Column(db.DateTime, nullable=False)

    started_by_user = db.relationship('User', primaryjoin=(User.id==started_by), overlaps="conversations")

    received_by_user = db.relationship('User', primaryjoin=(User.id==received_by), overlaps="conversations")
    
    messages = db.relationship('Message', primaryjoin=(Message.conversation_id==id))


    @classmethod
    def start_new_conversation(self, other_user=None):
        """Takes a User object and starts a new conversation between param User and g.User.
        
        Returns the Conversation object on successful creation, else returns False."""
        
        if not isinstance(other_user, User):
            return False
        
        now = datetime.utcnow()
        
        new_convo = Conversation(
            started_by = g.user.id,
            received_by = other_user.id,
            started_on = now,
            last_active = now
        )
        
        try:
            db.session.add(new_convo)
            db.session.commit()
        except:
            return False
        
        return new_convo


    @classmethod
    def get_other_user_of_conversation(self, user1, user2):
        """Takes two user objects of a conversation and returns the one that 
        is not g.user."""

        if not isinstance(user1, User) or not isinstance(user2, User):
            return False
        
        if user1.id == g.user.id:
            return user2
        elif user2.id == g.user.id:
            return user1
        else:
            return False
        
        
        
    @classmethod
    def check_for_existing_conversation(self, other_user=None, id=None):
        """Takes a user object or id and checks if there is an already existing conversation with g.user.
        
        Returns the conversation ID if it finds an existing conversation; Else returns False."""

        if id:
            other_user = User.query.get_or_404(id)
            
        if other_user.id == g.user.id:
            return False
        
        for convo in other_user.conversations:
            
            if convo in g.user.conversations:
                return convo.id
            
        return False
    
    
##########################################################################################################################################

class PastUsernames(db.Model):
    """Creates the'past_usernames' table."""
    
    __tablename__ = 'past_usernames'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)

    old_username = db.Column(db.Text, nullable=False)
    
    email = db.Column(db.Text, nullable=False)

    lastdate_used = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship('User', backref='past_usernames')
    
    def __repr__(self):
        return f'<#{self.id}, username:{self.old_username}, email:{self.email}'
    
    
    
    @classmethod
    def store_old_username(self, old_username: str):
        """Creates a new PastUsernames object and stores theUser's old username, in the DB. 
        
        Returns True on successful creation and commit, else returns False."""
        
        now = datetime.utcnow()
        
        past_username = PastUsernames(
            user_id = g.user.id,
            old_username = old_username,
            email = g.user.email,
            lastdate_used = now
        )
        
        try:
            db.session.add(past_username)
            db.session.commit()
        except:
            return False
        
        return True
    
    
##########################################################################################################################################