"""
"""
import tia.ressources as ressources




class Player:
    """
    """

    def __init__(self):
        self.name, self.shortname = ressources.random_player_name()
        # superpower activated
        if self.name == 'The flying bus shelter':
            self.name      = 'Our God, The Flying Bus Shelter'
            self.shortname = 'FBS'

    def __str__(self):
        return 'Player ' + self.shortname + ' ' + self.name
