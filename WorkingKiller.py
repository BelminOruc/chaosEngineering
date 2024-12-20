import logging

import networkx as nx
from matplotlib import pyplot as plt

import helpers


def find_killable_edges(G, edges_to_consider, max_cost, min_cap):
    """Find all edges from 'edges_to_consider' that can be killed while maintaining connectivity."""
    killable_edges = []

    # Attempt to remove each edge and check if the graph remains connected
    edges_to_consider.sort(key=lambda edge: G.get_edge_data(*edge).get('cost', 0), reverse=True)
    for edge in edges_to_consider:
        # Store edge attributes before removing
        edge_data = G.get_edge_data(*edge)
        G.remove_edge(*edge)
        if helpers.check_requirements(G, max_cost, min_cap):
            killable_edges.append(edge)  # This edge can be killed
        else:
            # Add it back if its removal disconnects the graph, with original attributes
            G.add_edge(*edge, **edge_data)
    print(G.edges)
    return killable_edges


def working_killer(G, max_cost, min_cap):

    """Iterative algorithm to kill as many edges as possible while maintaining connectivity.
    The original graph remains untouched throughout the process."""
    link_failures = []  # List to store all edges that were killed
    remaining_edges = list(G.edges())  # List of edges to consider in the current iteration
    original_edges = list(G.edges())

    while remaining_edges:
        iteration_links = []
        # Work with a fresh copy of the original graph in each round
        graph_copy = G.copy()
        # Try killing edges from the remaining set of edges
        killable_edges = find_killable_edges(graph_copy, remaining_edges, max_cost, min_cap)

        if not killable_edges:
            #If no more edges can be killed in this round, stop the process
            break
        # Mark the killable edges as killed (but don't change the original graph)

        for edge in killable_edges:
            iteration_links.append(edge)  # Track the edges that are killed
            remaining_edges.remove(edge)  # Remove them from the list of remaining edges
        link_failures.append(iteration_links)
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    survivors = helpers.show_logging_info(G, link_failures, survivors)
    return len(link_failures), survivors
