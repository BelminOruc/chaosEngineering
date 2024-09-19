import networkx as nx


def has_disjoint_spanning_trees(G):
    T1 = nx.minimum_spanning_tree(G)
    edges_T1 = set(T1.edges())
    G_copy = G.copy()
    G_copy.remove_edges_from(edges_T1)
    T2 = nx.minimum_spanning_tree(G_copy)
    edges_T2 = set(T2.edges())
    print(edges_T1)
    print(edges_T2)
    print(edges_T1.isdisjoint(edges_T2))
    return T1, T2, edges_T1.isdisjoint(edges_T2)

def compute_link_failures_scenarios(G):
    # Function to check if two spanning trees have disjoint edge sets
    if G.number_of_edges() == 0:
        return "No edges to fail"

    # Check for disjoint spanning trees
    T1, T2, disjoint = has_disjoint_spanning_trees(G)
    if disjoint:
        print("Fail edges in E1 and E2")
        return list(T1.edges()), list(T2.edges())
    else:
        # Initialize link weights
        for e in G.edges:
            G[e[0]][e[1]]['weight'] = 1

        while True:
            # Compute minimum spanning tree (MST)
            T = nx.minimum_spanning_tree(G)
            edges_T = set(T.edges())

            # Fail all links not in the MST
            failed_edges = set(G.edges()) - edges_T

            # Calculate new edge failures sum
            new_edge_failures_sum = sum(G[u][v]['weight'] for u, v in failed_edges)

            # Set weights of failed edges to 0
            for u, v in failed_edges:
                G[u][v]['weight'] = 0

            # Condition to break the loop
            if new_edge_failures_sum == 0 or all(G[u][v]['weight'] == 0 for u, v in G.edges()):
                break

    return failed_edges


# Example usage:
G = nx.petersen_graph()
nx.draw(G, with_labels=True, font_weight='bold')
failed_edges = compute_link_failures_scenarios(G)
print("Failed Edges:", failed_edges)


#plt.draw()
#plt.show()

