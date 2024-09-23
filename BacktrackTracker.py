import networkx as nx
from matplotlib import pyplot as plt

import helpers

def backtrack_killer(G, demands, max_cost, min_cap):
    """Backtracking algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges(data=True))
    killed_edge_sets = []
    all_edges_killed = set()

    def recursive_remove(temp_graph, current_set):
        nonlocal killed_edge_sets, all_edges_killed

        for edge in original_edges:
            if edge[:2] not in current_set:
                # Store edge attributes before removing
                edge_data = temp_graph.get_edge_data(*edge[:2])
                temp_graph.remove_edge(*edge[:2])
                current_set.add(edge[:2])

                if helpers.check_requirements(temp_graph, demands, max_cost, min_cap):
                    killed_edge_sets.append(list(current_set))
                    all_edges_killed.update(current_set)
                    if all_edges_killed == set(edge[:2] for edge in original_edges):
                        return  # Stop recursion if all edges have been killed at least once
                    recursive_remove(temp_graph, current_set)

                current_set.remove(edge[:2])
                # Restore edge with its attributes
                temp_graph.add_edge(*edge[:2], **edge_data)

    recursive_remove(G.copy(), set())
    print(killed_edge_sets)
    return helpers.count_inner_lists(killed_edge_sets)

file = 'nobel-germany.xml'
#G = parser.read_sndlib_topology(file)
#print("test")
#print(G.edges)
# Add Edges

G = nx.Graph()
G.add_edge("1", "2", capacity=6.0, weight=1.0)
G.add_edge("2", "3", capacity=6.0, weight=1.0)
G.add_edge("2", "4", capacity=6.0, weight=1.0)
G.add_edge("3", "5", capacity=6.0, weight=1.0)
G.add_edge("4", "5", capacity=6.0, weight=1.0)
G.add_edge("1", "3", capacity=6.0, weight=1.0)
G.add_edge("2", "5", capacity=6.0, weight=1.0)
# Initialize demands and other parameters
demands = {
    '1': 1,  # Supply node
    '2': 1,  # Transit node
    '3': 1,  # Transit node
    '4': 1,  # Demand node
    '5': 1,  # Transit node
}

min_cap = 0  # Minimum capacity for edges
max_cost = 30  # Maximum cost constraint

link_failure_scenarios = backtrack_killer(G, demands, max_cost, min_cap)
print(link_failure_scenarios)