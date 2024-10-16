import logging

import networkx as nx
from matplotlib import pyplot as plt

import helpers


def backtrack_killer(G, demands, max_cost, min_cap):
    """Backtracking algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges(data=True))
    remaining_edges = list(G.edges())
    link_failures = []
    all_edges_killed = set()

    def recursive_remove(temp_graph, current_set):
        nonlocal link_failures, all_edges_killed, remaining_edges

        for edge in original_edges:
            if edge[:2] not in current_set:
                # Store edge attributes before removing
                edge_data = temp_graph.get_edge_data(*edge[:2])
                temp_graph.remove_edge(*edge[:2])
                current_set.add(edge[:2])

                if helpers.check_requirements(temp_graph, max_cost, min_cap):
                    link_failures.append(list(current_set))
                    all_edges_killed.update(current_set)
                    remaining_edges.remove(edge[:2])
                    if not remaining_edges:
                        return  # Stop recursion if no remaining edges
                    recursive_remove(temp_graph, current_set)

                current_set.remove(edge[:2])
                # Restore edge with its attributes
                temp_graph.add_edge(*edge[:2], **edge_data)

    recursive_remove(G.copy(), set())

    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    helpers.showLoggingInfo(link_failures, survivors)
    return len(link_failures), len(survivors)
