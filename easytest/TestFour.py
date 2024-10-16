import networkx as nx
import matplotlib.pyplot as plt

import helpers


def is_edge_node(graph, node):
    # A node is considered an edge node if it has degree 1 (either in or out)
    neighbors = list(graph.neighbors(node)) + list(graph.predecessors(node))
    unique_neighbors = set(neighbors)
    return len(unique_neighbors) == 1

def smallest_maximum_flow(G):
    """
    Finds the smallest maximum flow between any pair of edge nodes, ensuring flow must go through other nodes.

    Parameters:
    - G: A directed graph (networkx.DiGraph) with capacity attribute on edges.

    Returns:
    - min_flow: The smallest maximum flow value among edge node pairs through intermediates.
    - node_pair: The pair of edge nodes with the smallest maximum flow through intermediates.
    """
    edge_nodes = [node for node in G.nodes if is_edge_node(G, node)]
    print(edge_nodes)
    min_flow = float('inf')
    for i in range(len(edge_nodes)):
        for j in range(i + 1, len(edge_nodes)):
            source = edge_nodes[i]
            sink = edge_nodes[j]
            # Check if there's a direct edge between source and sink
            if G.has_edge(source, sink) or G.has_edge(sink, source):
                # Temporarily remove the direct edge if it exists
                G_temp = G.copy()
                if G_temp.has_edge(source, sink):
                    G_temp.remove_edge(source, sink)
                if G_temp.has_edge(sink, source):
                    G_temp.remove_edge(sink, source)
                # Calculate maximum flow in the modified graph
                flow_value, _ = nx.maximum_flow(G_temp, source, sink)
            else:
                # Calculate maximum flow in the original graph as there is no direct edge
                flow_value, _ = nx.maximum_flow(G, source, sink)
            # Update the min flow and node pair if a smaller flow is found
            if flow_value < min_flow:
                min_flow = flow_value
    return min_flow

def add_sink_node_with_demand(G, demands):
    """
    Adds a sink node to the graph with a negative demand and connects it to the first node.
    Parameters:
    - G: A directed graph (networkx.DiGraph)
    - demands: A dictionary with node demands {node: demand}
    Returns:
    - DG: The modified directed graph with the new sink node
    - new_demands: The modified demands map including the sink node's demand
    """
    # Create a copy of the original graph to avoid modifying it
    DG = G.copy()

    # Calculate the total demand
    total_demand = sum(demands.values())

    # Determine the new sink node ID
    if G.nodes:
        first_node = list(G.nodes)[0]
        source_node = "source_node"
        while source_node in G.nodes:
            source_node += "_"
    else:
        first_node = None
        source_node = 0

    # Add the sink node to the graph
    DG.add_node(source_node)

    # Connect the sink node to the first node in the original graph
    if first_node is not None:
        DG.add_edge(source_node, first_node, capacity=total_demand, cost=0)
    # Create the new demands map

    new_demands = demands.copy()
    new_demands[source_node] = -total_demand

    pos = nx.spring_layout(DG)
    nx.draw(DG, pos, with_labels=True)
    # Draw edge labels with weights
    edge_labels = nx.get_edge_attributes(DG, 'capacity')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()

    return DG, new_demands, total_demand

def check_flow_requirements(G, demands, max_cost, min_flow):
    """
    Check if a flow exists that meets all the node demands with a maximum cost and a minimum flow.
    Parameters:
    G (nx.DiGraph): Directed graph with edge capacities and costs.
    demands (dict): Dictionary with node demands, e.g., {node1: demand1, node2: demand2, ...}
    maxcost (int): Maximum allowable cost.
    minflow (int): Minimum required flow.
    Returns:
    bool: True if requirements are met, False otherwise.
    """
    # Ensure the graph is directed for flow calculations
    if not isinstance(G, nx.DiGraph):
        G = G.to_directed()
        # Add demand attribute to nodes
    DG, dg_demands, total_demand = add_sink_node_with_demand(G, demands)
    for node, demand in dg_demands.items():
        DG.nodes[node]['demand'] = demand

    try:
        # Calculate minimum cost flow
        flow_cost, flow_values = nx.network_simplex(DG)

        # Check if the total cost exceeds the maximum allowed cost

        print("flow_cost: ", flow_cost)
        print("max: ", max_cost)
        if flow_cost > max_cost:
            return False

        # Calculate the total flow through the network
        # Total flow is calculated as the sum of flow out of the source node
        source_node = [node for node, demand in dg_demands.items() if demand < 0]
        if len(source_node) != 1:
            print(len(source_node))
            print("There should be exactly one source node with a negative demand")
        source_node = source_node[0]

        # Calculate the total flow through the network
        total_flow= smallest_maximum_flow(G)
        # Check if the total flow is less than the minimum required flow
        print("total_flow: ", total_flow)
        if total_flow < min_flow:
            return False

        # If both conditions are satisfied
        return True
    except nx.NetworkXUnfeasible:
        # If no feasible flow exists
        return False

# Example Usage
G = nx.Graph()
G.add_edge('A', 'B', capacity=55, weight=1)
G.add_edge('B', 'C', capacity=5, weight=2)
#G.add_edge('C', 'A', capacity=5, weight=2)
G.add_edge('C', 'D', capacity=7, weight=2)

demands = {'A': 15, 'B': 5, 'C': 5, 'D': 5}  # Example demands
maxcost = 100
minflow = 10
