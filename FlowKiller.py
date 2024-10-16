import glob
import itertools
import logging
import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import helpers
import parser

# I think its time to accept that the flowkiller is just really bad at looking at other requirements
# MSTs ensure that the graph will always be connected, but it does not guarantee that the graph will be able to handle the demands

def greedy_flow_killer(G, demands, max_cost, min_cap):
    # Step 1: Compute link failure scenarios
    link_failures = []
    remaining_edges = list(G.edges)
    # Step 2: Check for disjoint spanning trees
    iterator = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    tree1 = None
    tree2 = None
    test = False

    while not test:
        try:
            tree1 = next(iterator)
            if helpers.check_requirements(tree1, max_cost, min_cap):
                for tree2_candidate in iterator:
                    if helpers.check_requirements(tree2_candidate, max_cost, min_cap):
                        if tree1.edges.isdisjoint(tree2.edges):
                            tree2 = tree2_candidate
                            test = True
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

        while remaining_edges:  # Step 6: Repeat
            tree = nx.minimum_spanning_tree(G, weight='weight')  # Step 7: Compute MST
            print(tree.edges)
            # Step 8: Fail all links not in the MST
            failed_links = [e for e in G.edges if e not in tree.edges]
            if not failed_links:
                break
            link_failures.append(failed_links)

            # Step 9: Calculate sum of new edge failures
            lambda_sum = sum(edge_weights[e] for e in failed_links)
            test = helpers.check_requirements(tree, max_cost, min_cap)
            if test:
                # Step 10: Set weights of failed links to 0
                all_links = [e for e in all_links if e not in failed_links]
                for e in failed_links:
                    edge_weights[e] = 0
            else:
                link_failures.remove(failed_links)
            print(test)
            print(lambda_sum)
            # Step 11: Check termination condition
            if lambda_sum == 0:
                break
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    helpers.showLoggingInfo(link_failures, survivors)
    return len(link_failures), len(survivors)


