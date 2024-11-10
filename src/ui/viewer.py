from tkinter import *

from ui.graph_canvas import GraphCanvas

class Viewer:
    def __init__(self, root):
        self.root = root
        root.geometry("1200x600")
        root.title("Inteligência Artificial - Simulador")

        self.canvas = GraphCanvas(root, width=1200, height=600, bg="white")
        self.canvas.pack()

        self.setup_ui()

    def setup_ui(self):
        menu = Menu(self.root)
        menu.add_command(label="▶️")
        self.root.config(menu=menu)

    def display_graph(self, graph):
        # Determine min and max coordinates to scale
        min_x = min(node.position.x for node in graph.nodes.values())
        max_x = max(node.position.x for node in graph.nodes.values())
        min_y = min(node.position.y for node in graph.nodes.values())
        max_y = max(node.position.y for node in graph.nodes.values())

        # Function to scale coordinates
        def scale(x, y):
            scaled_x = 50 + (x - min_x) / (max_x - min_x) * 700
            scaled_y = 50 + (y - min_y) / (max_y - min_y) * 500
            return scaled_x, scaled_y

        # Draw edges
        for node in graph.nodes.values():
            for neighbour, open in node.neighbours:
                x1, y1 = scale(node.position.x, node.position.y)
                x2, y2 = scale(neighbour.position.x, neighbour.position.y)
                self.canvas.create_line(x1, y1, x2, y2, fill="black" if open else "red")

        # Draw nodes
        for node in graph.nodes.values():
            x, y = scale(node.position.x, node.position.y)
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="blue")

    def run(self):
        self.root.mainloop()