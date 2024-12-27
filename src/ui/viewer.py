from os import path
from tkinter import *
from PIL import Image, ImageTk  # Import Pillow for image resizing

from ui.graph_canvas import GraphCanvas

algorithms = {
    "bfs": "Breadth-first search",
    "dfs": "Depth-first search",
    "ids": "Iterative deepening depth-first search",
    "ucs": "Uniform-Cost search",
    "a_star": "A* search",
    "greedy": "Greedy search",
}

class Viewer:
    def __init__(self, root, algorithm_callback):
        self.root = root
        self.algorithm_callback = algorithm_callback
        root.geometry("1200x600")
        root.title("Inteligência Artificial - Simulador")

        self.canvas = GraphCanvas(root, width=1200, height=600, bg="white")
        self.canvas.pack()

        self.selected_algorithm = list(algorithms.keys())[0]
        self.setup_ui()

        end_image_path = path.join(path.dirname(__file__), "..", "assets", "images", "end_position.png")
        self.original_end_point_image = Image.open(end_image_path)

        start_image_path = path.join(path.dirname(__file__), "..", "assets", "images", "start_position.png")
        self.original_start_point_image = Image.open(start_image_path)

        self.tooltip = Label(root, text="", bg="white", fg="black", bd=1, relief=SOLID, padx=5, pady=2)
        self.tooltip.place_forget()

        self.images_on_canvas = []

    def setup_ui(self):
        menu = Menu(self.root)

        menu.add_command(label="▶️", command=lambda: print("Simulation started"))

        algorithm_menu = Menu(menu, tearoff=0)

        for algo_key, algo_name in algorithms.items():
            algorithm_menu.add_command(label=algo_name, command=lambda key=algo_key: self.select_algorithm(key))

        menu.add_cascade(label=f"Algorithm: {self.selected_algorithm.upper()}", menu=algorithm_menu)

        self.root.config(menu=menu)

    def update_menu_label(self):
        """Refresh the menu to update the label dynamically."""
        self.setup_ui()

    def show_tooltip(self, event, text):
        self.tooltip.config(text=text)
        self.tooltip.place(x=event.x_root - self.root.winfo_rootx() + 10,
                           y=event.y_root - self.root.winfo_rooty() + 10)

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

    def display_graph(self, graph, start_point, end_points):
        # Determine min and max coordinates to scale
        min_x = min(node.position.x for node in graph.nodes.values())
        max_x = max(node.position.x for node in graph.nodes.values())
        min_y = min(node.position.y for node in graph.nodes.values())
        max_y = max(node.position.y for node in graph.nodes.values())

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
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

        # Draw start point
        x, y = scale(start_point.position.x, start_point.position.y)
        start_image = self.original_start_point_image.resize((30, 30), Image.ANTIALIAS)
        tk_start_image = ImageTk.PhotoImage(start_image)
        self.images_on_canvas.append(tk_start_image)  # Keep reference
        start_id = self.canvas.create_image(x, y, image=tk_start_image, anchor=CENTER)

        supplies_text = "Contains: \n" + "\n".join(f"{supply.type}: {supply.quantity}" for supply in start_point.supplies)

        # Add tooltip for the start point
        self.canvas.tag_bind(start_id, "<Enter>", lambda e, t=supplies_text: self.show_tooltip(e, t))
        self.canvas.tag_bind(start_id, "<Leave>", self.hide_tooltip)

        # Draw end points
        for end_point in end_points:
            x, y = scale(end_point.position.x, end_point.position.y)
            end_image = self.original_end_point_image.resize((30, 30), Image.ANTIALIAS)
            tk_end_image = ImageTk.PhotoImage(end_image)
            self.images_on_canvas.append(tk_end_image)  # Keep reference
            end_id = self.canvas.create_image(x, y, image=tk_end_image, anchor=CENTER)

            needed_supplies_text = "Needed supplies: \n" + "\n".join(
                f"{supply_type}: {quantity}" for supply_type, quantity in end_point.get_supplies_needed().items()
            )

            self.canvas.tag_bind(end_id, "<Enter>", lambda e, t=needed_supplies_text: self.show_tooltip(e, t))
            self.canvas.tag_bind(end_id, "<Leave>", self.hide_tooltip)

    def run(self):
        self.root.mainloop()

    def select_algorithm(self, selected_algorithm):
        self.algorithm_callback(selected_algorithm)
        self.selected_algorithm = selected_algorithm
        self.update_menu_label()
