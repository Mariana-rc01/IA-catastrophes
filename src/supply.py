from enum import Enum

class SupplyType(Enum):
    Water = 0,
    Food = 1,
    Medicine = 2

def get_weight_volume_per_supply(supply_type):
    if supply_type == SupplyType.Water:
        return (1, 1)
    elif supply_type == SupplyType.Food:
        return (1.2, 1.2)
    elif supply_type == SupplyType.Medicine:
        return (0.5, 0.5)

class Supply:
    def __init__(self, quantity, type):
        self.quantity = quantity
        self.type = type    