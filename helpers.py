import networkx as nx
from matplotlib import pyplot as plt
import logging

logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def check_requirements(G, max_cost, min_flow):
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

    tG = G.copy()

    try:
        # Calculate maximum flow and its cost
        flow_value = float('inf')
        cost_value = 0
        for u, v, data in tG.edges(data=True):
            if 'cost' in data:
                data['weight'] = data.pop('cost')
        nodes = list(tG.nodes)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                source = nodes[i]
                sink = nodes[j]
                temp_flow = nx.maximum_flow_value(tG, source, sink)
                temp_dict = nx.max_flow_min_cost(tG, source, sink)
                temp_cost = nx.cost_of_flow(tG, temp_dict) / 100000
                if temp_flow < flow_value:
                    flow_value = temp_flow
                if temp_cost > cost_value:
                    cost_value = temp_cost

        #print(flow_value)
        #print(cost_value)
        # Check if the total flow is less than the minimum required flow
        if flow_value < min_flow:
            print("Total flow is less than min flow" + str(flow_value))
            return False

            # Check if the total cost exceeds the maximum allowed cost
        if cost_value > max_cost:
            print("Cost is greater than max cost"+ str(cost_value))
            return False

        # If both conditions are satisfied
        #logging.info("Network found")
        return True
    except nx.NetworkXUnfeasible:
        #logging.info("No feasible flow exists")
        return False


def is_connected(graph):
    """Check if the graph is connected."""
    return nx.is_connected(graph)


def count_inner_lists(list_of_lists):
    """Returns the number of lists in the given list of lists."""
    return len(list_of_lists)


def show_plot(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'cost')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()


def get_remaining_edges(original_edges, killed_edges):
    flattened_killed_edges = [edge for sublist in killed_edges for edge in sublist]
    remaining_edges = [edge for edge in original_edges if edge not in flattened_killed_edges]
    return remaining_edges


def showLoggingInfo(link_failures, survivors):
    iterations = len(link_failures)
    survive_number = len(survivors)
    logging.info("Follorwing Edges could not be killed: " + str(survivors))
    logging.info("Iterations needed to terminate: " + str(iterations))
    logging.info("Number of Survivors: " + str(survive_number))
