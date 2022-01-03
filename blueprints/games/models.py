from ...gamehunter.db import db

##########################################################################################################################################

class Games(db.Model):
    """Creates the 'games' table."""
    
    __tablename__ = 'games'

    rawg_id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    background_img = db.Column(db.Text, nullable=True)
    
    release_date = db.Column(db.Text, nullable=True)
    
    activity = db.Column(db.Integer, nullable=True, default=1)

    @classmethod
    def check_for_game_in_db(self, game_id: int) -> bool:
        """Checks if the game already exists in our DB. 

        Returns game if exists. """
        game = Games.query.get(game_id)
        if game == None:
            return False
        return game

    @classmethod
    def create_new_game(self, rawg_id=None, title=None, background_img=None, release_date=None):
        """Create a new Game and stores it in the DB. 
        
        Returns the Game object if successfully created and commited, else returns False."""
        
        new_game = Games(
                rawg_id = rawg_id,
                title = title,
                background_img = background_img,
                release_date = release_date
                )

        try:
            db.session.add(new_game)
            db.session.commit()
        except:
            return False
        return new_game

    
##########################################################################################################################################