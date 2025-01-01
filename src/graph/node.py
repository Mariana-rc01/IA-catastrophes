import weather

class Node:
    def __init__(self, position, id):
        self.id = id
        self.position = position
        self.neighbours = []  # List of tuples (Node, open: bool)
        self.accessible_terrains = [0,1,2] # List of Terrain

    def can_access_terrain(self, terrain, weather):
        return terrain in self.accessible_terrains and not weather.blocked_position(self.position)