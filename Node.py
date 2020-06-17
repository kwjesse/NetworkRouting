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


class Node:

    def __init__(self, node_id, distance, previous, loc, neighbors):
        self.node_id = node_id
        self.distance = distance
        self.previous = previous
        self.loc = loc
        self.neighbors = neighbors
