import logging
import networkx as nx
import random
from itertools import combinations

from matplotlib import pyplot as plt
import helpers


def random_killer(G, demands, max_cost, min_cap):
    logging.info("Random: ")
    """Random Algorithm to find all edges that can be killed while maintaining connectivity."""
    edges = list(G.edges())
    random.shuffle(edges)  # Shuffle the initial list of edges
    remaining_edges = edges.copy()
    link_failures = []

    for r in range(1, len(edges) + 1):  # r is the size of the subset
        for subset in combinations(edges, r):
            # Create a new graph without the edges in the subset
            temp_graph = G.copy()
            temp_graph.remove_edges_from(subset)

            # Check if the modified graph is still connected
            if helpers.check_requirements(temp_graph, max_cost, min_cap):
                link_failures.append(list(subset))
                for edge in subset:
                    if edge in remaining_edges:
                        remaining_edges.remove(edge)
            if not remaining_edges:
                break
        if not remaining_edges:
            break

    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    helpers.showLoggingInfo(link_failures, survivors)


G = nx.Graph()
G.add_edge("a", "b", capacity=6.0, weight=1.0)
G.add_edge("a", "c", capacity=6.0, weight=1.0)
G.add_edge("b", "c", capacity=6.0, weight=1.0)
G.add_edge("b", "c", capacity=6.0, weight=1.0)
G.add_edge("b", "e", capacity=6.0, weight=1.0)
G.add_edge("b", "d", capacity=6.0, weight=1.0)
G.add_edge("c", "d", capacity=6.0, weight=1.0)
G.add_edge("c", "e", capacity=6.0, weight=1.0)
G.add_edge("d", "e", capacity=6.0, weight=1.0)
# Initialize demands and other parameters
demands = {
    'a': 1,  # Supply node
    'b': 1,  # Transit node
    'c': 1,  # Transit node
    'd': 1,  # Demand node
    'e': 1,  # Transit node
    'x': 1,  # Transit node
    'y': 1  # Demand node
}
