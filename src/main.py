from algorithms.informed import heuristics
from geography.geography import load_map_data_to_graph
from graph.position import Position
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

from weather import Weather, WeatherCondition

algorithm = "bfs"  # Default algorithm
app = None
state = None
heuristic = "manhattan_heuristic"  # Default heuristic

def main():
    global algorithm
    global app
    global state

    state = load_dataset("data/dataset1.json")

    root = tk.Tk()
    app = Viewer(
        root,
        algorithm_callback=lambda selected_algorithm, blocked_routes, selected_heuristic: set_algorithm(selected_algorithm, blocked_routes, selected_heuristic),
        start_simulation_callback=lambda: run_algorithm(state),
        restart_simulation_callback=lambda: restart_simulation(),
        endpoints_callback=lambda: get_endpoints()
    )
    app.display_graph(state.graph, state.start_point, state.end_points, state.vehicles)
    app.run()

def set_algorithm(selected_algorithm, blocked_routes, selected_heuristic):
    global algorithm
    algorithm = selected_algorithm
    heuristic = selected_heuristic
    print(f"Algorithm updated to: {algorithm}")
    print(f"Blocked routes: {blocked_routes}")

def get_endpoints():
    return state.end_points

def run_algorithm(state):
    global algorithm
    algorithm_functions = {
        "bfs": bfs_supply_delivery,
        "dfs": dfs_supply_delivery,
        "ids": ids_supply_delivery,
        "ucs": ucs_supply_delivery,
        "a_star": lambda state, start, end, terrain, weather, blocked_routes: a_star_supply_delivery(
            state, start, end, getattr(heuristics, heuristic), terrain, weather, blocked_routes
        ),
        "greedy": lambda state, start, end, terrain, weather, blocked_routes: greedy_supply_delivery(
            state, start, end, getattr(heuristics, heuristic), terrain, weather, blocked_routes
        ),
    }
    selected_function = algorithm_functions.get(algorithm)

    if selected_function:
        # Create the Weather object
        weather = Weather()

        # Set weather conditions
        position = Position(-8.3969801, 41.5588274)
        weather.set_condition(position, WeatherCondition.SUNNY)

        selected_end_point = state.end_points[app.selected_end_point_index]

        # Pass blocked_routes as an additional argument
        path, total_distance, total_time, supplies_info = selected_function(
            state, 
            state.start_point, 
            selected_end_point, 
            0, 
            weather,
            app.blocked_routes  # Pass blocked routes here
        )
        if path:
            print("Path found.")
        else:
            print("No available path.")

        app.show_info_box(total_distance*100, total_time*60)
    app.draw_path(state.graph, path, on_complete=lambda: app.display_graph(state.graph, state.start_point, state.end_points, state.vehicles))


def restart_simulation():
    global state
    state = load_dataset("data/dataset1.json")
    print("Simulation restarted.")
    app.display_graph(state.graph, state.start_point, state.end_points, state.vehicles)

if __name__ == '__main__':
    main()
