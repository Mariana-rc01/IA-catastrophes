class Node:
    def __init__(self, position):
        self.position = position
        self.neighbours = []  # List of tuples (Node, open: bool)