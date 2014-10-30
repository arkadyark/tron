#####################################################
# Tic Tac Toe alpha-beta
# 
# Goal: Applying alpha-beta algorithm to tic tac toe
# Author: Christopher Chu
# Modification of the tic-tac-toe minimax program. 

import random
import copy

MAXIMIZING_PLAYER = 1
MINIMIZING_PLAYER = 2

def print_board (board):
    for i in board:
        print (i)
    print ("===========")


def check_win (board):
    "Returns 1 if player 1 wins, 2 if player 2 wins, 0 otherwise."
    for i in range (3):
        if board [0] [i] == board [1] [i] == board [2] [i] != 0:
            return board [0] [i]
        if board [i] [0] == board [i] [1] == board [i] [2] != 0:
            return board [i] [0]
    if (board [0] [0] == board [1] [1] == board [2] [2] != 0 or 
    board [2] [0] == board [1] [1] == board [0] [2] != 0):
        return board [1] [1]
    return 0
        
def get_possible_moves (board):
    "Returns a tuple of all possible moves by checking for empty squares"
    res = []
    for x, i in enumerate (board):
        for y, j in enumerate (i):
            if j == 0:
                res.append ((x, y))
    return res

def play_at (board, x, y, player):
    "Player places a 1 or 2 at board [x] [y]. "
    if board [x] [y] == 0:
        board [x] [y] = player
        return True
    else:
        print ("Invalid move")
        return False

def alphabeta (board, depth, alpha, beta, player):
    "Apply the naive minimax algorithm described http://en.wikipedia.org/wiki/Minimax, but return the best move, score."

    #If we have reached a terminal node, i.e. we should stop the recursion or one player has one,
    #evaluate the score. 
    if depth == 0 or get_possible_moves (board) == [] or check_win (board) != 0:
        return None, {1:1, 0:0, 2:-1} [check_win (board)]

    #The maximizing player iterates through all possible moves to explore their minimax scores.
    #Whenever a move with a better score is found, save it as the candidate score. 
    elif player == MAXIMIZING_PLAYER:
        best_move = None

        moves = get_possible_moves (board) #shuffle the moves to make it interesting. 
        random.shuffle(moves)  #what should be done is ordering the moves so it searches best first. 
        for move in moves:
            new_board = copy.deepcopy (board)
            play_at (new_board, move[0], move[1], MAXIMIZING_PLAYER)

            previous_move, candidate_alpha = alphabeta (new_board, depth - 1, alpha, beta, MINIMIZING_PLAYER)

            if candidate_alpha > alpha:
                alpha = candidate_alpha
                best_move = move
            if beta <= alpha:
                break
            
        return best_move, alpha

    #Like the maximizing player, the minimizing player is trying to minimize the score. 
    elif player == MINIMIZING_PLAYER:
        best_move = None
        
        moves = get_possible_moves (board) #shuffle the moves to make it interesting.
        random.shuffle(moves)
        for move in moves:
            new_board = copy.deepcopy (board)
            play_at (new_board, move[0], move[1], MINIMIZING_PLAYER)

            previous_move, candidate_beta = alphabeta (new_board, depth - 1, alpha, beta, MAXIMIZING_PLAYER)

            ###   Stack trace. I recommend that you put this in an if (depth == something) block so you don't have a huge output.
            #if depth == 6:
            #    print ("Minimizing player's turn. Candidate {} {}, score: {}/ Best score: {}".format (move [0], move[1], candidate_beta, beta))
            #    print_board (new_board)

            if candidate_beta < beta:
                beta = candidate_beta
                best_move = move
            if beta <= alpha:
                break
        return best_move, beta      

def begin_alphabeta(board, depth, player):
    return alphabeta (board, depth, -1000, 1000, player)

if __name__ == '__main__':
    print ("ALPHA-BETA Algorithm")
    
    board = [[0 for j in range (3)] for i in range (3)]
    cur_player = MAXIMIZING_PLAYER

    while (check_win (board) == 0 and get_possible_moves(board) != []): 
        if cur_player == MAXIMIZING_PLAYER:
            (move_x, move_y), result = begin_alphabeta (board, 9, MAXIMIZING_PLAYER)
        elif cur_player == MINIMIZING_PLAYER:
            (move_x, move_y), result = begin_alphabeta (board, 9, MINIMIZING_PLAYER)
            #move_x, move_y = random.choice (get_possible_moves (board))
        

        play_at (board, move_x, move_y, cur_player)
        print_board (board)
        
        cur_player = cur_player % 2 + 1

    if check_win (board) == 0:
        print ("Cat's game!")
    else:
        print ("Player {} has won!".format (check_win (board)))

