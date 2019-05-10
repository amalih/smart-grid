
def main():

    beta = 90
    remainingEnergy = beta
    potentialEnergy = 0 # Energy used by nodes of priority lower than the priority of the current node

    # Nodes are ordered by priority
    nodes = ('A', 'C', 'G', 'L', 'O', 'P', 'F', 'B', 'M', 'N')
    source = nodes[0]

    # The distances are used to calculate the shortest distance from the source to each node
    distances = {
        'A': {'B': 5, 'C': 10},
        'C': {'O': 40, 'F': 50},
        'G': {'O': 40, 'B': 5, 'L': 13, 'N': 13},
        'L': {},
        'O': {'G': 20, 'C': 10},
        'P': {},
        'F': {'M': 13},
        'B': {'P': 10, 'G': 20},
        'M': {},
        'N': {}}

    # The distancesInverted are used to calculate the shortest distance from each predecessor to a given node.
    # For example, (A, B, C and O) are predecessors to G.
    distancesInverted = {
        'A': {},
        'C': {'A': 10},
        'G': {'O': 20, 'B': 20},
        'L': {'G': 13},
        'O': {'G': 40, 'C': 40},
        'P': {'B': 10},
        'F': {'C': 50},
        'B': {'A': 5},
        'M': {'F': 13},
        'N': {'G': 13}}

    neighbours = {'A': ['C', 'B'], 'C': ['A', 'O', 'F'], 'G': ['O', 'B', 'N', 'L'],
                'L': ['G'], 'O': ['C', 'G'], 'P': ['B'], 'F': ['C', 'M'],
                'B': ['A', 'P', 'G'], 'M':  ['F'], 'N': ['G']}
    cost = {'A': 5, 'C': 10, 'G': 20, 'L': 13, 'O': 40, 'P': 10, 'F': 50, 'B': 5, 'M': 13, 'N': 13}
    connected = {'A': 0, 'C': 0, 'G': 0, 'L': 0, 'O': 0, 'P': 0, 'F': 0, 'B': 0, 'M': 0, 'N': 0}
    priority = {'A': 2**9, 'C': 2**8, 'G': 2**7, 'L': 2**6, 'O': 2**5, 'P': 2**4, 'F': 2**3,
                'B': 2**2, 'M': 2**1, 'N': 2**0}


    connected, remainingEnergy = init(source, remainingEnergy, cost, connected)
    
    # Calculate shortest distance from the source to each node.
    # Returns the dictionary distFromSource and the list prevToSource.
    distFromSource, prevToSource = dijkstra(nodes, distances, source)

    for currNode in nodes[1:]:

        if not connected[currNode]:
            # Connect current node immediately if the remaining energy is sufficient, and it has a connected neighbour
            if remainingEnergy >= cost[currNode]:
                for neighbour in neighbours[currNode]:
                    if connected[neighbour]:
                        connected[currNode] = 1
                        remainingEnergy -= cost[currNode]
                        break

        if not connected[currNode]:
            # Find shortest path from current node to all predecessors
            distFromCurr, prevToCurr = dijkstra(nodes, distancesInverted, currNode)

            # connList is a list of nodes, on the shortest path from the current node to A, that are connected
            connList = []
            prevNode = prevToSource[currNode]

            # Add all nodes on path to A to connList
            while prevNode != None:
                if connected[prevNode]:
                    connList.append(prevNode)
                prevNode = prevToSource[prevNode]

            closestConnNode = connList[0]
            currShortestDist = distFromCurr[connList[0]]

            # Check if there exists a shorter path between currNode and the corrently connected nodes
            for node in nodes:
                if connected[node] and node not in connList:
                    if distFromCurr[node] < currShortestDist:
                        currShortestDist = distFromCurr[node]
                        closestConnNode = node

            # Create trial states to enable testing of feasability of operation.
            # This is one way to ensure that we disconnect nodes of lower priority whenever possible and
            # necessary in order to connect a node of higher priority.
            if currShortestDist <= remainingEnergy + potentialEnergy:
                trialConnected = connected
                trialEnergy = remainingEnergy
                trialPotential = potentialEnergy

                # When the closest connected node is not on the path to A, we use the path from this connected
                # node to the current node to add all the needed nodes in between. Otherwise, we use the
                # path from A to the current.
                if closestConnNode != connList[0]:
                    prevNode = prevToCurr[closestConnNode]
                else:
                    prevNode = prevToSource[currNode]

                while prevNode != None and not connected[prevNode]:
                    trialConnected[prevNode] = 1
                    trialEnergy -= cost[prevNode]
                    if priority[prevNode] < priority[currNode]:
                        trialPotential += cost[prevNode]

                trialConnected[currNode] = 1
                trialEnergy -= cost[currNode]

                # Disconnect a node whenever its priority is lower than the current node,
                # and all the neighbours of this node have paths to the source (A) that do not include it (the node with lower priority)
                # We iterate through the reversed list of nodes to ensu
                for node in reversed(nodes):
                    if trialConnected[node] and priority[node] < priority[currNode]:
                        visited = [node]
                        nWithPath = 0 # Connected neighbours with alternate path(s) to A (that are not A)
                        nWithConn = 0 # Connected neighbours (that are not A)
                        for neighbour in neighbours[node]:
                            if neighbour != source and trialConnected[neighbour]:
                                nWithConn += 1

                                if findPathToSource(neighbour, visited, neighbours, source, trialConnected):
                                    nWithPath += 1

                        if nWithPath == nWithConn:
                            trialConnected[node] = 0
                            trialEnergy += cost[node]
                            trialPotential -= cost[node]

                if trialEnergy >= 0:
                    connected = trialConnected
                    remainingEnergy = trialEnergy
                    potentialEnergy = trialPotential

    print("NODE LIST: ", connected)


def init(source, remainingEnergy, cost, connected):
    if cost[source] <= remainingEnergy:
        connected[source] = 1
        remainingEnergy -= cost[source]
        return connected, remainingEnergy

    else:
        print("Insufficient energy to connect any nodes")
        exit()


def findPathToSource(node, visited, neighbours, source, connected):
    visited.append(node)
    if node == source:
        return 1
    else:
        for neighbour in neighbours[node]:
            if (neighbour not in visited) and connected[neighbour]:
                return findPathToSource(neighbour,visited,neighbours,source,connected  )
        return 0


def dijkstra(nodes, distances, source):
    unvisited = {node: float("inf") for node in nodes}
    previous = {node: None for node in nodes}
    visited = {}
    current = source
    currentDistance = 0
    previous[source] = None
    unvisited[source] = currentDistance

    while True:
        for successor, distance in distances[current].items():
            if successor not in unvisited: continue
            newDistance = currentDistance + distance

            if unvisited[successor] is None or unvisited[successor] > newDistance:
                unvisited[successor] = newDistance
                previous[successor] = current

        visited[current] = currentDistance
        del unvisited[current]
        if not unvisited:
            break

        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0] # Sorting on current distance from source

    return visited, previous


if __name__== "__main__":
  main()
