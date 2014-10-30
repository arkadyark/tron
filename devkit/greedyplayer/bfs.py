## TODO - find out how to properly import this
from Enums import *
from collections import deque
import cProfile

possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def heuristic(player_pos, opponent_pos, game_map):
    player_distances = bfs(player_pos, game_map)
    ours, theirs, neutral = bfs2(opponent_pos, game_map, player_distances)

    return len (ours) - len (theirs)

def bfs(pos, game_map):
    # Calculates shortest path distances from pos to all nodes
    fringe = deque()
    fringe.append((pos, 0))
    fringe_length = 1
    distances = {pos:0}
    # Keep track of nodes visited, don't revisit nodes
    visited = {pos}
    while fringe_length != 0:
        node = fringe.popleft()
        fringe_length -= 1
        nodeCoords = node[0]
        nodeLength = node[1]
        # Write the distance to the node
        distances[nodeCoords] = nodeLength
        for successor in getSuccessors(nodeCoords, game_map):
            if successor not in visited:
                visited.add(successor)
                successor_length = nodeLength + 1
                fringe.append((successor, successor_length))
                fringe_length += 1
    return distances

def bfs2(pos, game_map, player_distances):
    # Assigns each square as either ours (closest to player), theirs (closest to opponent),
    # or neutral (equal)
    fringe = deque()
    fringe.append((pos, 0))
    fringe_length = 1
    ours = []
    theirs = [pos]
    neutral = []
    # Keep track of nodes visited, don't revisit nodes
    visited = {pos}
    while fringe_length != 0:
        node = fringe.popleft()
        fringe_length -= 1
        nodeCoords = node[0]
        nodeLength = node[1]
        # Assign the node by comparing path lengths
        for successor in getSuccessors(nodeCoords, game_map):
            if successor not in visited:
                visited.add(successor)
                successor_length = nodeLength + 1
                fringe.append((successor, successor_length))
                fringe_length += 1
                # Assign the node by comparing path lengths
                player_path_length = player_distances[successor]
                if successor_length > player_path_length:
                    ours.append(successor)
                elif successor_length < player_path_length:
                    theirs.append(successor)
                else:
                    neutral.append(successor)
    return ours, theirs, neutral

def getSuccessors(pos, game_map):
    successors = []
    for move in possible_moves:
        next_move = (pos[0] + move[0], pos[1] + move[1])
        next_x = pos[0] + move[0]
        next_y = pos[1] + move[1]
        ## Assuming always bounded by walls
        next_move_type = game_map[next_move[0]][next_move[1]]
        # If the next move is empty or powerup
        if next_move_type in (POWERUP, EMPTY):
            successors.append((next_x, next_y))
    return successors