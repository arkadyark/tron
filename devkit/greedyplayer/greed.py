
import copy
from collections import deque
from Enums import *
from myheuristic import *

def _get_possible_moves(board, lightcycle):
    """Returns a list of possible moves"""
    result = []
    for diff in ((0, 1, PlayerActions.MOVE_DOWN), (1, 0, PlayerActions.MOVE_RIGHT), (0, -1, PlayerActions.MOVE_UP), (-1, 0, PlayerActions.MOVE_LEFT)):
        next_x = lightcycle['position'][0] + diff[0]
        next_y = lightcycle['position'][1] + diff[1]
        if 0 <= next_x < len(board) and 0 <= next_y < len(board[0]):
            if board[next_x][next_y] in (EMPTY, POWERUP):
                result += [diff]
    return result
    
def greedy_search (board, player_lightcycle, opponent_lightcycle):
    board[player_lightcycle['position'][0]][player_lightcycle['position'][1]] = TRAIL
    
    max_score = -99999
    best_moves = [PlayerActions.SAME_DIRECTION]
    
    for move in _get_possible_moves(board, player_lightcycle):
        heuristic_value = heuristic((player_lightcycle['position'][0] + move[0], player_lightcycle['position'][1] + move[1]), 
         (opponent_lightcycle['position'][0], opponent_lightcycle['position'][1]), board)
    
        if heuristic_value > max_score:
            best_moves = [move]
            max_score = heuristic_value
        elif heuristic_value == max_score:
            best_moves.append(move)
            max_score = heuristic_value
    
    return best_moves[-1][2]
