import networkx as nx
from collections import deque
from matplotlib import pyplot as plt
import logging

logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')




def bfs_min_flow(graph, source):
    """Finds the minimum flow in the residual graph using BFS."""
    visited = {node: False for node in graph}
    queue = deque([(source, float('Inf'))])
    min_flow = float('Inf')

    while queue:
        current_node, flow = queue.popleft()
        visited[current_node] = True

        for neighbor in graph[current_node]:
            capacity = graph[current_node][neighbor]['capacity']
            if not visited[neighbor]:
                new_flow = min(flow, capacity)
                min_flow = min(min_flow, new_flow)
                queue.append((neighbor, new_flow))

    return min_flow


def find_lowest_weight(G, paths):
    """Finds the lowest weight path in the graph."""
    min_weight = float('Inf')
    for source, target_paths in paths.items():
        for target, path in target_paths.items():
            weight = sum(
                nx.get_edge_attributes(G, 'weight').get((path[i], path[i + 1]), 0) for i in range(len(path) - 1))
            if weight < min_weight:
                min_weight = weight
    return min_weight


def check_requirements(G, max_cost, min_flow):
    """Checks if a flow exists that meets the requirements."""
    #if not nx.is_biconnected(G):
    #    return False

    if not nx.is_connected(G):
        return False

    if(check_graph_data(G)):
        tG = G.copy()
        nodes = list(tG.nodes)
        lowest_flow = float('Inf')
        for node in nodes:

            flow = bfs_min_flow(tG, node)
            if flow < lowest_flow:
                lowest_flow = flow

        for u, v, data in tG.edges(data=True):
            if 'cost' in data:
                data['weight'] = data.pop('cost')
        weights = nx.get_edge_attributes(tG, 'weight')

        cost = max(weights.values(), default=None)

        if lowest_flow < min_flow or cost > max_cost:
            return False
        else:
            return True
    else:
        return True


def show_plot(G):
    """Displays a plot of the graph with edge labels."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'cost')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.show()


def get_remaining_edges(original_edges, killed_edges):
    """Returns the edges that are not in the killed edges list."""
    if all(isinstance(edge, tuple) and len(edge) == 2 for edge in killed_edges):
        flattened_killed_edges = killed_edges
    else:
        flattened_killed_edges = [edge for sublist in killed_edges for edge in sublist]

    remaining_edges = [edge for edge in original_edges if edge not in flattened_killed_edges]
    return remaining_edges


def show_logging_info(G, link_failures, survivors):
    """Logs the number of iterations and survivors."""
    iterations = len(link_failures)
    survive_number = survivors
    survive_percentage = len(survivors)/len(list(G.edges()))*100
    logging.info("Iterations needed to terminate: " + str(iterations))
    if survive_number != 0:
        logging.info("Number of Survivors: " + str(len(survive_number)))
        logging.info("Following Edges could not be killed: " + str(survivors))
    return survive_percentage


def generate_tikz_graph(name, y_values, x_values, failed_edges, filename='graphs.txt'):
    """Generates LaTeX TikZ code for a graph."""
    x_values, y_values, failed_edges = sort_by_values(x_values, y_values, failed_edges)
    tikz_code = "\\\ \n"
    tikz_code += "\\begin{tikzpicture}\n"
    tikz_code += "  \\begin{axis}[\n"
    tikz_code += "    title={" + name + " iterations},\n"
    tikz_code += "    xlabel={Edges},\n"
    tikz_code += "    ylabel={Iterations},\n"
    tikz_code += "    grid=major,\n"
    tikz_code += "    width=10cm,\n"
    tikz_code += "    height=6cm\n"
    tikz_code += "  ]\n"
    tikz_code += "  \\addplot coordinates {\n"

    for x, y in zip(y_values, x_values):
        tikz_code += f"    ({x}, {y})"

    tikz_code += "  };\n"
    tikz_code += "  \\end{axis}\n"
    tikz_code += "\\end{tikzpicture}\n"
    tikz_code += "\\\ \n"
    tikz_code += "\\begin{tikzpicture}\n"
    tikz_code += "  \\begin{axis}[\n"
    tikz_code += "    title={" + name + " not killed},\n"
    tikz_code += "    xlabel={Edges},\n"
    tikz_code += "    ylabel={Failed Edges in Percent},\n"
    tikz_code += "    grid=major,\n"
    tikz_code += "    width=10cm,\n"
    tikz_code += "    height=6cm\n"
    tikz_code += "  ]\n"

    tikz_code += "  \\addplot[color=red, mark=*] coordinates {\n"

    for x, y in zip(y_values, failed_edges):
        tikz_code += f"    ({x}, {y})"

    tikz_code += "  };\n"
    tikz_code += "  \\end{axis}\n"
    tikz_code += "\\end{tikzpicture}\n"
    tikz_code += "\\\ \n"
    with open(filename, 'a') as file:
        file.write(tikz_code)


def plot_result_graph(name, y_values, x_values, failed_edges):
    """Plots a graph using matplotlib."""
    x_values, y_values, failed_edges = sort_by_values(x_values, y_values, failed_edges)

    # Plot for iterations
    plt.figure(figsize=(10, 6))
    plt.plot(y_values, x_values, marker='o', label='Iterations')
    plt.xlabel('Edges')
    plt.ylabel('Iterations')
    plt.title(name + ' Iterations')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Plot for failed edges
    plt.figure(figsize=(10, 6))
    plt.plot(y_values, failed_edges, marker='o', color='red', label='Failed Edges in Percent')
    plt.xlabel('Edges')
    plt.ylabel('Failed Edges')
    plt.title(name + ' Failed Edges')
    plt.grid(True)
    plt.legend()
    plt.show()


def get_test_values(G):
    """Returns test values for the graph."""
    flows = []
    costs = []
    tG = G.copy()
    nodes = list(tG.nodes)

    flow = bfs_min_flow(tG, nodes[0])

    for u, v, data in tG.edges(data=True):
        if 'cost' in data:
            data['weight'] = data.pop('cost')
    weights = list(nx.get_edge_attributes(tG, 'weight').values())
    highest_cost = max(weights) + 1
    weights.sort()
    index_95th_percentile = int(len(weights) * 0.99)
    index_80th_percentile = int(len(weights) * 0.95)
    index_50th_percentile = int(len(weights) * 0.50)
    five_percent = weights[index_95th_percentile-1]
    twenty_percent = weights[index_80th_percentile-1]
    half = weights[index_50th_percentile-1]

    lowest_flow = flow - 1

    return highest_cost, five_percent, twenty_percent,  half,  lowest_flow


def sort_by_values(x_values, y_values, failed_edges):
    """Sorts the x_values, y_values, and failed_edges lists."""
    if len(x_values) != len(y_values) or len(x_values) != len(failed_edges):
        raise ValueError("The length of x_values, y_values, failed_edges.")
    combined = list(zip(y_values, x_values, failed_edges))
    combined.sort()  # Sort by the first element of the tuples, which is y_values

    sorted_y_values, sorted_x_values, sorted_failed_edges = zip(*combined)
    return list(sorted_x_values), list(sorted_y_values), list(sorted_failed_edges)


def clear_files():
    """Clears the contents of specified files."""
    files_to_clear = ['graphs.txt', 'analysis.log']
    for file in files_to_clear:
        with open(file, 'w') as f:
            f.truncate(0)


def check_graph_data(G):
    """Checks if all edges in the graph have 'capacity' and 'cost' as edge data."""
    for u, v, data in G.edges(data=True):
        if 'capacity' not in data or 'cost' not in data:
            return False
    return True