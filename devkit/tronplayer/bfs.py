from Queue import Queue
## TODO - find out how to properly import this
from Enums import *
import cProfile

possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def partition(player_pos, opponent_pos, game_map):
    pr = cProfile.Profile()
    pr.enable()
    
    player_distances = _bfs(player_pos, game_map)
    ours, theirs, neutral = _bfs2(opponent_pos, game_map, player_distances)
    territory_score = getTerritoryScore(ours, game_map)
    
    pr.disable()
    pr.print_stats()

    return ours, theirs, neutral, territory_score
    
    
def _bfs(pos, game_map):
    # Calculates shortest path distances from pos to all nodes
    fringe = Queue()
    fringe.put((pos, []))
    distances = {pos:0}
    # Keep track of nodes visited, don't revisit nodes
    visited = {pos} 
    while not fringe.empty():
        node = fringe.get()
        nodeCoords = node[0]
        nodePath = node[1]
        # Write the distance to the node
        distances[nodeCoords] = len(nodePath)
        for successor in getSuccessors(nodeCoords, game_map):
            if successor not in visited:
                visited.append(successor)
                successorPath = nodePath + [successor]
                fringe.put((successor, successorPath))      
    return distances

def _bfs2(pos, game_map, player_distances):
    # Assigns each square as either ours (closest to player), theirs (closest to opponent),
    # or neutral (equal)
    fringe = Queue()
    fringe.put((pos, []))
    ours = []
    theirs = [pos]
    neutral = []
    # Keep track of nodes visited, don't revisit nodes
    visited = {pos}
    while not fringe.empty():
        node = fringe.get()
        nodeCoords = node[0]
        nodePath = node[1]
        # Assign the node by comparing path lengths
        path_length = len(nodePath)
        for successor in getSuccessors(nodeCoords, game_map):
            if successor not in visited:
                visited.append(successor)
                successorPath = nodePath + [successor]
                fringe.put((successor, successorPath))
                # Assign the node by comparing path lengths
                player_path_length = player_distances[successor]
                if path_length + 1 > player_path_length:
                    ours.append(successor)
                elif path_length + 1 < player_path_length:
                    theirs.append(successor)
                else:
                    neutral.append(successor)
    return ours, theirs, neutral

def getSuccessors(pos, game_map):
    successors = []
    width = len(game_map[0])
    height = len(game_map)
    for move in possible_moves:
        next_move = (pos[0] + move[0], pos[1] + move[1])
        if 0 <= next_move[0] < width and 0 <= next_move[1] < height:
            next_move_type = game_map[next_move[0]][next_move[1]]
            # If the next move is empty or powerup
            if next_move_type == POWERUP or next_move_type == EMPTY:
                successors.append(next_move)
    return successors

def getTerritoryScore(territory, game_map):
    def numNeighbors(pos):
        return len(getSuccessors(pos, game_map))
    return sum(map(numNeighbors, territory))
