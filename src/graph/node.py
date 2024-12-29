import weather

class Node:
    def __init__(self, position, priority):
        self.position = position
        self.neighbours = []  # List of tuples (Node, open: bool)
        self.accessible_terrains = [0,1,2] # List of Terrain
        self.priorityZone = 0

    def can_access_terrain(self, terrain, weather):
        return terrain in self.accessible_terrains and not weather.blocked_position(self.position)