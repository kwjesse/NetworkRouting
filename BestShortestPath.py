

class BestShortestPath:
    def __init__(self):
        pass

    # Finds the shortest path between the source node and destination node
    def getBestShortestPath(self, destIndex, shortest_paths):
        best_shortest_path = []
        dest_pos = -1
        # Find destination index
        for x in range(len(shortest_paths)):
            if shortest_paths[x].node_id == destIndex:
                dest_pos = x
                best_shortest_path.insert(0, shortest_paths[x])
                break
        # If destination not found
        if dest_pos == -1:
            return best_shortest_path
        next_pos = dest_pos
        for x in range(dest_pos - 1, 0, -1):
            # Find the previous node and insert the node into the front of the list
            if shortest_paths[x].node_id == shortest_paths[next_pos].previous.node_id:
                best_shortest_path.insert(0, shortest_paths[x])
                next_pos = x
        # Insert the source node
        best_shortest_path.insert(0, shortest_paths[0])
        return best_shortest_path




