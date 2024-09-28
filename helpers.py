import networkx as nx
from matplotlib import pyplot as plt
import logging

logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def check_requirements(G, demands, max_cost, min_flow):
    """
    Check if a flow exists that meets all the node demands with a maximum cost and a minimum flow.
    Parameters:
    G (nx.DiGraph): Directed graph with edge capacities and costs.
    demands (dict): Dictionary with node demands, e.g., {node1: demand1, node2: demand2, ...}
    max_cost (int): Maximum allowable cost.
    min_flow (int): Minimum required flow.
    Returns:
    bool: True if requirements are met, False otherwise.
    """
    # Ensure the graph is directed for flow calculations
    if not nx.is_connected(G):
        #logging.info("Graph is not connected")
        return False

    if not isinstance(G, nx.DiGraph):
        DG = G.to_directed()

    # Add demand attribute to nodes
    DG, dg_demands, total_demand = add_sink_node_with_demand(DG, demands)
    for node, demand in dg_demands.items():
        DG.nodes[node]['demand'] = demand

    try:
        # Calculate maximum flow and its cost
        flow_value, flow_dict = nx.maximum_flow(DG, 'source_node', list(DG.nodes)[0])
        flow_cost = sum(DG[u][v]['cost'] * flow_dict[u][v] for u in flow_dict for v in flow_dict[u])

        # Check if the total cost exceeds the maximum allowed cost
        if flow_cost > max_cost:
            #logging.info("Cost is greater than max cost")
            return False

        # Check if the total flow is less than the minimum required flow
        if flow_value < min_flow:
            #logging.info("Total flow is less than min flow")
            return False

        # If both conditions are satisfied
        #logging.info("Network found")
        return True
    except nx.NetworkXUnfeasible:
        #logging.info("No feasible flow exists")
        return False


def old_check_requirements(G, demands, max_cost, min_flow):
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
        if flow_cost > max_cost:
            print("Cost is greater than max cost")
            return False

        # Calculate the total flow through the network
        # Total flow is calculated as the sum of flow out of the source node
        source_node = [node for node, demand in dg_demands.items() if demand < 0]
        if len(source_node) != 1:
            print(len(source_node))
            print("There should be exactly one source node with a negative demand")
        source_node = source_node[0]

        # Calculate the total flow through the network
        total_flow = smallest_maximum_flow(G)
        # Check if the total flow is less than the minimum required flow
        if total_flow < min_flow:
            print("Total flow is less than min flow")
            return False

        # If both conditions are satisfied
        print("Network found")
        return True
    except nx.NetworkXUnfeasible:
        print("Network Simplex doesnt work")
        # If no feasible flow exists
        return False


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

    return DG, new_demands, total_demand


def smallest_maximum_flow(G):
    """
    Finds the smallest maximum flow between any pair of edge nodes, ensuring flow must go through other nodes.

    Parameters:
    - G: A directed graph (networkx.DiGraph) with capacity attribute on edges.

    Returns:
    - min_flow: The smallest maximum flow value among edge node pairs through intermediates.
    """
    edge_nodes = [node for node in G.nodes if is_edge_node(G, node)]
    min_flow = float('inf')
    for i in range(len(edge_nodes)):
        for j in range(i + 1, len(edge_nodes)):
            source = edge_nodes[i]
            sink = edge_nodes[j]
            # Use a copy of the graph for each flow calculation
            G_temp = G.copy()
            # Check if there's a direct edge between source and sink
            if G_temp.has_edge(source, sink):
                G_temp.remove_edge(source, sink)
            if G_temp.has_edge(sink, source):
                G_temp.remove_edge(sink, source)
            # Calculate maximum flow in the modified graph
            flow_value, _ = nx.maximum_flow(G_temp, source, sink)
            # Update the min flow if a smaller flow is found
            if flow_value < min_flow:
                min_flow = flow_value
    return min_flow


def is_edge_node(graph, node):
    # A node is considered an edge node if it has degree 1 (either in or out)
    neighbors = list(graph.neighbors(node)) + list(graph.predecessors(node))
    unique_neighbors = set(neighbors)
    return len(unique_neighbors) == 1


def is_connected(graph):
    """Check if the graph is connected."""
    return nx.is_connected(graph)


def count_inner_lists(list_of_lists):
    """Returns the number of lists in the given list of lists."""
    return len(list_of_lists)


def show_plot(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()
