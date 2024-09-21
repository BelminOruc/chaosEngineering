import networkx as nx
import random
import helpers
'''
Algorithm RandomLinkKilling(N = (V, E), iterations)
    max_killed_links = 0
    best_killed_set = ∅

    for i from 1 to |E| do
        for j from 1 to iterations do
            random_set S = RandomSubset(E / best_killed_set)

            if isConnected(V, E / (best_killed_set ∪ S)) then
                killed_count = |best_killed_set ∪ S|
                if killed_count > max_killed_links then
                    max_killed_links = killed_count
                    best_killed_set = best_killed_set ∪ S

    return best_killed_set
'''


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

            if helpers.check_requirements(temp_graph):
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

    return list(killed_edge_sets)


# Example usage
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
link_failure_scenarios = random_killer(G, demands, max_cost, min_cap)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()