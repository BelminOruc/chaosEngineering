import networkx as nx
import helpers
'''
Algorithm BacktrackingLinkKilling(N = (V, E), current_set)
    if current_edge > |E| then
        if isConnected(V, E w.o. current_set) then
            return current_set // Valid set of killed links

        return ∅ // Not valid

    // Include this edge in the current set to kill it
    current_set.add(E[current_edge])
    result_with_edge = BacktrackingLinkKilling(N, current_set, current_edge + 1)

    // Exclude this edge from the current set and try again
    current_set.remove(E[current_edge])
    result_without_edge = BacktrackingLinkKilling(N, current_set, current_edge + 1)

    return bestResult(result_with_edge, result_without_edge)
'''




def backtrack_killer(G, demands, max_cost, min_cap):
    """Backtracking algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges())
    killed_edge_sets = []
    all_edges_killed = set()

    def recursive_remove(temp_graph, current_set):
        nonlocal killed_edge_sets, all_edges_killed

        for edge in original_edges:
            if edge not in current_set:
                temp_graph.remove_edge(*edge)
                current_set.add(edge)

                if helpers.check_requirements(temp_graph, demands, max_cost, min_cap ):
                    killed_edge_sets.append(list(current_set))
                    all_edges_killed.update(current_set)
                    if all_edges_killed == set(original_edges):
                        return  # Stop recursion if all edges have been killed at least once
                    recursive_remove(temp_graph, current_set)

                current_set.remove(edge)
                temp_graph.add_edge(*edge)

    recursive_remove(G.copy(), set())

    return killed_edge_sets

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

# Draw Graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
link_failure_scenarios = backtrack_killer(G, demands, max_cost, min_cap)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()