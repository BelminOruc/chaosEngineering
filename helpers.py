import networkx as nx
from matplotlib import pyplot as plt
import logging

logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def check_requirements(G, max_cost, min_flow):
    """
    Check if a flow exists that meets all the node demands with a maximum cost and a minimum flow.
    Parameters:
    G (nx.DiGraph): Directed graph with edge capacities and costs.
    max_cost (int): Maximum allowable cost.
    min_flow (int): Minimum required flow.
    Returns:
    bool: True if requirements are met, False otherwise.
    """
    if not nx.is_connected(G):
        return False

    tG = G.copy()

    nodes = list(tG.nodes)
    valid_costs = []
    for u, v, data in tG.edges(data=True):
        if 'cost' in data:
            data['weight'] = data.pop('cost')
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            print("trying to find flow between " + str(i) + " and " + str(j))
            source = nodes[i]
            sink = nodes[j]
            temp_flow = nx.maximum_flow_value(tG, source, sink)
            if temp_flow >= min_flow:
                try:
                    temp_dict = nx.max_flow_min_cost(tG, source, sink)
                    temp_cost = nx.cost_of_flow(tG, temp_dict)
                    valid_costs.append(temp_cost)
                except nx.NetworkXUnfeasible:
                    continue
    if not valid_costs:
        return False

    min_valid_cost = min(valid_costs)
    return min_valid_cost <= max_cost


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
    logging.info("Iterations needed to terminate: " + str(iterations))
    if survive_number != 0:
        logging.info("Number of Survivors: " + str(survive_number))
        logging.info("Follorwing Edges could not be killed: " + str(survivors))


def generate_tikz_graph(name, y_values, x_values, failed_edges, filename='graphs.txt'):
    """
    Generates LaTeX TikZ code for a graph given two lists of integers.

    Parameters:
    name (str): Label for the graph.
    x_values (list of int): List of x-axis values (iterations).
    y_values (list of int): List of y-axis values (edges).
    failed_edges (list of int): List of y-axis values for failed edges.
    filename (str): Name of the file to save the TikZ code.

    Returns:
    str: LaTeX TikZ code for the graph.
    """
    x_values, y_values, failed_edges = sort_by_values(x_values, y_values, failed_edges)

    tikz_code = "\\begin{tikzpicture}\n"
    tikz_code += "  \\begin{axis}[\n"
    tikz_code += "    title={" + name + "},\n"
    tikz_code += "    xlabel={edges},\n"
    tikz_code += "    ylabel={iterations},\n"
    tikz_code += "    grid=major,\n"
    tikz_code += "    width=10cm,\n"
    tikz_code += "    height=6cm\n"
    tikz_code += "  ]\n"
    tikz_code += "  \\addplot coordinates {\n"

    for x, y in zip(y_values, x_values):
        tikz_code += f"    ({x}, {y})\n"

    tikz_code += "  };\n"
    tikz_code += "  \\addplot[color=red] coordinates {\n"

    for x, y in zip(y_values, failed_edges):
        tikz_code += f"    ({x}, {y})\n"

    tikz_code += "  };\n"
    tikz_code += "  \\end{axis}\n"
    tikz_code += "\\end{tikzpicture}\n"

    with open(filename, 'a') as file:
        file.write(tikz_code)


def plot_result_graph(name, y_values, x_values, failed_edges):
    x_values, y_values, failed_edges = sort_by_values(x_values, y_values, failed_edges)
    """
    Plots a graph given three lists of integers using matplotlib.

    Parameters:
    name (str): Label for the graph.
    x_values (list of int): List of x-axis values (iterations).
    y_values (list of int): List of y-axis values (edges).
    failed_edges (list of int): List of y-axis values for failed edges.
    surviving_edges (list of int): List of y-axis values for surviving edges.

    Returns:
    None
    """


    plt.figure(figsize=(10, 6))
    plt.plot(y_values, x_values, marker='o', label='Iterations')
    plt.plot(y_values, failed_edges, marker='o', color='red', label='Failed Edges')
    plt.xlabel('Edges')
    plt.ylabel('Iterations/Not Failed Edges')
    plt.title(name)
    plt.grid(True)
    plt.legend()
    plt.show()

def get_test_values(G):
    tG = G.copy()
    flows = []
    costs = []

    nodes = list(tG.nodes)
    for u, v, data in tG.edges(data=True):
        if 'cost' in data:
            data['weight'] = data.pop('cost')
    flow = nx.maximum_flow_value(tG, nodes[0], nodes[1])
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            source = nodes[i]
            sink = nodes[j]
            temp_flow = nx.maximum_flow_value(tG, source, sink)
            try:
                temp_dict = nx.max_flow_min_cost(tG, source, sink)
                temp_cost = nx.cost_of_flow(tG, temp_dict)
                costs.append(temp_cost)
                flows.append(temp_flow)
            except nx.NetworkXUnfeasible:
                continue
    if not costs or not flows:
        raise ValueError("No valid flows or costs found")
    highest_cost = max(costs) + 1
    mean_cost = sum(costs) / len(costs)
    lowest_cost = min(costs) - 1
    lowest_flow = min(flows) - 1

    return highest_cost,  mean_cost, lowest_cost, lowest_flow

def sort_by_values(x_values, y_values, failed_edges):
    """
    Sorts the x_values, y_values, and failed_edges lists based on ascending y_values.

    Parameters:
    x_values (list of int): List of x-axis values (iterations).
    y_values (list of int): List of y-axis values (edges).
    failed_edges (list of int): List of y-axis values for failed edges.

    Returns:
    tuple: Sorted x_values, y_values, and failed_edges lists.
    """
    if len(x_values) != len(y_values) or len(x_values) != len(failed_edges):
        raise ValueError("The length of x_values, y_values, failed_edges.")
    combined = list(zip(y_values, x_values, failed_edges))
    combined.sort()  # Sort by the first element of the tuples, which is y_values

    sorted_y_values, sorted_x_values, sorted_failed_edges = zip(*combined)
    return list(sorted_x_values), list(sorted_y_values), list(sorted_failed_edges)

def clear_files():
    files_to_clear = ['graphs.txt', 'analysis.log']
    for file in files_to_clear:
        with open(file, 'w') as f:
            f.truncate(0)

