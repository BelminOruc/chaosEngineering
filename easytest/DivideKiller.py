import networkx as nx
#Doesnt work
def is_connected(graph):
    """Check if the graph is connected."""
    return nx.is_connected(graph)

def find_killable_edges(graph, edges_to_consider):
    """Find all edges from 'edges_to_consider' that can be killed while maintaining connectivity."""
    killable_edges = []

    # Attempt to remove each edge and check if the graph remains connected
    for edge in edges_to_consider:
        graph.remove_edge(*edge)
        if is_connected(graph):
            killable_edges.append(edge)  # This edge can be killed
        else:
            graph.add_edge(*edge)  # Add it back if its removal disconnects the graph

    return killable_edges

def divide_and_conquer_kill(graph, nodes):
    """Divide and conquer algorithm to kill as many edges as possible while maintaining connectivity."""
    if len(nodes) <= 1:
        return []

    mid = len(nodes) // 2
    left_nodes = nodes[:mid]
    right_nodes = nodes[mid:]

    left_subgraph = graph.subgraph(left_nodes).copy()
    right_subgraph = graph.subgraph(right_nodes).copy()

    killed_left = divide_and_conquer_kill(left_subgraph, left_nodes)
    killed_right = divide_and_conquer_kill(right_subgraph, right_nodes)

    combined_kills = killed_left + killed_right

    # Attempt to kill edges across the boundary
    boundary_edges = [(u, v) for u in left_nodes for v in right_nodes if graph.has_edge(u, v)]
    killable_boundary_edges = find_killable_edges(graph, boundary_edges)

    return combined_kills + killable_boundary_edges

def divide_and_kill(graph):
    """Wrapper function to initiate the divide and conquer edge killing algorithm."""
    nodes = list(graph.nodes())
    return divide_and_conquer_kill(graph, nodes)

# Example usage
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5)])

    killed_edges = divide_and_kill(G)

    print("Edges killed:", killed_edges)