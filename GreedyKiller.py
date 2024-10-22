import networkx as nx
import matplotlib.pyplot as plt

import helpers


# Check if array 1 and array 2 are mutually exclusive.
# bool: True if the arrays are mutually exclusive, False otherwise.
def mutually_exclusive(arr1, arr2):
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
    tree1 = None
    tree2 = None
    test = False

    while not test:
        try:
            tree1 = next(iterator)
            for tree2_candidate in iterator:
                if tree1.edges.isdisjoint(tree2.edges):
                    tree2 = tree2_candidate
                    test = True
                    break
        except:
            break
    if (test == True):
        # Step 3: Fail links not in T1 and T2
        link_failures.append(list(set(G.edges) - set(tree1.edges)))
        link_failures.append(list(set(G.edges) - set(tree2.edges)))
    else:
        # Step 4: No disjoint spanning trees
        for u, v, data in G.edges(data=True):
            data['weight'] = 1  # Initialize weights to 1

        while True:
            tree = nx.minimum_spanning_tree(G, weight='weight')  # Compute MST
            failed_links = [e for e in G.edges if e not in tree.edges]  # Fail links not in MST
            if not failed_links:
                break
            link_failures.append(failed_links)
            lambda_sum = sum(G[u][v]['weight'] for u, v in failed_links)
            for u, v in failed_links:
                G[u][v]['weight'] = 0  # Set weights of failed links to 0
            if lambda_sum == 0 or all(G[u][v]['weight'] == 0 for u, v in G.edges):
                break
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    survivors=helpers.show_logging_info(G, link_failures, survivors)
    return len(link_failures), survivors


