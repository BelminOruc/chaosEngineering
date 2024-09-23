import networkx as nx
import matplotlib.pyplot as plt
import helpers

import parser


#Most current version of the greedy algorithm
# Computes a minimum flow, a max cost and checks for all demands

def compute_cap_link_failures(G, demands, max_cost, min_cap):
    # Step 1: Compute link failure scenarios
    link_failures = []
    # Step 2: Check for disjoint spanning trees
    iterator1 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    # Get the first two spanning trees
    iter(iterator1)
    test = False
    tree1 = []
    tree2 = []
    while not test:
        test = False
        try:
            tree1 = next(iterator1)
            iterator2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
            test = helpers.check_requirements(tree1, demands, max_cost, min_cap)
            if test:
                iter(iterator2)
                test = False
                while not test:
                    try:
                        tree2 = next(iterator2)
                        test = helpers.check_requirements(tree2, demands, max_cost, min_cap)
                        if test:
                            test = mutually_exclusive(tree1.edges, tree2.edges)
                    except:
                        break
        except:
            break
    if test:
        # Step 3: Fail links not in T1 and T2
        link_failures.append(list(set(G.edges) - set(tree1.edges)))
        link_failures.append(list(set(G.edges) - set(tree2.edges)))
    else:
        # Step 4: No valid spanning trees
        edge_weights = {e: 1 for e in G.edges}
        it2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
        iter(it2)
        while True:
            # Step 7: Compute minimum weight spanning tree (MST)
            try:
                tree = next(it2)
            except:
                break
            # Step 8: Fail all links not in the MST
            failed_links = [e for e in G.edges if e not in tree.edges]
            if not failed_links:
                break
            link_failures.append(failed_links)

            # Step 9: Calculate sum of new edge failures
            lambda_sum = sum(edge_weights[e] for e in failed_links)
            test = helpers.check_requirements(tree, demands, max_cost, min_cap)
            if test:
                # Step 10: Set weights of failed links to 0
                for e in failed_links:
                    edge_weights[e] = 0
            else:
                link_failures.remove(failed_links)

            # Step 11: Check termination condition
            if lambda_sum == 0 or all(weight == 0 for weight in edge_weights.values()):
                # Search for a spanning tree that can fail not yet terminated edges
                found_valid_tree = False
                while not found_valid_tree:
                    try:
                        tree = next(it2)
                        remaining_edges = [e for e in G.edges if edge_weights[e] != 0]
                        if any(e in tree.edges for e in remaining_edges):
                            found_valid_tree = True
                    except:
                        break
                if not found_valid_tree:
                    break
    return helpers.count_inner_lists(link_failures)


def mutually_exclusive(arr1, arr2):
    # Convert the arrays to sets of tuples for efficient comparison
    set1 = set(tuple(row) for row in arr1)
    set2 = set(tuple(row) for row in arr2)
    # Check if the intersection of the two sets is empty
    return not bool(set1.intersection(set2))


#---------------------------------------------------TEST--------------------------------------------------



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
link_failure_scenarios = compute_cap_link_failures(G, demands, max_cost, min_cap)
print(link_failure_scenarios)
