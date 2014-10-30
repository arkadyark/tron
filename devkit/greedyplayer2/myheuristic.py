from collections import deque
from Enums import *

neighbours = ((0, 1), (1, 0), (-1, 0), (0, -1))

OBSTACLE = -12345
TIE = -23456

# Different parameter sets for the different 'modes'
parameters = {'near':{'voronoi_weight':3.0, 'powerup_weight':3, 'territory_weight':0.15, 'max_powerup_dist':50},
              'far':{'voronoi_weight':4.5, 'powerup_weight':7, 'territory_weight':0.3, 'max_powerup_dist':50},
              'endgame':{'voronoi_weight':6.0, 'powerup_weight':2, 'territory_weight':0.6, 'max_powerup_dist':30}}

def heuristic(play_pos, isInvincible, opp_pos, game_map):
    # Calculates shortest path distances from pos to all nodes

    if game_map[play_pos[0]][play_pos[1]] == WALL or (game_map[play_pos[0]][play_pos[1]] == TRAIL and not isInvincible):
        return -5000
    
    collided = False
    
    cur_dist = 1 #distance from either node that we are currently expanding
    territory_score = 0
    
    p_fringe = deque()
    p_fringe.append(play_pos)
    player_nodes = 1
    
    o_fringe = deque()
    o_fringe.append(opp_pos)
    opponent_nodes = 1
    
    new_game_map = [[OBSTACLE if game_map[i][j] not in ((EMPTY, POWERUP) if not isInvincible else (EMPTY, POWERUP, TRAIL)) else 0 for j in range(len(game_map[0]))] for i in range(len(game_map))]
    
    new_game_map [play_pos[0]] [play_pos[1]] = 1
    new_game_map [opp_pos[0]] [opp_pos[1]] = -1

    num_powerups = sum([column.count(POWERUP) for column in game_map])

    manhattan_distance = abs(play_pos[0] - opp_pos[0]) + abs(play_pos[1] - opp_pos[1])
    if manhattan_distance <= 8:
        mode = 'near'
    else:
        mode = 'far'
    
    distance_to_powerup = 0 if game_map[play_pos[0]][play_pos[1]] == POWERUP else (50 if num_powerups else 0)
    
    while (len (p_fringe) > 0 or len (o_fringe) > 0) and cur_dist < 30:
        while len (p_fringe) > 0 and new_game_map[p_fringe[0][0]][p_fringe[0][1]] <= cur_dist:
            #expand the node
            node = p_fringe.popleft()
            for n in neighbours:
                if new_game_map[n[0] + node[0]][n[1] + node[1]] == 0:
                    p_fringe.append((n[0] + node[0], n[1] + node[1]))
                    new_game_map[n[0] + node[0]][n[1] + node[1]] = cur_dist + 1
                    player_nodes += 1
                    territory_score += 1
                elif new_game_map[n[0] + node[0]][n[1] + node[1]] != OBSTACLE:
                    territory_score += 1
                if game_map[n[0] + node[0]][n[1] + node[1]] == POWERUP:
                    distance_to_powerup = min(distance_to_powerup, cur_dist)                   
        while len (o_fringe) > 0 and new_game_map[o_fringe[0][0]][o_fringe[0][1]] >= -cur_dist:
            node = o_fringe.popleft()
            for n in neighbours:
                if new_game_map[n[0] + node[0]][n[1] + node[1]] == 0:
                    new_game_map[n[0] + node[0]][n[1] + node[1]] = -cur_dist - 1
                    o_fringe.append((n[0] + node[0], n[1] + node[1]))
                    opponent_nodes += 1
                elif new_game_map[n[0] + node[0]][n[1] + node[1]] == cur_dist + 1:
                    new_game_map[n[0] + node[0]][n[1] + node[1]] = TIE
                    player_nodes -= 1
                    collided = True
                elif new_game_map[n[0] + node[0]][n[1] + node[1]] > 0:
                    collided = True
        cur_dist += 1

    if not collided:
        mode = 'endgame'

    params = parameters[mode]
    score = (player_nodes - opponent_nodes)*params['voronoi_weight'] \
            - distance_to_powerup*params['powerup_weight'] \
            - territory_score*params['territory_weight']

    #print manhattan_distance
    if manhattan_distance <= 2:
        score -= 1000
        #print "DANGEROUSLY CLOSE"

    #print "Mode:", mode
    #print "Player nodes:", player_nodes
    #print "Opponent nodes:", opponent_nodes
    #print "Voronoi", (player_nodes - opponent_nodes)*params['voronoi_weight']
    #print "Powerup score", -(distance_to_powerup**2)*params['powerup_weight']
    #print "Territory score", - territory_score*params['territory_weight']
    
    return score
