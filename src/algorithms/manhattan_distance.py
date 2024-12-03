from graph.node import Node

def manhattan_distance(p1, p2):
    if isinstance(p1, Node):
        p1 = p1.position
    if isinstance(p2, Node):
        p2 = p2.position

    return abs(p1.x - p2.x) + abs(p1.y - p2.y)