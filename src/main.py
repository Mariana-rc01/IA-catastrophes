from geography.geography import load_map_data_to_graph
from ui.viewer import Viewer
import tkinter as tk
from algorithms.uninformed.bfs import bfs_supply_delivery
from algorithms.uninformed.dfs import dfs_supply_delivery
from algorithms.uninformed.iterative_deepening import ids_supply_delivery
from algorithms.uninformed.uniform_cost import ucs_supply_delivery
from algorithms.informed.greedy import greedy_supply_delivery
from algorithms.informed.a_star import a_star_supply_delivery
from algorithms.informed.heuristics import manhattan_heuristic, final_combined_heuristic
from load_dataset import load_dataset
import time

algorithm = "bfs"  # Default algorithm
app = None
state = None

def main():
    global algorithm
    global app
    global state

    state = load_dataset("data/dataset1.json")

    root = tk.Tk()
    app = Viewer(
        root,
        algorithm_callback=lambda selected_algorithm: set_algorithm(selected_algorithm),
        start_simulation_callback=lambda: run_algorithm(state),
        restart_simulation_callback=lambda: restart_simulation()
    )
    app.display_graph(state.graph, state.start_point, state.end_points, state.vehicles)
    app.run()

def set_algorithm(selected_algorithm):
    global algorithm
    algorithm = selected_algorithm
    print(f"Algorithm updated to: {algorithm}")

def run_algorithm(state):
    global algorithm
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
            print("Path found.")
        else:
            print("No available path.")

    app.draw_path(state.graph, path, on_complete=lambda: app.display_graph(state.graph, state.start_point, state.end_points, state.vehicles))

def restart_simulation():
    global state
    state = load_dataset("data/dataset1.json")
    print("Simulation restarted.")
    app.display_graph(state.graph, state.start_point, state.end_points, state.vehicles)

if __name__ == '__main__':
    main()
