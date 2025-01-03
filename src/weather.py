from enum import Enum

class WeatherCondition(Enum):
    SUNNY = 0
    RAINY = 1
    SNOWY = 2
    STORM = 3

class Weather:
    def __init__(self):
        self.conditions = {}

    def set_condition(self, position, condition):
        self.conditions[position] = condition

    def get_condition(self, position):
        return self.conditions.get(position)
    
    def blocked_position(self, position):
        return self.conditions[position] == WeatherCondition.STORM