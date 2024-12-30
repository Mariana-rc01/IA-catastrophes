from collections import deque
from supply import SupplyType, Supply
from vehicle import VehicleStatus
from algorithms.supplies_per_vehicles import split_supplies_per_vehicle
from algorithms.utils import manhattan_distance
from weather import WeatherCondition

def dfs_supply_delivery(state, start_point, end_point, terrain, weather, blocked_routes):
    # Check needed supplies
    needed_supplies = end_point.supplies_needed
    available_supplies = start_point.supplies

    # Separate the available and required supplies
    supplies_to_send = []
    supplies_consumed = {supply_type: 0 for supply_type in SupplyType}
    for needed_type, needed_quantity in needed_supplies.items():
        total_available = sum(s.quantity for s in available_supplies if s.type == SupplyType[needed_type])
        if total_available >= needed_quantity:
            supplies_to_send.append(Supply(needed_quantity, SupplyType[needed_type]))
            supplies_consumed[SupplyType[needed_type]] = needed_quantity
        else:
            supplies_to_send.append(Supply(total_available, SupplyType[needed_type]))
            supplies_consumed[SupplyType[needed_type]] = total_available

    # DFS
    visited = set()
    stack = [(start_point.position, [], 0)]

    while stack:
        current_position, path, total_distance = stack.pop()

        if current_position in visited:
            continue

        visited.add(current_position)

        if current_position == end_point.position:
            # Split supplies per vehicle
            vehicles = [v for v in state.vehicles
                        if v.position == start_point.position and v.vehicle_status == VehicleStatus.IDLE
                        and v.current_fuel >= total_distance and v.type.can_access_terrain(terrain)]
            supplies_per_vehicle = split_supplies_per_vehicle(vehicles, supplies_to_send)

            total_time = 0
            for vehicle, supplies in zip(vehicles, supplies_per_vehicle):
                if supplies:
                    vehicle.position = end_point.position
                    vehicle.vehicle_status = VehicleStatus.BUSY
                    vehicle.current_fuel -= total_distance

                    for i in range(len(path) - 1):
                        start_pos = path[i]
                        end_pos = path[i + 1]
                        
                        weather_condition = weather.get_condition(start_pos)
                        velocity = vehicle.type.adjust_velocity(weather_condition)
                        distance = manhattan_distance(start_pos, end_pos)
                        
                        time_for_vehicle = distance / velocity if velocity > 0 else float('inf')
                        
                        total_time += time_for_vehicle

            if supplies_per_vehicle:
                for supply_type, quantity_used in supplies_consumed.items():
                    if quantity_used > 0:
                        for supply in available_supplies:
                            if supply.type == supply_type:
                                if supply.quantity >= quantity_used:
                                    supply.quantity -= quantity_used
                                    end_point.satisfy_supplies([Supply(quantity_used, supply_type)])
                                    break
                                else:
                                    quantity_used -= supply.quantity
                                    end_point.satisfy_supplies([Supply(supply.quantity, supply_type)])
                                    supply.quantity = 0
            else:
                return None, 0, 0, print("There aren't any available vehicles.")

            return ([start_point.position] + path, total_distance, total_time,
                {vehicle.id: [s.type.name for s in supplies] for vehicle, supplies in zip(vehicles, supplies_per_vehicle)})

        current_node = state.graph.nodes.get(current_position)
        if current_node:
            for neighbor, is_open in reversed(current_node.neighbours):
                route1, route2 = f'{current_node.id},{neighbor.id}', f'{neighbor.id},{current_node.id}'
                if is_open and neighbor.position not in visited and neighbor.can_access_terrain(terrain, weather) and route1 not in blocked_routes and route2 not in blocked_routes:
                    weather_condition = weather.get_condition(neighbor.position)
                    distance = manhattan_distance(current_position, neighbor.position)

                    # We adjust the distance based on the weather conditions
                    if weather_condition == WeatherCondition.SNOWY:
                        distance *= 1.25
                    elif weather_condition == WeatherCondition.RAINY:
                        distance *= 1.1

                    new_distance = total_distance + distance
                    stack.append((neighbor.position, path + [neighbor.position], new_distance))

    return None, 0, 0, "No path found."
