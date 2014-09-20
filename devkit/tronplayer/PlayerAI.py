import random
from tronclient.Client import *
from Enums import *
import partition
import time

class PlayerAI():

    def __init__(self):
        self.trails = []
        self.walls = []
        self.powerups = []
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        self.width = len(game_map[0])
        self.height = len(game_map)
        self.walls = self.get_all(game_map, WALL)
        self.powerups = self.get_all(game_map, POWERUP)
        print self.width, self.height
        print self.powerups
        print self.walls

    def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
        startTime = time.time()
        return self.get_move_greedy(game_map, player_lightcycle, opponent_lightcycle, moveNumber)
        print "Took " + str(time.time() - startTime) + "ms to calculate next move!"

    def get_move_greedy(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
        my_position = player_lightcycle['position']
        my_x = my_position[0]
        my_y = my_position[1]
        my_direction = player_lightcycle['direction']
        directions = {Direction.UP : (0, 1), Direction.DOWN : (0, -1), Direction.LEFT : (-1, 0), Direction.RIGHT : (1, 0)}
        left_turns = {Direction.UP : Direction.LEFT, Direction.DOWN : Direction.RIGHT, \
                      Direction.LEFT : Direction.DOWN, Direction.RIGHT : Direction.UP}
        right_turns = {Direction.UP : Direction.RIGHT, Direction.DOWN : Direction.LEFT, \
                      Direction.LEFT : Direction.UP, Direction.RIGHT : Direction.DOWN}

        next_pos = my_x + directions[my_direction][0], \
                            my_y + directions[my_direction][1]
        next_player_cycle = {'direction':my_direction, 'isInvincible':false, \
                                hasPowerup:game_map[my_x + directions[my_direction][0], \
                                                    my_y + directions[my_direction][1]},
                                
            

    def heuristic(self, board, player_lightcycle, opponent_lightcycle):
        my_position = player_lightcycle['position']
        their_position = player_lightcycle['position']
        ours, theirs, neutral = partition.partition(my_position, their_position, board)
        return len(ours) - len(theirs)

    def get_all(self, game_map, square_type):
                # Gets all values on the map with value equal to square_type
                vals = []
                for i in xrange(self.height):
                        for j in xrange(self.width):
                                if game_map[i][j] == square_type:
                                        vals.append((i, j))
                return vals
'''

8888888 8888888888 8 888888888o.      ,o888888o.     b.             8 
      8 8888       8 8888    `88.  . 8888     `88.   888o.          8 
      8 8888       8 8888     `88 ,8 8888       `8b  Y88888o.       8 
      8 8888       8 8888     ,88 88 8888        `8b .`Y888888o.    8 
      8 8888       8 8888.   ,88' 88 8888         88 8o. `Y888888o. 8 
      8 8888       8 888888888P'  88 8888         88 8`Y8o. `Y88888o8 
      8 8888       8 8888`8b      88 8888        ,8P 8   `Y8o. `Y8888 
      8 8888       8 8888 `8b.    `8 8888       ,8P  8      `Y8o. `Y8 
      8 8888       8 8888   `8b.   ` 8888     ,88'   8         `Y8o.` 
      8 8888       8 8888     `88.    `8888888P'     8            `Yo
      
                                Quick Guide
                --------------------------------------------
                      Feel free to delete this comment.

        1. THIS IS THE ONLY .PY OR .BAT FILE YOU SHOULD EDIT THAT CAME FROM THE ZIPPED STARTER KIT

        2. Any external files should be accessible from this directory

        3. new_game is called once at the start of the game if you wish to initialize any values

        4. get_move is called for each turn the game goes on

        5. game_map is a 2-d array that contains values for every board position.
                example call: game_map[2][3] == POWERUP would evaluate to True if there was a powerup at (2, 3)

        6. player_lightcycle is your lightcycle and is what the turn you respond with will be applied to.
                It is a dictionary with corresponding keys: "position", "direction", "hasPowerup", "isInvincible", "powerupType"
                position is a 2-element int array representing the x, y value
                direction is the direction you are travelling in. can be compared with Direction.DIR where DIR is one of UP, RIGHT, DOWN, or LEFT
                hasPowerup is a boolean representing whether or not you have a powerup
                isInvincible is a boolean representing whether or not you are invincible
                powerupType is what, if any, powerup you have

        7. opponent_lightcycle is your opponent's lightcycle. Same keys and values as player_lightcycle

        8. You ultimately are required to return one of the following:
                                                PlayerAction.SAME_DIRECTION
                                                PlayerAction.MOVE_UP
                                                PlayerAction.MOVE_DOWN
                                                PlayerAction.MOVE_LEFT
                                                PlayerAction.MOVE_RIGHT
                                                PlayerAction.ACTIVATE_POWERUP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_UP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_DOWN
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_LEFT
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_RIGHT
                
        9. If you have any questions, contact challenge@orbis.com

        10. Good luck! Submissions are due Sunday, September 21 at noon. You can submit multiple times and your most recent submission will be the one graded.
 
'''
