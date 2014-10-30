from Enums import *
import copy

_MAXIMIZING_PLAYER = 111
_MINIMIZING_PLAYER = 222

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

def _make_move (board, lightcycle, move):
    """
    Updates the state to reflect a hypothetical move. 
    move is a 3-tuple of the (change_in_x, change_in_y, enumerated_value e.g. PlayerActions.MOVE_RIGHT)
    """
    board [lightcycle['position'][0]] [lightcycle['position'][1]] = TRAIL
    lightcycle['position'] = lightcycle['position'][0] + move[0], lightcycle['position'][1] + move[1]     

def alphabeta(initial_state, depth, heuristic_function):
    """Runs an alphabeta search over the game tree for the car that we control"""
    def _alphabeta (state, depth, heuristic, alpha, beta, player):
        """
        state: a 3-tuple of (board, player_lightcycle, opponent_light_cycle)
        alpha, beta: minimum max and maximum min to apply alphabeta pruning. 
        Apply the naive minimax algorithm described http://en.wikipedia.org/wiki/Minimax, but return the best move, score."""

        board, player_lightcycle, opponent_lightcycle = state

        #If we have gone too deep, stop. 
        if depth == 0:
            value = heuristic (board, player_lightcycle, opponent_lightcycle)
            return None, value

        #The maximizing player iterates through all possible moves to explore their minimax scores.
        #Whenever a move with a better score is found, save it as the candidate score. 
        elif player == _MAXIMIZING_PLAYER:
            #Death is bad; sooner death is worse. 
            moves = _get_possible_moves (board, player_lightcycle) 
            if moves == [] or board [player_lightcycle['position'][0]] [player_lightcycle['position'][1]] not in (EMPTY, POWERUP):
                print ("THIS SHOULDN'T BE HAPPENING")
                return None, -1000 - depth
            
            best_move = None

            for move in moves:
                new_state = copy.deepcopy (state)
                _make_move (new_state[0], new_state[1], move)

                previous_move, candidate_alpha = _alphabeta (new_state, depth - 1, heuristic, alpha, beta, _MINIMIZING_PLAYER)
                if candidate_alpha >= alpha:
                    alpha = candidate_alpha
                    best_move = move[2]
                if beta <= alpha:
                    break
            return best_move, alpha

        #Same code as the maximizing player, but the minimizing player is trying to minimize the score. 
        elif player == _MINIMIZING_PLAYER:
            moves = _get_possible_moves (board, opponent_lightcycle)
            if moves == [] and board [opponent_lightcycle['position'][0]] [opponent_lightcycle['position'][1]] not in (EMPTY, POWERUP):
                print ("THIS SHOULDN'T BE HAPPENING")
                return None, 1000 + depth
            
            best_move = None
            for move in moves:
                new_state = copy.deepcopy (state)
                _make_move (new_state[0], new_state[2], move)

                previous_move, candidate_beta = _alphabeta (new_state, depth - 1, heuristic, alpha, beta, _MAXIMIZING_PLAYER)

                if candidate_beta <= beta:
                    beta = candidate_beta
                    best_move = move[2]
                if beta <= alpha:
                    break
            return best_move, beta 
            
    final_best_score = -10000
    final_best = None
    
    game_map, player_lightcycle, opponent_light_cycle = initial_state
        
    for move, direction in zip (((0, 1, PlayerActions.MOVE_DOWN), (1, 0, PlayerActions.MOVE_RIGHT), (0, -1, PlayerActions.MOVE_UP), 
        (-1, 0, PlayerActions.MOVE_LEFT)), ("Down", "Right", "Up", "Left")):
        new_state = copy.deepcopy (initial_state)
        _make_move (new_state[0], new_state[1], move)

        previous_move, candidate_alpha = _alphabeta (new_state, depth - 1, heuristic_function, -10000, 10000, _MINIMIZING_PLAYER)
        print ("Evaluated score for moving " + direction + " is " + str(candidate_alpha))

        if candidate_alpha > final_best_score:
            final_best_score = candidate_alpha
            final_best = move [2]

    return final_best
    #return _alphabeta (initial_state, depth, heuristic_function, -10000, 10000, _MAXIMIZING_PLAYER) [0]
