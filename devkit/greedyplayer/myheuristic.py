from collections import deque
from Enums import *

import cProfile

neighbours = ((0, 1), (1, 0), (-1, 0), (0, -1))

OBSTACLE = -12345
TIE = -23456

def heuristic(play_pos, opp_pos, game_map):
    # Calculates shortest path distances from pos to all nodes

    cur_dist = 1 #distance from either node that we are currently expanding
    
    p_fringe = deque()
    p_fringe.append(play_pos)
    player_nodes = 1
    
    o_fringe = deque()
    o_fringe.append(opp_pos)
    opponent_nodes = 1

    if game_map[opp_pos[0]][opp_pos[1]] not in (EMPTY, POWERUP):
        o_fringe.pop()
    
    new_game_map = [[OBSTACLE if game_map[i][j] not in (EMPTY, POWERUP) else 0 for j in range(len(game_map))] for i in range(len(game_map))]
    
    new_game_map [play_pos[0]] [play_pos[1]] = 1
    new_game_map [opp_pos[0]] [opp_pos[1]] = -1
    
    while (len (p_fringe) > 0 or len (o_fringe) > 0):
        while len (p_fringe) > 0 and new_game_map[play_pos[0]][play_pos[1]] == cur_dist:
            #expand the node 
            node = p_fringe.popleft()
            for n in neighbours:
                if new_game_map[n[0] + node[0]][n[1] + node[1]] == 0:
                    p_fringe.append((n[0] + node[0], n[1] + node[1]))
                    new_game_map[n[0] + node[0]][n[1] + node[1]] = cur_dist + 1
                    player_nodes += 1
            
        while len (o_fringe) > 0 and new_game_map[opp_pos[0]][opp_pos[1]] == -cur_dist:            
            node = o_fringe.popleft()
            for n in neighbours:
                if new_game_map[n[0] + node[0]][n[1] + node[1]] == 0:
                    new_game_map[n[0] + node[0]][n[1] + node[1]] = -cur_dist - 1
                    o_fringe.append((n[0] + node[0], n[1] + node[1]))
                    opponent_nodes += 1
                elif new_game_map[n[0] + node[0]][n[1] + node[1]] == cur_dist + 1:
                    new_game_map[n[0] + node[0]][n[1] + node[1]] = TIE
                    player_nodes -= 1
        cur_dist += 1 
        
    return player_nodes - opponent_nodes
