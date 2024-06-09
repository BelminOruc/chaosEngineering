import networkx as nx
import matplotlib.pyplot as plt

# Check if array 1 and array 2 are mutually exclusive.
def mutually_exclusive(arr1, arr2):
    """
    Checks if two 2D arrays are mutually exclusive.

    Args:
        arr1 (list): A 2D list representing the first array.
        arr2 (list): A 2D list representing the second array.

    Returns:
        bool: True if the arrays are mutually exclusive, False otherwise.
    """
    # Convert the arrays to sets of tuples for efficient comparison
    set1 = set(tuple(row) for row in arr1)
    set2 = set(tuple(row) for row in arr2)
    # Check if the intersection of the two sets is empty
    return not bool(set1.intersection(set2))


def compute_link_failures(G):
    # Step 1: Compute link failure scenarios
    link_failures = []
    # Step 2: Check for disjoint spanning trees
    iterator = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    # Get the first two spanning trees
    iter(iterator)
    tree1 = next(iterator)
    tree2 = next(iterator)
    test= mutually_exclusive(nx.to_numpy_array(tree1),nx.to_numpy_array(tree2))
    while test==False:
        try:
            tree2 = next(iterator)
            test = mutually_exclusive(nx.to_numpy_array(tree1), nx.to_numpy_array(tree2))
        except:
            break
    if(test==True):
        T1 = nx.maximum_spanning_tree(G)
        G.remove_edges_from(T1.edges)
        T2 = nx.maximum_spanning_tree(G)
        G.add_edges_from(T1.edges)
        # Step 3: Fail links not in T1 and T2
        link_failures.append(list(set(G.edges) - set(T1.edges)))
        link_failures.append(list(set(G.edges) - set(T2.edges)))
    else:
        # Step 4: No disjoint spanning trees
        edge_weights = {e: 1 for e in G.edges}
        it2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
        iter(it2)
        while True:
            # Step 7: Compute minimum weight spanning tree (MST)
            try:
                tree = next(it2)
            except:
                break
            print("In schleife")
            # Step 8: Fail all links not in the MST
            failed_links = [e for e in G.edges if e not in tree.edges]
            if not failed_links:
                break
            link_failures.append(failed_links)
            # Step 9: Calculate sum of new edge failures
            lambda_sum = sum(edge_weights[e] for e in failed_links)
            # Step 10: Set weights of failed links to 0
            for e in failed_links:
                edge_weights[e] = 0
            # Step 11: Check termination condition
            if lambda_sum == 0 or all(weight == 0 for weight in edge_weights.values()):
                break
    return link_failures




# Example usage
G = nx.petersen_graph()
#G= nx.Graph();
#G.add_edge("1", "2", weight=4)
#G.add_edge("2", "3", weight=2)
#G.add_edge("3", "4", weight=3)
#G.add_edge("4", "1", weight=3)
#G.add_edge("1", "3", weight=4)
nx.draw(G, with_labels=True, font_weight='bold')


link_failure_scenarios = compute_link_failures(G)
print(link_failure_scenarios)
plt.show()