from graph.graph import Graph
from graph.position import Position
import osmnx as ox

def load_map_data_to_graph(geography):
    """
    Loads map data from a given geographical location and converts it into a graph representation.

    Args:
        geography (str): The geographical location to load the map data for.

    Returns:
        Graph: A graph object containing nodes and edges representing the road network of the given geography.
    """
    G = ox.graph_from_place(geography, network_type="drive")

    graph = Graph()
    id = 0
    for node, data in G.nodes(data=True):
        position = Position(data['x'], data['y'])
        graph.add_node(position, id)
        id += 1
    for u, v in G.edges():
        pos1 = Position(G.nodes[u]['x'], G.nodes[u]['y'])
        pos2 = Position(G.nodes[v]['x'], G.nodes[v]['y'])
        graph.add_edge(pos1, pos2)

    return graph