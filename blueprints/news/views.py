from flask.json import jsonify
from blueprints.api.models import GetSteamNews
from blueprints.web_scraper.models import WebScraper
from blueprints.blueprints import news_bp

##########################################################################################################################################

@news_bp.route('/<string:name>')
def home_page(name):
    """Endpoint to reach out to the WebScrape App and Steam API for Game news. 
    
    Returns JSON."""
    
    scrape_resp = WebScraper.scrape_steam_for_id(name, name)
    
    if scrape_resp:
        news = GetSteamNews.get_steam_news(scrape_resp[0])
        return news.json()
    else:
        return jsonify(dict(message='None'))