from geography.geography import load_map_data_to_graph
from ui.viewer import Viewer
import tkinter as tk
from algorithms.uninformed.bfs import bfs_supply_delivery
from algorithms.uninformed.dfs import dfs_supply_delivery
from algorithms.uninformed.iterative_deepening import ids_supply_delivery
from algorithms.uninformed.uniform_cost import ucs_supply_delivery
from algorithms.informed.greedy import greedy_supply_delivery
from algorithms.informed.a_star import a_star_supply_delivery
from algorithms.informed.heuristics import manhattan_heuristic, time_estimation_heuristic, blocked_route_heuristic, dynamic_supply_priority_heuristic, delivery_success_probability_heuristic, final_combined_heuristic
from load_dataset import load_dataset

algorithm = "bfs"  # Default algorithm

def main():
    global algorithm

    ## SETUP
    # Load dataset
    state = load_dataset("data/dataset1.json")

    # Initialize the Viewer and pass a callback to update the algorithm
    root = tk.Tk()
    app = Viewer(root, lambda selected_algorithm: set_algorithm(selected_algorithm))
    app.display_graph(state.graph, state.start_point, state.end_points)
    app.run()

    print("Supplies iniciais no start_point:", {s.type.name: s.quantity for s in state.start_point.supplies})

    # Select the appropriate algorithm
    algorithm_functions = {
        "bfs": bfs_supply_delivery,
        "dfs": dfs_supply_delivery,
        "ids": ids_supply_delivery,
        "ucs": ucs_supply_delivery,
        "a_star": lambda state, start, end, cost: a_star_supply_delivery(state, start, end, final_combined_heuristic, cost),
        "greedy": lambda state, start, end, cost: greedy_supply_delivery(state, start, end, manhattan_heuristic, cost),
    }
    selected_function = algorithm_functions.get(algorithm)

    if selected_function:
        path, total_distance, supplies_info = selected_function(state, state.start_point, state.end_points[0], 0)
        if path:
            print("Caminho encontrado:", path)
            print("Distância total:", total_distance)
            print("Supplies enviados por veículo:", supplies_info)
            print("Supplies restantes no start_point:", {s.type.name: s.quantity for s in state.start_point.supplies})
            print("Supplies necessários no end_point:", state.end_points[0].get_supplies_needed())
        else:
            print("Nenhum caminho disponível.")
            print(f"{supplies_info}")
            print("Supplies restantes no start_point:", {s.type.name: s.quantity for s in state.start_point.supplies})

def set_algorithm(selected_algorithm):
    global algorithm
    algorithm = selected_algorithm
    print(f"Algorithm globally updated to: {algorithm}")

if __name__ == '__main__':
    main()
