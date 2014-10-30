import copy
from collections import deque
from Enums import *
from myheuristic import *

neighbours = ((0, 1), (1, 0), (-1, 0), (0, -1))

inverse_moves = {Direction.UP: (0, 1),
                 Direction.DOWN: (0, -1),
                 Direction.LEFT: (1, 0),
                 Direction.RIGHT: (-1, 0)}

def _get_good_moves(board, lightcycle, other_lightcycle):
    """Returns a list of good moves"""
    result = []
    for diff in ((0, 1, PlayerActions.MOVE_DOWN), (1, 0, PlayerActions.MOVE_RIGHT), (0, -1, PlayerActions.MOVE_UP), (-1, 0, PlayerActions.MOVE_LEFT)):
        next_x = lightcycle['position'][0] + diff[0]
        next_y = lightcycle['position'][1] + diff[1]
        if 0 <= next_x < len(board) and 0 <= next_y < len(board[0]):
            if board[next_x][next_y] in (EMPTY, POWERUP):
                if abs(next_x - other_lightcycle['position'][0]) + abs(next_y - other_lightcycle['position'][1]) > 1: 
                    result += [diff]
    return result
    
def _get_backup_moves(board, lightcycle, other_lightcycle):
    """Return a list of moves that can be taken iff necessary."""
    result = []
    for diff in ((0, 1, PlayerActions.MOVE_DOWN), (1, 0, PlayerActions.MOVE_RIGHT), (0, -1, PlayerActions.MOVE_UP), (-1, 0, PlayerActions.MOVE_LEFT)):
        next_x = lightcycle['position'][0] + diff[0]
        next_y = lightcycle['position'][1] + diff[1]
        if 0 <= next_x < len(board) and 0 <= next_y < len(board[0]):
            if board[next_x][next_y] in (EMPTY, POWERUP):
                result += [diff]
            elif lightcycle['isInvincible'] and board[next_x][next_y] == TRAIL and (next_x, next_y) != last_pos(lightcycle):
                result += [diff]
    return result

def last_pos(lightcycle):
    reverse_last_move = inverse_moves[lightcycle['direction']]
    lightcycle_pos = lightcycle['position']
    return (lightcycle_pos[0] + reverse_last_move[0], lightcycle_pos[1] + reverse_last_move[1])
                                                                                       
def num_neighbours(game_board, pos, target_values):
    res = 0
    for n in neighbours:
        if game_board[pos[0] + n[0]][pos[1] + n[1]] in target_values:
            res += 1
    return res
                                                                                       
def greedy_search (board, player_lightcycle, opponent_lightcycle, depth=2):
    print "We are currently considering ({},{})".format (player_lightcycle['position'][0], player_lightcycle['position'][1])
    board[player_lightcycle['position'][0]][player_lightcycle['position'][1]] = TRAIL
    
    max_score = -99999
    best_moves = [(0, 0, PlayerActions.SAME_DIRECTION)]
    
    moves = _get_good_moves(board, player_lightcycle, opponent_lightcycle)
    if len (moves) == 0:
        moves = _get_backup_moves(board, player_lightcycle, opponent_lightcycle)
    
    for move in moves:
        new_player_lightcycle = copy.deepcopy(player_lightcycle)
        new_board = copy.deepcopy(board)
        
        new_player_lightcycle['position'] = (player_lightcycle['position'][0] + move[0], player_lightcycle['position'][1] + move[1])
    
        if depth == 1:
            heuristic_value = heuristic(new_player_lightcycle, opponent_lightcycle, board)
        else:
            heuristic_value = 4*heuristic(new_player_lightcycle, opponent_lightcycle, board) + greedy_search(new_board, new_player_lightcycle, opponent_lightcycle, depth-1) [1]
            if board[new_player_lightcycle['position'][0]] [new_player_lightcycle['position'][1]] == POWERUP:
                heuristic_value += 100
    
        #print ("Possible move: {}; Heuristic value: {}; ".format(move, heuristic_value))
    
        if heuristic_value > max_score:
            best_moves = [move]
            max_score = heuristic_value
        elif heuristic_value == max_score:
            best_moves.append(move)
            max_score = heuristic_value
    
    print("Submitting best move " + str (best_moves[-1]) + " which scored a", max_score)
    return best_moves[-1][2], max_score