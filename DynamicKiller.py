import networkx as nx
import matplotlib.pyplot as plt
import helpers

# Fill the DP table
def dynamic_killer(G, demands, max_cost, min_cap):
    """Dynamic Programming algorithm to find all edges that can be killed while maintaining connectivity."""
    original_edges = list(G.edges())
    n = len(original_edges)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    removable_edges = []

    # Fill the DP table
    for i in range(1, n + 1):
        edge_to_remove = original_edges[i - 1]
        temp_graph = G.copy()

        if temp_graph.has_edge(*edge_to_remove):
            temp_graph.remove_edge(*edge_to_remove)

        if helpers.check_requirements(temp_graph, demands, max_cost, min_cap):  # Check if the graph remains connected
            dp[i][1] = 1  # We can remove this edge
            removable_edges.append([edge_to_remove])

        for j in range(2, n + 1):
            dp[i][j] = dp[i - 1][j]  # Not removing this edge
            if dp[i - 1][j - 1] > 0:  # Check if we can remove this edge
                if temp_graph.has_edge(*edge_to_remove):
                    temp_graph.remove_edge(*edge_to_remove)

                if helpers.check_requirements(temp_graph, demands, max_cost, min_cap):
                    dp[i][j] = max(dp[i][j], dp[i - 1][j - 1] + 1)
                    if len(removable_edges) < j:
                        removable_edges.append([])
                    if edge_to_remove not in removable_edges[j - 1]:
                        removable_edges[j - 1].append(edge_to_remove)
                temp_graph.add_edge(*edge_to_remove)  # Restore the edge
    return helpers.count_inner_lists(removable_edges)


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
link_failure_scenarios = dynamic_killer(G, demands, max_cost, min_cap)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()
