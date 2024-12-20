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

def greedy_flow_killer(G, max_cost, min_cap):
    logging.info("Flowkiller: ")
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
        # Step 4: No valid spanning trees#
        edge_weights = {e: 1 for e in G.edges}
        it2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight', minimum=False)
        iter(it2)
        finished_once = False
        tree = None
        while remaining_edges:  # Continue as long as remaining_edges is not empty
            # Step 7: Compute minimum weight spanning tree (MST)
            if not finished_once:
                try:
                    tree = next(it2)
                except:
                    break
            # Step 8: Fail all links not in the MST
            try:
                failed_links = [e for e in G.edges if e not in tree.edges]
            except:
                break
            if not failed_links:
                break
            link_failures.append(failed_links)

            # Step 9: Calculate sum of new edge failures
            lambda_sum = sum(edge_weights[e] for e in failed_links)
            test = helpers.check_requirements(tree, max_cost, min_cap)
            if test:
                # Step 10: Set weights of failed links to 0
                remaining_edges = [e for e in remaining_edges if e not in failed_links]
                for e in failed_links:
                    edge_weights[e] = 0
            else:
                link_failures.remove(failed_links)

            # Step 11: Check termination condition
            if lambda_sum == 0:
                finished_once = True
                tree=None
                remaining_edges.reverse()
                for link in remaining_edges:
                    try:
                        while not tree:
                            current_tree = next(it2)
                            if link not in current_tree.edges:
                                tree = current_tree
                                break  # Restart the main while loop with the newly found tree
                    except:
                        break
                continue
    survivors = helpers.get_remaining_edges(list(G.edges()), link_failures)
    survivors = helpers.show_logging_info(G, link_failures, survivors)
    return len(link_failures), survivors


