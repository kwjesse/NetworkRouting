from CS4412Graph import *
import math
from Node import *

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class UnsortedArray:
    def __init__(self, network, source):
        assert (type(network) == CS4412Graph)
        self.network = network
        self.source = source
        self.unsortedArray = []
        self.currentSize = 0

    # Calculates the Euclidean distance between two nodes
    def calculate_distance(self, point1, point2):
        dist = math.sqrt((point1.x() - point2.x()) ** 2 + (point1.y() - point2.y()) ** 2)
        return dist * 100

    # Inserts the distance into the specified index
    def insert(self, index, dist):
        self.unsortedArray[index].distance = dist
        self.currentSize += 1

    # Updates the distance of the node
    def decrease_key(self, index, dist):
        self.unsortedArray[index].distance = dist

    """Finds and deletes the min node"""
    def delete_min(self):
        min_node_index = 0
        is_found = False
        for i in range(0, len(self.unsortedArray)):
            # If the node was already deleted
            if is_found and self.unsortedArray[i].distance == -1:
                continue
            # If the distance is smaller, set the minimum node index to the current index
            elif is_found and self.unsortedArray[i].distance < self.unsortedArray[min_node_index].distance:
                min_node_index = i
            # Find the starting index for the minimum node index
            elif not is_found and (self.unsortedArray[i].distance == float("inf") or self.unsortedArray[i].distance == -1):
                min_node_index += 1
            elif not is_found and self.unsortedArray[i].distance != -1 and self.unsortedArray[i].distance != float("inf"):
                is_found = True
                if self.currentSize == 1:
                    break
        min_node = self.unsortedArray[min_node_index]
        self.currentSize -= 1
        return min_node

    # Populate the unsorted array with unvisted nodes and insert the source node into the unsorted array
    def make_array(self):
        self.unsortedArray = [Node(x, float("inf"), None, self.network.nodes[x].loc, self.network.nodes[x].neighbors) for x in range(len(self.network.nodes))]
        self.insert(self.source, 0.0)

    # Finds the shortest paths between nodes in the graph
    def Dijkstra(self):
        self.make_array()
        shortest_paths = []
        while self.currentSize > 0:
            min_node = self.delete_min()
            shortest_paths.append(min_node)
            # For all edges of min_node
            for i in range(len(min_node.neighbors)):
                neighbor_id = min_node.neighbors[i].dest.node_id
                # If the neighbor was already deleted
                if self.unsortedArray[neighbor_id].distance == -1:
                    continue
                dist = self.calculate_distance(min_node.loc, self.network.nodes[neighbor_id].loc) + min_node.distance
                # If the neighbor is not visited, insert into the unsorted array
                if self.unsortedArray[neighbor_id].distance == float("inf"):
                    self.insert(neighbor_id, dist)
                    self.unsortedArray[neighbor_id].previous = min_node
                # Update the distance value if a shorter distance
                elif dist < self.unsortedArray[neighbor_id].distance:
                    self.decrease_key(neighbor_id, dist)
                    self.unsortedArray[neighbor_id].previous = min_node
            self.unsortedArray[min_node.node_id].distance = -1
        return shortest_paths