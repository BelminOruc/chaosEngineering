import logging

import networkx as nx
from itertools import combinations
import helpers


def brute_killer(G, max_cost, min_cap):
    """Brute Force algorithm to find all edges that can be killed while maintaining connectivity."""
    edges = list(G.edges())
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
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    survivors = helpers.show_logging_info(G, link_failures, survivors)
    return len(link_failures), survivors


