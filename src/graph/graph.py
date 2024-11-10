from graph.node import Node
from graph.position import Position

class Graph:
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, position):
        if position not in self.nodes:
            self.nodes[position] = Node(position)

    def add_edge(self, pos1, pos2, open=True):
        if pos1 in self.nodes and pos2 in self.nodes:
            self.nodes[pos1].neighbours.append((self.nodes[pos2], open))
            self.nodes[pos2].neighbours.append((self.nodes[pos1], open))