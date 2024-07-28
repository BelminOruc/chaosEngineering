import networkx as nx
import matplotlib.pyplot as plt

def ensure_demand_and_minimum_flow_met(G, demands, minimum_flow, maxCost):
    """
    Ensures that every node demand is met and the graph has at least the specified minimum flow.

    Parameters:
    G (nx.Graph): Undirected graph with edge weights and capacities.
    demands (dict): Dictionary with node as key and demand as value.
                    Positive values represent demand, and negative values represent supply.
    minimum_flow (float): The minimum total flow that must be met.

    Returns:
    bool: True if demands are met and total flow is at least minimum_flow, False otherwise.
    """
    # Convert undirected graph to directed graph
    DG = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        DG.add_edge(u, v, capacity=data.get('capacity', 0), weight=data.get('weight', 0))
        DG.add_edge(v, u, capacity=data.get('capacity', 0), weight=data.get('weight', 0))

    # Add a super-source and super-sink to balance demands
    dgDemands=demands
    super_source = 'super_source'
    super_sink = 'super_sink'
    DG.add_node(super_source)
    DG.add_node(super_sink)

    #TODO: Fix
    total_demand = 0
    for node, demand in demands.items():
        if demand > 0:
            DG.add_edge(super_source, node, capacity=demand, weight=0)
            total_demand += demand
        elif demand < 0:
            DG.add_edge(node, super_sink, capacity=-demand, weight=0)

    # Balance the total demand and supply
    DG.nodes[super_source]['demand'] = -total_demand
    DG.nodes[super_sink]['demand'] = total_demand

    pos = nx.spring_layout(DG)
    nx.draw(DG, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(DG, 'capacity')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()
    
    for nodes in DG.nodes():
        print(nodes)

    # Use the network simplex algorithm to find the minimum cost flow that satisfies demands
    try:
        flow_cost, flow_dict = nx.network_simplex(DG)
    except nx.NetworkXUnfeasible:
        print("Demands not met")
        return False


    # Calculate the total flow from super_source
    total_flow = sum(flow_dict[super_source].values())
    print("total flow", total_flow)
    # Check if the total flow is at least the minimum flow
    if total_flow < minimum_flow:
        print("Not enough flow")
        return False
    if flow_cost > maxCost:
        print("Cost too high", flow_cost)
        return False
    return True


# Example usage
if __name__ == "__main__":
    # Create an undirected graph
    G = nx.Graph()

    # Add edges with weights and capacities
    G.add_edge('A', 'B', capacity=1)
    G.add_edge('B', 'C', capacity=2)
    G.add_edge('A', 'C', capacity=3)
    G.add_edge('C', 'D', capacity=1)

    # Define demands
    demands = {
        'A': 15,  # Supply node
        'B': 2,  # Transit node
        'C': -7,  # Transit node
        'D': -10  # Demand node
    }

    # Define minimum flow
    minimum_flow = 13

    # Ensure demands and minimum flow are met
    result = ensure_demand_and_minimum_flow_met(G, demands, minimum_flow, 20)

    print("Are demands and minimum flow met?", result)
