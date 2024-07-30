import networkx as nx


def check_flow_requirements(G, demands, maxcost, minflow):
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
        DG = G.to_directed()
    else:
        DG = G

    dgDemands = demands
    # Add demand attribute to nodes
    for node, demand in demands.items():
        DG.nodes[node]['demand'] = dgDemands

    try:
        #DG.add_node(DG,comp_node)
        # Calculate minimum cost flow
        flow_cost, flow_values = nx.network_simplex(DG)

        # Check if the total cost exceeds the maximum allowed cost
        print("flow_cost: ", flow_cost)
        if flow_cost > maxcost:
            return False

        # Calculate the total flow through the network
        total_flow = sum(sum(flow_values[u][v] for v in flow_values[u]) for u in flow_values)
        print(flow_values)
        # Check if the total flow is less than the minimum required flow
        print("total_flow: ", total_flow)
        if total_flow < minflow:
            return False

        # If both conditions are satisfied
        return True
    except nx.NetworkXUnfeasible:
        # If no feasible flow exists
        return False


# Example Usage
G = nx.DiGraph()
G.add_edge('A', 'B', capacity=10, weight=1)
G.add_edge('B', 'C', capacity=15, weight=2)
G.add_edge('A', 'C', capacity=5, weight=2)

demands = {'A': -15, 'B': 0, 'C': 15}  # Example demands
maxcost = 100
minflow = 10

result = check_flow_requirements(G, demands, maxcost, minflow)
print(result)