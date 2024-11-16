class EndPoint:
    def __init__(self, position, supplies_needed):
        self.position = position
        self.supplies_needed = supplies_needed

    def get_supplies_needed(self):
        return {supply_type: quantity for supply_type, quantity in self.supplies_needed.items() if quantity > 0}
    
    def satisfy_supplies(self, supplies):
        for supply in supplies:
            if supply.type.name in self.supplies_needed:
                self.supplies_needed[supply.type.name] = max(0, self.supplies_needed[supply.type.name] - supply.quantity)

