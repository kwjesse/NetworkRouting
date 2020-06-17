#!/usr/bin/python3


from CS4412Graph import *
from Distance import *
from Node import *
from BestShortestPath import *
from BinaryHeap import *
from UnsortedArray import *
import time
import math

class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert (type(network) == CS4412Graph)
        self.network = network
        self.distance = Distance()

    def calculate_distance(self, point1, point2):
        dist = math.sqrt((point1.x() - point2.x())**2 + (point1.y() - point2.y())**2)
        return dist*100

    # Determine the shortest path between the source node and destination node
    def getShortestPath(self, destIndex):
        self.dest = destIndex
        path_edges = []
        total_length = 0

        # Get shortest path
        shortest_path = BestShortestPath()
        self.distance.best_shortest_path = shortest_path.getBestShortestPath(self.dest, self.distance.shortest_paths)

        # If the destination node is not found, return unreachable
        if len(self.distance.best_shortest_path) == 0:
            return {'cost': float('inf'), 'path': path_edges}

        edges_left = len(self.distance.best_shortest_path)-1
        node = self.network.nodes[self.source]
        cur = 1
        while edges_left > 0:
            for next in range(len(node.neighbors)):
                # Determine which neighbor is the next node
                if node.neighbors[next].dest.node_id == self.distance.best_shortest_path[cur].node_id:
                    # Add the edge to the list
                    edge = node.neighbors[next]
                    path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
                    total_length += edge.length
                    node = edge.dest
                    edges_left -= 1
                    cur += 1
                    break
        return {'cost': total_length, 'path': path_edges}

    # Determine the shortest paths of the graph using an unsorted array or a binary heap
    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        if use_heap:
            array = BinaryHeap(self.network, self.source)
            self.distance.shortest_paths = array.Dijkstra()
        else:
            array = UnsortedArray(self.network, self.source)
            self.distance.shortest_paths = array.Dijkstra()
        t2 = time.time()
        return (t2 - t1)


