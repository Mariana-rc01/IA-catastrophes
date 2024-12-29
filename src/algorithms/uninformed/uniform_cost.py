import heapq
from collections import deque
import vehicle as vh
import supply as sp
from graph.node import Node
from algorithms.supplies_per_vehicles import split_supplies_per_vehicle
from algorithms.utils import manhattan_distance
from weather import WeatherCondition

def ucs_supply_delivery(state, start_point, end_point, terrain, weather):
    def get_supplies_to_send(needed_supplies, available_supplies):
        supplies_to_send = []
        supplies_consumed = {supply_type: 0 for supply_type in sp.SupplyType}
        for needed_type, needed_quantity in needed_supplies.items():
            total_available = sum(
                s.quantity
                for s in available_supplies
                if s.type == sp.SupplyType[needed_type]
            )
            if total_available >= needed_quantity:
                supplies_to_send.append(
                    sp.Supply(needed_quantity, sp.SupplyType[needed_type])
                )
                supplies_consumed[sp.SupplyType[needed_type]] = needed_quantity
            else:
                supplies_to_send.append(
                    sp.Supply(total_available, sp.SupplyType[needed_type])
                )
                supplies_consumed[sp.SupplyType[needed_type]] = total_available
        return supplies_to_send, supplies_consumed

    def update_vehicle_and_supplies(
        vehicles,
        supplies_per_vehicle,
        total_distance,
        supplies_consumed,
        available_supplies,
        end_point,
    ):
        total_time = 0
        supplies_info = {}
        for vehicle, supplies in zip(vehicles, supplies_per_vehicle):
            if supplies:
                vehicle.position = end_point.position
                vehicle.vehicle_status = vh.VehicleStatus.BUSY
                vehicle.current_fuel -= total_distance

                velocity = vehicle.type.average_velocity
                for position in path:
                    weather_condition = weather.get_condition(position)
                    velocity = vehicle.type.adjust_velocity(weather_condition)

                    time_for_vehicle = total_distance / velocity if velocity > 0 else float('inf')
                    total_time = max(total_time, time_for_vehicle)

                supplies_info[vehicle.id] = [s.type.name for s in supplies]

        if supplies_per_vehicle:
            for supply_type, quantity_used in supplies_consumed.items():
                if quantity_used > 0:
                    for supply in available_supplies:
                        if supply.type == supply_type:
                            if supply.quantity >= quantity_used:
                                supply.quantity -= quantity_used
                                end_point.satisfy_supplies(
                                    [sp.Supply(quantity_used, supply_type)]
                                )
                                break
                            else:
                                quantity_used -= supply.quantity
                                end_point.satisfy_supplies(
                                    [sp.Supply(supply.quantity, supply_type)]
                                )
                                supply.quantity = 0
        else:
            return None, 0, 0, "There aren't any available vehicles."
        
        return [start_point.position] + path, total_distance, total_time, supplies_info


    needed_supplies = end_point.supplies_needed
    available_supplies = start_point.supplies

    supplies_to_send, supplies_consumed = get_supplies_to_send(
        needed_supplies, available_supplies
    )

    pq = []
    heapq.heappush(pq, (0, start_point.position, []))
    visited = set()

    while pq:
        total_distance, current_position, path = heapq.heappop(pq)

        if current_position in visited:
            continue

        visited.add(current_position)

        if current_position == end_point.position:
            vehicles = [
                v
                for v in state.vehicles
                if v.position == start_point.position
                and v.vehicle_status == vh.VehicleStatus.IDLE
                and v.current_fuel >= total_distance
                and v.type.can_access_terrain(terrain)
            ]

            supplies_per_vehicle = split_supplies_per_vehicle(
                vehicles, supplies_to_send
            )

            result = update_vehicle_and_supplies(
                vehicles,
                supplies_per_vehicle,
                total_distance,
                supplies_consumed,
                available_supplies,
                end_point,
            )
            if result:
                return result

            return (
                [start_point.position] + path,
                total_distance,
                {
                    vehicle.id: [s.type.name for s in supplies]
                    for vehicle, supplies in zip(vehicles, supplies_per_vehicle)
                },
            )

        current_node = state.graph.nodes.get(current_position)
        if current_node:
            for neighbor, is_open in current_node.neighbours:
                if is_open and neighbor.position not in visited and neighbor.can_access_terrain(terrain, weather):
                    weather_condition = weather.get_condition(neighbor.position)
                    distance = manhattan_distance(current_position, neighbor.position)

                    # We adjust the distance based on the weather conditions
                    if weather_condition == WeatherCondition.SNOWY:
                        distance *= 1.25
                    elif weather_condition == WeatherCondition.RAINY:
                        distance *= 1.1

                    if isinstance(neighbor.position, Node):
                        neighbor.position = neighbor.position

                    new_distance = total_distance + distance
                    heapq.heappush(
                        pq,
                        (new_distance, neighbor.position, path + [neighbor.position]),
                    )

    return None, 0, 0, "No path found."
