from geography.geography import load_map_data_to_graph
from ui.viewer import Viewer
import tkinter as tk
import json

class State:
    def __init__(self, time, vehicles, start_point, end_points, graph):
        self.time = time
        self.vehicles = vehicles
        self.start_point = start_point
        self.end_points = end_points
        self.graph = graph

def main():
    ## SETUP
    # Load dataset
    with open("data/dataset1.json", 'r') as file:
        dataset = json.load(file)

    geography = dataset['geography']
    graph = load_map_data_to_graph(geography)

    # TODO: Load extra data from dataset
    state = State(0, [], None, [], graph)

    ## Load main window
    root = tk.Tk()
    app = Viewer(root)
    app.display_graph(state.graph)
    app.run()

if __name__ == '__main__':
    main()
