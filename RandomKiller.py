import logging

import networkx as nx
import random

from matplotlib import pyplot as plt

import helpers
def random_killer(G, demands, max_cost, min_cap):
    logging.info("Random: ")
    """Random Algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges())
    killed_edges = []
    link_failures = []
    while original_edges:
        random.shuffle(original_edges)
        best_killed_set = set()
        max_killed_links = 0

        for _ in range(len(original_edges)):
            random_set = set(random.sample(original_edges, random.randint(1, len(original_edges))))
            temp_graph = G.copy()
            temp_graph.remove_edges_from(random_set)
            print(temp_graph.edges)
            if helpers.check_requirements(temp_graph, max_cost, min_cap):
                killed_count = len(best_killed_set.union(random_set))
                if killed_count > max_killed_links:
                    max_killed_links = killed_count
                    best_killed_set = best_killed_set.union(random_set)
        link_failures.append(random_set)
        if not best_killed_set:
            # Restart with the original graph if no more edges can be killed
            original_edges = list(G.edges())
        else:
            killed_edges.extend(best_killed_set)
            original_edges = [edge for edge in original_edges if edge not in best_killed_set]
    #print(list(link_failures))
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    helpers.showLoggingInfo(link_failures, survivors)
