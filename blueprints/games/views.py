from flask import flash, redirect, render_template, g, request, jsonify
from ...gamehunter.db import db
from ...blueprints.api.models import RAWGioAPI
from .models import Games
from ...blueprints.users.models import FavoriteGames
from ...blueprints.blueprints import games_bp

### An initial list of grabbed games from the RAWG API
rawg_resp = RAWGioAPI.get_list_of_games()

##########################################################################################################################################

@games_bp.route('/', methods=['GET', 'POST'])
def games_home_page():
    """Endpoint to render the Games home page."""
    
    if not rawg_resp.status_code or rawg_resp.status_code != 200:
        games=False
    else:
        games=rawg_resp.json()['results']
        
    return render_template('games/games_home.html', games=games)


##########################################################################################################################################

@games_bp.route('/<int:id>')
def game_details_page(id):
    """Endpoint for a Game details page."""
    
    try:
        resp = RAWGioAPI.get_specific_game(id)
        screenshots = RAWGioAPI.get_game_screenshots(id)
    except:
        flash('Something went wrong. Please try again.', 'danger')
        return redirect('/')
    
    if not resp:
         flash("The game you're searching for doesn't exist. Sorry about that.", 'danger')
         return redirect('/')
     
    return render_template('games/game_details.html', game=resp.json(), screenshots=screenshots.json())
    
    
##########################################################################################################################################

@games_bp.route('/search/<string:term>')
def return_search_results(term):
    """Endpoint that reaches out to the RAWG api for the query coming from the user."""
    
    if term.strip() == '':
        flash('Please enter a search value', 'danger')
        return redirect('/games')
    
    resp = RAWGioAPI.game_search(term)
    
    return resp.json()


##########################################################################################################################################

@games_bp.route('/favorites/add')
def add_game_to_favorites():
    """Adds the game to the user's favorites as well as to a games database."""
    
    if not g.user:
        return jsonify(dict(message='You need to be logged in to do that.', category='danger'))

    if len(g.user.favorites) >= 10:
        return jsonify(dict(message=f"You already have the maxiumum amount of favorites. Please <a class='link-light' href='/users/{g.user.id}/favorites'>remove</a> one to add another.", category='danger'))

    game_id = request.args['game_id']
    game_check = Games.check_for_game_in_db(game_id)
    
    if game_check:
        game_check.activity = game_check.activity + 1
        try:
            db.session.add(game_check)
            db.session.commit()
        except:
            return jsonify(dict(message='Something went wrong. Please try again later.', category='danger'))
        pass
    
    else:
        new_game = Games.create_new_game(rawg_id=game_id,title=request.args['game_name'],
                                         background_img=request.args['game_image'],
                                         release_date=request.args['release_date'])
        
    fav_check = FavoriteGames.check_for_favorite(game_id)
    
    if fav_check:
        return jsonify(dict(message='You already have this game in your favorites.', category='danger'))
    else:
        pass
    
    new_fav = FavoriteGames.create_new_favorite(game_id=game_id, position=len(g.user.favorites) + 1)
    if not new_fav:
            return jsonify(dict(message='Something went wrong. Please try again later.', category='danger'))
        
    return jsonify(dict(message='Game successfully added to your favorites.', category='success'))


##########################################################################################################################################

@games_bp.route('/favorites/remove')
def remove_game_from_favorites():
    """Endpoint to from the Game from the User's favorites."""

    if not g.user:
        return jsonify(dict(message='You need to be logged in to do that.', category='danger'))

    favorite = FavoriteGames.query.filter(FavoriteGames.user_id==g.user.id,FavoriteGames.game_id==request.args['game_id']).first()
    
    game = Games.query.get_or_404(request.args['game_id'])
    
    game.activity = game.activity - 1
    
    try:
        db.session.add(game)
        db.session.delete(favorite)
        db.session.commit()
        
    except:
        return jsonify(dict(message='Something went wrong. Please try again later.', category='danger'))
    
    return jsonify(dict(message='Game successfully removed from your favorites.', category='success'))


##########################################################################################################################################