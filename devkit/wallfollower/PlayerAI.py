"Wall follower: Always follows the right wall"""

from tronclient.Client import *
from Enums import *

import copy

class PlayerAI():
    #conversions of enumerated values of Direction to x, y vectors. 
    DIRECTION_TO_VECT = {Direction.UP:(0, -1), Direction.DOWN:(0, 1), Direction.RIGHT: (1, 0), Direction.LEFT: (-1, 0)}

    def __init__(self):
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        print ("==WALL FOLLOWER==")
        return

    def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
        if PlayerAI.is_safe (self.check_left (game_map, player_lightcycle)):
            return self.turn_left(player_lightcycle)
        elif PlayerAI.is_safe (self.check_ahead (game_map, player_lightcycle)):
            return PlayerActions.SAME_DIRECTION
        elif PlayerAI.is_safe (self.check_right (game_map, player_lightcycle)):
            return self.turn_right(player_lightcycle)
        else:
            return PlayerActions.ACTIVATE_POWERUP

    @staticmethod
    def is_safe(cell):
        """Returns whether the cell is safe (i.e. is empty or contains a powerup)"""
        return cell in (EMPTY, POWERUP)
    
    def check_ahead(self, game_map, player_lightcycle):
        """Returns whatever is in the cell ahead"""
        lookahead_direction = PlayerAI.DIRECTION_TO_VECT[player_lightcycle['direction']]
        return game_map [player_lightcycle['position'][0] + lookahead_direction[0]] [player_lightcycle['position'][1] + lookahead_direction[1]]

    def check_left(self, game_map, player_lightcycle):
        """Returns whatever is in the cell to the left of the current cell"""
        lookahead_direction = PlayerAI.DIRECTION_TO_VECT[player_lightcycle['direction']]
        return game_map [player_lightcycle['position'][0] + lookahead_direction[1]] [player_lightcycle['position'][1] - lookahead_direction[0]]

    def check_right(self, game_map, player_lightcycle):
        """Returns whatever is in the cell to the right of the current cell"""
        lookahead_direction = PlayerAI.DIRECTION_TO_VECT[player_lightcycle['direction']]
        return game_map [player_lightcycle['position'][0] - lookahead_direction[1]] [player_lightcycle['position'][1] + lookahead_direction[0]]

    def turn_left(self, player_lightcycle):
        """Return the action to move the player one square to the right"""
        new_direction = (player_lightcycle['direction'] - 1) % 4
        return (PlayerActions.MOVE_UP, PlayerActions.MOVE_RIGHT, PlayerActions.MOVE_DOWN, PlayerActions.MOVE_LEFT) [new_direction]

    def turn_right(self, player_lightcycle):
        """Return the action to move the player one square to the right"""
        new_direction = (player_lightcycle['direction'] + 1) % 4
        return (PlayerActions.MOVE_UP, PlayerActions.MOVE_RIGHT, PlayerActions.MOVE_DOWN, PlayerActions.MOVE_LEFT) [new_direction]
