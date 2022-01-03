import requests, json
from ...app import app
from ...blueprints.web_scraper.functions import clean_and_seperate_search_terms

class GetSteamNews():
    """A class designed to reach out to the Steam API and grab news articles"""
    @classmethod
    def get_steam_news(self, id: int, count=10, maxlength=250, format='json') -> dict:
        """Reaches out to the Steam API and grabs news articles based off the input parameters."""
        try:
            resp = requests.get(f'{app.config["BASE_URL_STEAM_NEWS"]}?key={app.config["STEAM_KEY"]}&appid={id}&count={count}&maxlength={maxlength}&format={format}')
        except:
            return False
        
        return resp

class RAWGioAPI():
    """A class designed to reach out to the RAWG API and grab information."""
    @classmethod
    def get_list_of_games(self, page=1, page_size=20):
        """Reaches out to the RAWG API for a list of non specific games.
        
        Returns API response. Returns False if it can't connect."""
        try:
            resp = requests.get(f'{app.config["RAWG_BASE_URL"]}?key={app.config["RAWG_KEY"]}&page={page}&page_size={page_size}')
        except:
            return False
        return resp

    @classmethod
    def get_specific_game(self, id :int) -> json:
        """Reaches out to the RAWG API for details about a specific game.
        
        Returns API response."""
        try:
            resp = requests.get(f'{app.config["RAWG_BASE_URL"]}/{id}?key={app.config["RAWG_KEY"]}')
        except:
            return False
        if 'detail' in resp.json():
            return None
        else:
            return resp
    
    @classmethod
    def game_search(self, terms :str):
        """Reaches out to the RAWG API and searches for a specific term.
        
        Returns API response."""
        clean_terms = clean_and_seperate_search_terms(terms)
        try:
            resp = requests.get(f'{app.config["RAWG_BASE_URL"]}?key={app.config["RAWG_KEY"]}&search={clean_terms}&exclude_additions=true&search_exact=true&ordering=-rating')
        except:
            return False
        return resp
    
    @classmethod
    def get_game_screenshots(self, id :int):
        """Reaches out to the RAWG API for screenshots of the specified Game ID.
        
        Returns API response. """
        try:
            resp = requests.get(f'{app.config["RAWG_BASE_URL"]}/{id}/screenshots?key={app.config["RAWG_KEY"]}')
        except:
            return False
        return resp