from geography.geography import load_map_data_to_graph
from ui.viewer import Viewer
import tkinter as tk
from algorithms.bfs import bfs_supply_delivery
from algorithms.uniform_cost import ucs_supply_delivery
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
    path, total_distance, supplies_info = ucs_supply_delivery(state, state.start_point, state.end_points[0])
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


