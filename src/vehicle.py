from enum import Enum

from weather import Weather, WeatherCondition

class VehicleStatus(Enum):
    IDLE = 0
    BUSY = 1

class Transportation(Enum):
    LAND = 0
    AIR = 1
    SEA = 2

class VehicleType:
    def __init__(self, name, transportation, fuel_capacity, weight_capacity, volume_capacity, average_velocity):
        self.name = name
        self.transportation = transportation
        self.fuel_capacity = fuel_capacity
        self.weight_capacity = weight_capacity
        self.volume_capacity = volume_capacity
        self.average_velocity = average_velocity

    def adjust_velocity(self, weather):
        if weather == WeatherCondition.STORM:
            return self.average_velocity * 0.5
        elif weather == WeatherCondition.SNOWY:
            return self.average_velocity * 0.75
        elif weather == WeatherCondition.RAINY:
            return self.average_velocity * 0.9
        return self.average_velocity

    def can_access_terrain(self, terrain):
        return self.transportation == terrain

class Vehicle:
    def __init__(self, id, position, type, current_fuel, current_weight, current_volume, vehicle_status):
        self.id = id
        self.position = position
        self.type = type
        self.current_fuel = current_fuel
        self.current_weight = current_weight
        self.current_volume = current_volume
        self.vehicle_status = vehicle_status