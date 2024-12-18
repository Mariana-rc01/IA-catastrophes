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

def main():
    ## SETUP
    # Load dataset
    state = load_dataset("data/dataset1.json")

    # TODO: Load extra data from dataset
    #state = State(0, [], None, [], graph)

    ## Load main window
    #root = tk.Tk()
    #app = Viewer(root)
    #app.display_graph(state.graph)
    #app.run()

    print("Supplies iniciais no start_point:", {s.type.name: s.quantity for s in state.start_point.supplies})

    # Example
    #path, total_distance, supplies_info = bfs_supply_delivery(state, state.start_point, state.end_points[0])
    path, total_distance, supplies_info = dfs_supply_delivery(state, state.start_point, state.end_points[0])
    #path, total_distance, supplies_info = ids_supply_delivery(state, state.start_point, state.end_points[0])
    #path, total_distance, supplies_info = ucs_supply_delivery(state, state.start_point, state.end_points[0])
    #path, total_distance, supplies_info = a_star_supply_delivery(state, state.start_point, state.end_points[0], final_combined_heuristic)
    #path, total_distance, supplies_info = a_star_supply_delivery(state, state.start_point, state.end_points[0], manhattan_heuristic)
    #path, total_distance, supplies_info = greedy_supply_delivery(state, state.start_point, state.end_points[0], manhattan_heuristic)
    
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

if __name__ == '__main__':
    main()
