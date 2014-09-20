from Queue import Queue

def partition(player_pos, opponent_pos, board):
    player_distances = bfs(player_pos)
    ours, theirs, neutral = bfs2(opponent_pos, player_distances)
    return ours, theirs, neutral

def bfs(player_pos):
    fringe = Queue()
    fringe.put(player_pos)
    while not fringe.isEmpty():
	node = fringe.get()
	nodeCoords = node[0]
	nodePath = node[1]
	if nodeCoords not in closed:
	    closed.add(nodeCoords)
	    if problem.isGoalState(nodeCoords):
		return nodePath
	    else:
		for successor in problem.getSuccessors(nodeCoords):
		    successorNode = successor[0]
		    successorAction = successor[1]
		    newPath = nodePath + [successorAction]
		    fringe.push((successorNode, newPath))
