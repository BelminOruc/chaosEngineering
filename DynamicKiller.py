import itertools
import logging

import networkx as nx
import matplotlib.pyplot as plt
import helpers

# Fill the DP table
def dynamic_killer(G, max_cost, min_cap):
    """Dynamic Programming algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges())
    memo = {}

    def dp(edges):
        edges_tuple = tuple(sorted(edges))
        if edges_tuple in memo:
            return memo[edges_tuple]

        temp_graph = G.copy()
        temp_graph.remove_edges_from(edges)

        if not helpers.check_requirements(temp_graph, max_cost, min_cap):
            memo[edges_tuple] = False
            return False

        for edge in edges:
            remaining_edges = [e for e in edges if e != edge]
            if dp(remaining_edges):
                memo[edges_tuple] = True
                return True

        memo[edges_tuple] = True
        return True

    link_failures = []
    for r in range(1, len(original_edges) + 1):
        for edges_to_remove in itertools.combinations(original_edges, r):
            if dp(edges_to_remove):
                link_failures.append(list(edges_to_remove))
            if len(link_failures) == len(original_edges):
                break
        if len(link_failures) == len(original_edges):
            break

    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    survivors = helpers.show_logging_info(G, link_failures, survivors)
    return len(link_failures), survivors
