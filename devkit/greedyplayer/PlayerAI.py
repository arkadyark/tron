from greed import greedy_search
from Enums import *

class PlayerAI():
    #conversions of enumerated values of Direction to x, y vectors. 
    activate_powerups = {PlayerActions.SAME_DIRECTION:PlayerActions.ACTIVATE_POWERUP,
    PlayerActions.MOVE_UP:PlayerActions.ACTIVATE_POWERUP_MOVE_UP,
    PlayerActions.MOVE_DOWN:PlayerActions.ACTIVATE_POWERUP_MOVE_DOWN,
    PlayerActions.MOVE_LEFT:PlayerActions.ACTIVATE_POWERUP_MOVE_LEFT,
    PlayerActions.MOVE_RIGHT:PlayerActions.ACTIVATE_POWERUP_MOVE_RIGHT}
    
    def __init__(self):
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        print ("==GREEDY==")
        return

    def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
        g = greedy_search(game_map, player_lightcycle, opponent_lightcycle)
        
        if player_lightcycle['hasPowerup']:
            g = PlayerAI.activate_powerups[g]        
        return g 
