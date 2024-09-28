import networkx as nx
import random

from matplotlib import pyplot as plt

import helpers
def random_killer(G, demands, max_cost, min_cap):
    """Random Algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges())
    killed_edges = []
    killed_edge_sets = []
    while original_edges:
        random.shuffle(original_edges)
        best_killed_set = set()
        max_killed_links = 0

        for _ in range(len(original_edges)):
            random_set = set(random.sample(original_edges, random.randint(1, len(original_edges))))
            temp_graph = G.copy()
            temp_graph.remove_edges_from(random_set)
            print(temp_graph.edges)
            if helpers.check_requirements(temp_graph, demands, max_cost, min_cap):
                killed_count = len(best_killed_set.union(random_set))
                if killed_count > max_killed_links:
                    max_killed_links = killed_count
                    best_killed_set = best_killed_set.union(random_set)
        killed_edge_sets.append(random_set)
        if not best_killed_set:
            # Restart with the original graph if no more edges can be killed
            original_edges = list(G.edges())
        else:
            killed_edges.extend(best_killed_set)
            original_edges = [edge for edge in original_edges if edge not in best_killed_set]
    #print(list(killed_edge_sets))
    return helpers.count_inner_lists(list(killed_edge_sets))
