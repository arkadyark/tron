import copy
from collections import deque
from Enums import *
from myheuristic import *

inverse_moves = {Direction.UP: (0, 1),
                 Direction.DOWN: (0, -1),
                 Direction.LEFT: (1, 0),
                 Direction.RIGHT: (-1, 0)}

def _get_possible_moves(board, lightcycle):
    """Returns a list of possible moves"""
    result = []
    for diff in ((0, 1, PlayerActions.MOVE_DOWN), (1, 0, PlayerActions.MOVE_RIGHT), (0, -1, PlayerActions.MOVE_UP), (-1, 0, PlayerActions.MOVE_LEFT)):
        next_x = lightcycle['position'][0] + diff[0]
        next_y = lightcycle['position'][1] + diff[1]
        if 0 <= next_x < len(board) and 0 <= next_y < len(board[0]):
            if board[next_x][next_y] in (EMPTY, POWERUP):
                result += [diff]
            if lightcycle['isInvincible'] and board[next_x][next_y] == TRAIL and (next_x, next_y) != last_pos(lightcycle):
                result += [diff]
    return result

def last_pos(lightcycle):
    reverse_last_move = inverse_moves[lightcycle['direction']]
    lightcycle_pos = lightcycle['position']
    return (lightcycle_pos[0] + reverse_last_move[0], lightcycle_pos[1] + reverse_last_move[1])
                                                                                       

def greedy_search (board, player_lightcycle, opponent_lightcycle):
    #print ("The AI is currently on a {} ({},{})".format (board[player_lightcycle['position'][0]][player_lightcycle['position'][1]],
    # player_lightcycle['position'][0],player_lightcycle['position'][1]))
    
    board[player_lightcycle['position'][0]][player_lightcycle['position'][1]] = TRAIL
    
    max_score = -99999
    best_moves = [(0, 0, PlayerActions.SAME_DIRECTION)]
    
    for move in _get_possible_moves(board, player_lightcycle):
        heuristic_value = heuristic((player_lightcycle['position'][0] + move[0], player_lightcycle['position'][1] + move[1]),
            player_lightcycle['isInvincible'],
         (opponent_lightcycle['position'][0], opponent_lightcycle['position'][1]), board)
        #print (str(move[2]) + "'s value of heuristic is " + str (heuristic_value))
    
        if heuristic_value > max_score:
            best_moves = [move]
            max_score = heuristic_value
        elif heuristic_value == max_score:
            best_moves.append(move)
            max_score = heuristic_value
    
    #print ("Submitting best move" + str(best_moves[-1]))
    return best_moves[-1][2]
