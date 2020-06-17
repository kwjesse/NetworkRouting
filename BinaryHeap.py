from NetworkRoutingSolver import *
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


class BinaryHeap:
    def __init__(self, network, source):
        assert (type(network) == CS4412Graph)
        self.network = network
        self.source = source
        # insert dummy node into array for index 0, Binary Heap values start at index 1
        self.binaryHeapArray = [Node(-1, float("inf"), None, QPointF(0.0, 0.0), None)]
        self.pointerArray = [float("inf") for x in range(1, len(self.network.nodes)+1)]
        self.currentSize = 0

    # Calculates the Euclidean distance between two nodes
    def calculate_distance(self, point1, point2):
        dist = math.sqrt((point1.x() - point2.x())**2 + (point1.y() - point2.y())**2)
        return dist*100

    # Relocates the node to the correct position by swapping the parent with the child node
    def bubble_up(self, index):
        i = index
        parent = math.ceil(i/2)
        # While i is not the minNode and the distance of the child is less than the distance of the parent
        while i != 1 and self.binaryHeapArray[i].distance < self.binaryHeapArray[parent].distance:
            # Swap child and parent
            self.pointerArray[int(self.binaryHeapArray[i].node_id)], self.pointerArray[int(self.binaryHeapArray[parent].node_id)] = parent, i
            self.binaryHeapArray[i], self.binaryHeapArray[parent] = self.binaryHeapArray[parent], self.binaryHeapArray[i]
            i = parent
            parent = math.ceil(i/2)

    # Inserts node at the end of the binary heap and relocates the node to the correct position
    def insert(self, node, dist):
        node = Node(node.node_id, dist, float("inf"), node.loc, node.neighbors)
        self.binaryHeapArray.append(node)
        self.currentSize += 1
        self.pointerArray[node.node_id] = self.currentSize
        if self.currentSize != 1:
            self.bubble_up(self.currentSize)

    # Updates the distance of the node and relocate the node to correct position
    def decrease_key(self, index, dist):
        self.binaryHeapArray[int(self.pointerArray[index])].distance = dist
        self.bubble_up(int(self.pointerArray[index]))

    # Determines which child has the smallest distance
    def min_child(self, index):
        if 2 * index == self.currentSize:
            return index * 2 # Return only, left child
        elif 2 * index > self.currentSize:
            return 0  # No children
        else:
            # Determine the minimum child
            if self.binaryHeapArray[index*2].distance < self.binaryHeapArray[index*2+1].distance:
                return index * 2  # Return left child
            else:
                return index * 2 + 1 # Return right child

    # Swaps the root with its smallest child less than the root, repeats until the node is in the correct position
    def siftdown(self, index):
        i = index
        min_child = self.min_child(i)
        while min_child != 0 and self.binaryHeapArray[i].distance > self.binaryHeapArray[min_child].distance:
            # Swap parent and child
            self.pointerArray[self.binaryHeapArray[i].node_id], self.pointerArray[self.binaryHeapArray[min_child].node_id] = min_child, i
            self.binaryHeapArray[i], self.binaryHeapArray[min_child] = self.binaryHeapArray[min_child], self.binaryHeapArray[i]
            i = min_child
            min_child = self.min_child(i)

    """Deletes the min node and replace it with the last node of the binary heap array, 
       and relocates that node to the correct position """
    def delete_min(self):
        min_node = self.binaryHeapArray[1]
        # Update the pointer array
        self.pointerArray[min_node.node_id] = -1
        if self.currentSize != 1:
            self.pointerArray[self.binaryHeapArray[self.currentSize].node_id] = 1
        # Puts the last node into index 1
        self.binaryHeapArray[1] = self.binaryHeapArray[self.currentSize]
        # Delete last node
        self.binaryHeapArray.pop(self.currentSize)
        self.currentSize -= 1
        # Relocate the node at index 1 to the correct position
        if self.currentSize != 0:
            self.siftdown(1)
        return min_node

    # Insert the source node into the binary heap
    def make_heap(self):
        self.insert(self.network.nodes[self.source], 0.0)

    # Finds the shortest paths between nodes in the graph
    def Dijkstra(self):
        self.make_heap()
        shortest_paths = []
        while self.currentSize > 0:
            min_node = self.delete_min()
            shortest_paths.append(min_node)
            # For all edges of min_node
            for i in range(len(min_node.neighbors)):
                neighbor_id = min_node.neighbors[i].dest.node_id
                dist = self.calculate_distance(min_node.loc, self.network.nodes[neighbor_id].loc) + min_node.distance
                # If the neighbor was already deleted
                if self.pointerArray[neighbor_id] == -1:
                    continue
                # If the neighbor is not visited, insert into the binary heap
                elif self.pointerArray[neighbor_id] == float("inf"):
                    self.insert(self.network.nodes[neighbor_id], dist)
                    self.binaryHeapArray[int(self.pointerArray[neighbor_id])].previous = min_node
                # Update the distance value if a shorter distance
                elif dist < self.binaryHeapArray[int(self.pointerArray[neighbor_id])].distance:
                    self.decrease_key(neighbor_id, dist)
                    self.binaryHeapArray[int(self.pointerArray[neighbor_id])].previous = min_node
        return shortest_paths
