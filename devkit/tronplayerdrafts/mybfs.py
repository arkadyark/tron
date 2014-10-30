

def bfs(pos, game_map):
    # Calculates shortest path distances from pos to all nodes
    fringe = deque()
    fringe.append((pos, 0))
    fringe_length = 1
    distances = {pos:0}
   
    new_game_map = [[0 if game_map[i][j] in (POWERUP, EMPTY) else: -1 for j in xrange(len(game_map[0]))] for i in xrange (len (game_map))]
   
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