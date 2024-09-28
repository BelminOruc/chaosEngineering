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
    #print(removable_edges)
    return helpers.count_inner_lists(removable_edges)

