import networkx as nx
import matplotlib.pyplot as plt

def mutually_exclusive(arr1, arr2):
    # Convert the arrays to sets of tuples for efficient comparison
    set1 = set(tuple(row) for row in arr1)
    set2 = set(tuple(row) for row in arr2)
    # Check if the intersection of the two sets is empty
    return not bool(set1.intersection(set2))


#TODO: Fix
def test_edge_capacities(G, min_capacity):
    # Create a copy of the graph to avoid modifying the original
    # Create a copy of the graph to avoid modifying the original
    H = G.copy()

    # Add source and sink nodes
    H.add_node('source')
    H.add_node('sink')

    # Connect source to all nodes and all nodes to sink
    for node in G.nodes():
        H.add_edge('source', node, capacity=min_capacity)
        H.add_edge(node, 'sink', capacity=min_capacity)

    # Convert the undirected graph to a directed graph
    H_directed = H.to_directed()

    # Set capacities for both directions of each edge
    for u, v, data in H_directed.edges(data=True):
        if 'capacity' not in data:
            H_directed[u][v]['capacity'] = min_capacity
            H_directed[v][u]['capacity'] = min_capacity

    # Calculate maximum flow
    flow_value, _ = nx.maximum_flow(H_directed, 'source', 'sink')

    # Check if flow value equals expected value
    expected_flow = len(G.nodes()) * min_capacity
    return flow_value == expected_flow


def compute_cap_link_failures(G, minCap):
    # Step 1: Compute link failure scenarios
    link_failures = []

    # Step 2: Check for disjoint spanning trees
    iterator1 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    iterator2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    # Get the first two spanning trees
    iter(iterator1)
    sumCap1 = 0
    sumCap2 = 0
    test = False
    while test == False or sumCap1 < minCap or sumCap2 < minCap:
        test = False
        try:
            tree1 = next(iterator1)
            print("################################################################")
            #how can we reset the iterator?
            iterator2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
            iter(iterator2)
            while test == False:
                try:
                    tree2 = next(iterator2)
                    print("Tree1:  ")
                    print(tree1.edges)
                    print("Tree2: ")
                    print(tree2.edges)
                    #testing if both trees have the necessary capacitys for all edges
                    test = test_edge_capacities(tree1, minCap)
                    print("Tree 1 Capacity enough?")
                    print(test)
                    test = test_edge_capacities(tree2, minCap)
                    print("Tree 2 Capacity enough?")
                    print(test)
                    test = mutually_exclusive(tree1.edges, tree2.edges)
                    print(test)
                    print("----------------------------------------------------------------")
                except:
                    break
        except:
            break
#TODO: Anpassen
    if (test == True and sumCap1 >= minCap and sumCap2 >= minCap):
        # Step 3: Fail links not in T1 and T2
        link_failures.append(list(set(G.edges) - set(tree1.edges)))
        link_failures.append(list(set(G.edges) - set(tree2.edges)))
    else:
        # Step 4: No disjoint spanning trees
        edge_weights = {e: 1 for e in G.edges}
        edge_limit = {e: G.edges[e]['capacity'] for e in G.edges}
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
            cap_sum = sum(edge_limit[e] for e in failed_links)

            if cap_sum > minCap:

                # Step 10: Set weights of failed links to 0
                for e in failed_links:
                    edge_weights[e] = 0
            else:
                link_failures.remove(failed_links)

            # Step 11: Check termination condition
            if lambda_sum == 0 or all(weight == 0 for weight in edge_weights.values()):
                break
    return link_failures


G = nx.Graph()
G.add_node("a", demand=-5)
G.add_node("b", demand=-5)
G.add_node("c", demand=-5)
G.add_node("d", demand=-5)
G.add_node("e", demand=-5)
G.add_node("x", demand=-5)
G.add_node("y", demand=-5)
G.add_edge("x", "a", capacity=6.0)
G.add_edge("x", "b", capacity=1.0)
G.add_edge("a", "c", capacity=3.0)
G.add_edge("b", "c", capacity=5.0)
G.add_edge("b", "d", capacity=4.0)
G.add_edge("d", "e", capacity=2.0)
G.add_edge("c", "y", capacity=2.0)
G.add_edge("e", "y", capacity=3.0)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
# Draw edge labels with weights
link_failure_scenarios = compute_cap_link_failures(G,22)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()

