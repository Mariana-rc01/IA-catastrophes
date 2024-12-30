from os import path
from tkinter import *
from PIL import Image, ImageTk
from ui.graph_canvas import GraphCanvas
import time

algorithms = {
    "bfs": "Breadth-first search",
    "dfs": "Depth-first search",
    "ids": "Iterative deepening depth-first search",
    "ucs": "Uniform-Cost search",
    "a_star": "A* search",
    "greedy": "Greedy search",
}

class Viewer:
    def __init__(self, root, algorithm_callback, start_simulation_callback, restart_simulation_callback):
        self.root = root
        self.algorithm_callback = algorithm_callback
        self.start_simulation_callback = start_simulation_callback
        self.restart_simulation_callback = restart_simulation_callback
        root.geometry("1200x600")
        root.title("Inteligência Artificial - Simulador")

        self.canvas = GraphCanvas(root, width=1200, height=600, bg="white")
        self.canvas.pack()

        self.selected_algorithm = list(algorithms.keys())[0]
        self.setup_ui()

        self.blocked_routes = set()

        end_image_path = path.join(path.dirname(__file__), "..", "assets", "images", "end_position.png")
        self.original_end_point_image = Image.open(end_image_path)

        start_image_path = path.join(path.dirname(__file__), "..", "assets", "images", "start_position.png")
        self.original_start_point_image = Image.open(start_image_path)

        # TODO: Add other vehicle images
        vehicle_image_path = path.join(path.dirname(__file__), "..", "assets", "images", "truck.png")
        self.original_vehicle_image = Image.open(vehicle_image_path)

        square_image_path = path.join(path.dirname(__file__), "..", "assets", "images", "square.png")
        self.original_square_image = Image.open(square_image_path)

        self.tooltip = Label(root, text="", bg="white", fg="black", bd=1, relief=SOLID, padx=5, pady=2)
        self.tooltip.place_forget()

        self.images_on_canvas = []

    def setup_ui(self):
        menu = Menu(self.root)

        # Start Simulation button
        menu.add_command(label="▶ Start Simulation", command=self.start_simulation_callback)

        # Algorithm selection menu
        algorithm_menu = Menu(menu, tearoff=0)
        for algo_key, algo_name in algorithms.items():
            algorithm_menu.add_command(label=algo_name, command=lambda key=algo_key: self.select_algorithm(key))

        menu.add_cascade(label=f"⚙️ Algorithm: {self.selected_algorithm.upper()}", menu=algorithm_menu)
        self.root.config(menu=menu)

        # Restart simulation
        menu.add_command(label="↺ Restart", command=self.restart_simulation)

        # Block Route
        menu.add_command(label="Block Route", command=self.block_route_ui)

    def restart_simulation(self):
        self.blocked_routes.clear()
        self.restart_simulation_callback()

    def block_route_ui(self):
        block_route_window = Toplevel(self.root)
        block_route_window.title("Block Route")
        
        Label(block_route_window, text="Enter the route to block (format: node1,node2):").pack(pady=5)
        route_var = StringVar()
        Entry(block_route_window, textvariable=route_var).pack(pady=5)
        
        def confirm_block_route():
            route = route_var.get()
            if "," in route:
                self.block_route(route.strip())
                print(f"Blocked route: {route.strip()}")
                self.restart_simulation_callback()
            else:
                print("Invalid route format. Please use 'node1,node2'.")
            block_route_window.destroy()
        
        Button(block_route_window, text="Block", command=confirm_block_route).pack(pady=5)


    def update_menu_label(self):
        self.setup_ui()

    def show_tooltip(self, event, text):
        self.tooltip.config(text=text)
        self.tooltip.place(x=event.x_root - self.root.winfo_rootx() + 10,
                           y=event.y_root - self.root.winfo_rooty() + 10)

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

    def display_graph(self, graph, start_point, end_points, vehicles):
        self.canvas.delete("all")
        # Scale function for node positions
        min_x = min(node.position.x for node in graph.nodes.values())
        max_x = max(node.position.x for node in graph.nodes.values())
        min_y = min(node.position.y for node in graph.nodes.values())
        max_y = max(node.position.y for node in graph.nodes.values())

        def scale(x, y):
            scaled_x = 50 + (x - min_x) / (max_x - min_x) * 700
            scaled_y = 50 + (y - min_y) / (max_y - min_y) * 500
            return scaled_x, scaled_y

        # Draw edges
        drawn_edges = set()
        for node in graph.nodes.values():
            for neighbour, open in node.neighbours:
                route = f'{node.id},{neighbour.id}'
                if route in drawn_edges or f'{neighbour.id},{node.id}' in drawn_edges:
                    continue
                drawn_edges.add(route)
                
                x1, y1 = scale(node.position.x, node.position.y)
                x2, y2 = scale(neighbour.position.x, neighbour.position.y)
                
                # Draw the line
                if route in self.blocked_routes:
                    self.canvas.create_line(x1, y1, x2, y2, fill="red")
                else:
                    self.canvas.create_line(x1, y1, x2, y2, fill="black" if open else "green")
                
                # Calculate the midpoint of the edge
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Tooltip information
                square_image = self.original_square_image.resize((5, 5), Image.BILINEAR)
                tk_edge_image = ImageTk.PhotoImage(square_image)
                self.images_on_canvas.append(tk_edge_image)
                idEdge = self.canvas.create_image(mid_x, mid_y, image=tk_edge_image, anchor=CENTER)
                edge_text = f"Edge: {node.id},{neighbour.id}"

                # Bind tooltip to the graphical edge ID
                self.canvas.tag_bind(idEdge, "<Enter>", lambda e, t=edge_text: self.show_tooltip(e, t))
                self.canvas.tag_bind(idEdge, "<Leave>", self.hide_tooltip)

        # Draw nodes
        for node in graph.nodes.values():
            x, y = scale(node.position.x, node.position.y)
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

        # Draw start point
        x, y = scale(start_point.position.x, start_point.position.y)
        start_image = self.original_start_point_image.resize((30, 30), Image.BILINEAR)
        tk_start_image = ImageTk.PhotoImage(start_image)
        self.images_on_canvas.append(tk_start_image)
        start_id = self.canvas.create_image(x, y, image=tk_start_image, anchor=CENTER)

        # Tooltip for start point
        supplies_text = "Contains: \n" + "\n".join(f"{supply.type.name}: {supply.quantity}" for supply in start_point.supplies)
        self.canvas.tag_bind(start_id, "<Enter>", lambda e, t=supplies_text: self.show_tooltip(e, t))
        self.canvas.tag_bind(start_id, "<Leave>", self.hide_tooltip)

        # Draw end points
        for end_point in end_points:
            x, y = scale(end_point.position.x, end_point.position.y)
            end_image = self.original_end_point_image.resize((30, 30), Image.BILINEAR)
            tk_end_image = ImageTk.PhotoImage(end_image)
            self.images_on_canvas.append(tk_end_image)
            end_id = self.canvas.create_image(x, y, image=tk_end_image, anchor=CENTER)

            # Tooltip for end points
            needed_supplies_text = "Needed supplies: \n" + "\n".join(
                f"{supply_type}: {quantity}" for supply_type, quantity in end_point.get_supplies_needed().items()
            )
            self.canvas.tag_bind(end_id, "<Enter>", lambda e, t=needed_supplies_text: self.show_tooltip(e, t))
            self.canvas.tag_bind(end_id, "<Leave>", self.hide_tooltip)

        # Draw vehicles
        i = 1
        for vehicle in vehicles:
            x, y = scale(vehicle.position.x + 0.0006 * i, vehicle.position.y)
            vehicle_image = self.original_vehicle_image.resize((20, 20), Image.BILINEAR)
            tk_vehicle_image = ImageTk.PhotoImage(vehicle_image)
            self.images_on_canvas.append(tk_vehicle_image)
            vehicle_id = self.canvas.create_image(x, y, image=tk_vehicle_image, anchor=CENTER)
            i += 1

            # Tooltip for vehicles
            vehicle_text = f"Vehicle {vehicle.id} ({vehicle.type.name}) \nFuel: {vehicle.current_fuel}/{vehicle.type.fuel_capacity} \nWeight: {vehicle.current_weight}/{vehicle.type.weight_capacity} \nVolume: {vehicle.current_volume}/{vehicle.type.volume_capacity} \n Average speed: {vehicle.type.average_velocity} km/h"
            self.canvas.tag_bind(vehicle_id, "<Enter>", lambda e, t=vehicle_text: self.show_tooltip(e, t))
            self.canvas.tag_bind(vehicle_id, "<Leave>", self.hide_tooltip)

    def run(self):
        self.root.mainloop()

    def draw_path(self, graph, positions, on_complete=None):
        if not positions or len(positions) < 2:
            print("Error: Path requires at least two positions to draw.")
            return

        min_x = min(node.position.x for node in graph.nodes.values())
        max_x = max(node.position.x for node in graph.nodes.values())
        min_y = min(node.position.y for node in graph.nodes.values())
        max_y = max(node.position.y for node in graph.nodes.values())

        def scale(x, y):
            scaled_x = 50 + (x - min_x) / (max_x - min_x) * 700
            scaled_y = 50 + (y - min_y) / (max_y - min_y) * 500
            return scaled_x, scaled_y

        def draw_segment(i):
            if i < len(positions) - 1:
                x1, y1 = scale(positions[i].x, positions[i].y)
                x2, y2 = scale(positions[i + 1].x, positions[i + 1].y)
                self.canvas.create_line(x1, y1, x2, y2, fill="green", width=4)
                # All segments get drawn in 1.5 seconds
                self.root.after(int((1.5 * 1000) // len(positions)), lambda: draw_segment(i + 1))
            else:
                if on_complete:
                    time.sleep(1)
                    on_complete()

        # Start drawing the path from the first segment
        draw_segment(0)

    def select_algorithm(self, selected_algorithm):
        self.algorithm_callback(selected_algorithm, self.blocked_routes)
        self.selected_algorithm = selected_algorithm
        self.update_menu_label()


    
    def block_route(self, route):
        self.blocked_routes.add(route)
