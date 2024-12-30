from graph.graph import Graph
from graph.position import Position
import osmnx as ox

def load_map_data_to_graph(geography):
    G = ox.graph_from_place(geography, network_type="drive")

    graph = Graph()
    id = 0
    for node, data in G.nodes(data=True):
        position = Position(data['x'], data['y'])
        priority = 0
        if 'priority' in data:
            priority = data['priority']
        graph.add_node(position, priority, id)
        id += 1
    for u, v in G.edges():
        pos1 = Position(G.nodes[u]['x'], G.nodes[u]['y'])
        pos2 = Position(G.nodes[v]['x'], G.nodes[v]['y'])
        graph.add_edge(pos1, pos2)

    return graph