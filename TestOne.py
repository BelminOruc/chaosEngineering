import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


def has_edge_disjoint_spanning_trees(graph):
    def is_spanning_tree(graph, tree_edges):
        # Create a subgraph with the edges of the tree
        tree = nx.Graph()
        tree.add_edges_from(tree_edges)
        # Check if the tree is a spanning tree
        return nx.is_connected(tree) and len(tree.edges()) == len(graph.nodes()) - 1

    nodes = graph.nodes()
    edges = list(graph.edges())

    # Generate all possible combinations of edges for the first spanning tree
    for edges1 in combinations(edges, len(nodes) - 1):
        if is_spanning_tree(graph, edges1):
            # Find remaining edges after removing edges1
            remaining_edges = [e for e in edges if e not in edges1]
            # Generate all possible combinations of remaining edges for the second spanning tree
            for edges2 in combinations(remaining_edges, len(nodes) - 1):
                if is_spanning_tree(graph, edges2):
                    return True, edges1, edges2

    return False, None, None


# Example usage
G = nx.Graph()
G.add_node("A")
G.add_edge("A", "B", weight=4)
G.add_edge("B", "D", weight=2)
G.add_edge("A", "C", weight=3)
G.add_edge("C", "D", weight=4)
G.add_edge("D", "E", weight=6)
# Add edges to your graph G
# For example: G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)])

# Check for edge-disjoint spanning trees
has_trees, tree1, tree2 = has_edge_disjoint_spanning_trees(G)

if has_trees:
    print("The graph has two edge-disjoint spanning trees:")
    print("Tree 1:", tree1)
    print("Tree 2:", tree2)
else:
    print("The graph does not have two edge-disjoint spanning trees.")

#myIter = nx.SpanningTreeIterator(G)
#print(next(myIter))
#nx.draw(G, with_labels=True, font_weight='bold')
nx.draw(G, with_labels=True, font_weight='bold')
#plt.draw()
plt.show()
print(nx.shortest_path(G, "A", "E", weight="weight"))
print(G.number_of_edges())
print(G.number_of_nodes())
print(list(G.nodes))
print(list(G))
print(list(G))