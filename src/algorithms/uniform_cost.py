import heapq
from collections import deque
import vehicle as vh
import supply as sp
from graph.node import Node
from algorithms.supplies_per_vehicles import split_supplies_per_vehicle
from algorithms.manhattan_distance import manhattan_distance

def ucs_supply_delivery(state, start_point, end_point):
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
        for vehicle, supplies in zip(vehicles, supplies_per_vehicle):
            if supplies:
                vehicle.position = end_point.position
                vehicle.vehicle_status = vh.VehicleStatus.BUSY
                vehicle.current_fuel -= total_distance

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
            return None, 0, "There aren't any available vehicles."

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
                [str(position) for position in path + [end_point.position]],
                total_distance,
                {
                    vehicle.id: [s.type.name for s in supplies]
                    for vehicle, supplies in zip(vehicles, supplies_per_vehicle)
                },
            )

        current_node = state.graph.nodes.get(current_position)
        if current_node:
            for neighbor in current_node.neighbours:
                neighbor_position, is_open = neighbor

                if is_open and neighbor_position not in visited:
                    if isinstance(neighbor_position, Node):
                        neighbor_position = neighbor_position.position
                    new_distance = total_distance + manhattan_distance(
                        current_position, neighbor_position
                    )
                    heapq.heappush(
                        pq,
                        (new_distance, neighbor_position, path + [neighbor_position]),
                    )

    return None, 0, "No path found."
