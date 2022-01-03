##########################################################################################################################################

def clean_and_seperate_search_terms(search_terms: str) -> str:
    """Returns a string of the search terms serperated by a '+' character."""
    
    search_terms = search_terms.strip().replace(' ', '+')
    return search_terms


##########################################################################################################################################
    
def clean_and_seperate_game_name(game_name: str) -> str:
    """Returns a string of the game name serperated by a '_' character."""

    game_name = game_name.strip().replace(' ', '_')
    return game_name
    
    
##########################################################################################################################################