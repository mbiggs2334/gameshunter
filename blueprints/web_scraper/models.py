import requests
from .functions import clean_and_seperate_search_terms, clean_and_seperate_game_name
from bs4 import BeautifulSoup

steam_search_url = 'https://store.steampowered.com/search/?term='
        
##########################################################################################################################################
        
class WebScraper():
    """A class dedicated to grabbing game IDs from Steam's webpages via a GET request"""
        
    @classmethod
    def scrape_steam_for_id(self, search_terms: str, game_name: str) -> list:
        """Returns a list of integers (upon successful finding) by scraping 
        the Steam page for the game id. This function is designed specifcally 
        to grab game ID's from Steam's search page.
        
        Else, returns False"""
        
        return_list = []
        
        clean_game_name = clean_and_seperate_game_name(game_name)
        
        clean_terms = clean_and_seperate_search_terms(search_terms)
        
        html = requests.get(steam_search_url + clean_terms)
        
        soup = BeautifulSoup(html.content, 'lxml')
        
        links_in_soup = soup.select('a[href^="https://store.steampowered.com/app/"]')
        
        for link in links_in_soup:
            if clean_game_name in link.get('href'):
                return_list.append(link.get('data-ds-appid'))

        if len(return_list) > 0:
            int_list = list(map(int, return_list))
            return int_list
        else:
            return False