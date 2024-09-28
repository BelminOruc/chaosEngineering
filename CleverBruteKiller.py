import networkx as nx
from itertools import combinations
import helpers


def clever_brute_killer(G, demands, max_cost, min_cap):
    """Brute Force algorithm to find all edges that can be killed while maintaining connectivity."""
    edges = list(G.edges())
    killed_links = []

    for r in range(1, len(edges) + 1):  # r is the size of the subset
        print("try")
        for subset in combinations(edges, r):
            print("trying")
            # Create a new graph without the edges in the subset
            temp_graph = G.copy()
            temp_graph.remove_edges_from(subset)

            # Check if the modified graph is still connected
            if helpers.check_requirements(temp_graph, demands, max_cost, min_cap):
                killed_links.append(list(subset))
                #killed_links = remove_smaller_tuples(killed_links)
                #killed_links = remove_redundant_sublists(killed_links)
    #print(killed_links)
    return  helpers.count_inner_lists(killed_links)


def remove_redundant_sublists(lst):
    result = []  # To store non-redundant sublists

    for i in range(len(lst)):
        current_sublist = lst[i]

        # Step 1: Collect all tuples from other sublists except the current one
        other_tuples = set()
        for j in range(len(lst)):
            if i != j:
                other_tuples.update(lst[j])  # Add all tuples from other sublists to the set

        # Step 2: Check if the current sublist is redundant
        is_redundant = all(tup in other_tuples for tup in current_sublist)

        # Step 3: If the current sublist is not redundant, keep it
        if not is_redundant:
            result.append(current_sublist)

    return result

    # Example usage:

    return True


def remove_smaller_tuples(lst):
    lst = sorted(lst, key=len)

    result = []

    for i in range(len(lst)):
        is_subsequence = False

        # Compare the current sublist with all other sublists that are longer
        for j in range(i + 1, len(lst)):
            if set(lst[i]).issubset(lst[j]):
                is_subsequence = True
                break

        # If the current sublist is not a subsequence of a larger sublist, keep it
        if not is_subsequence:
            result.append(lst[i])

    return result

