import networkx as nx
import helpers

def iterative_killer(G, max_cost, min_cap):
    """Iterate through all edges and try to kill them one by one."""
    original_edges = list(G.edges())
    link_failures = []

    for edge in original_edges:
        temp_graph = G.copy()
        temp_graph.remove_edge(*edge)

        if helpers.check_requirements(temp_graph, max_cost, min_cap):
            link_failures.append(edge)
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    survivors = helpers.show_logging_info(G, link_failures, survivors)
    return len(link_failures), survivors