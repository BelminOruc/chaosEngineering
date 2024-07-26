import networkx as nx
import matplotlib.pyplot as plt

# Check if array 1 and array 2 are mutually exclusive.
#bool: True if the arrays are mutually exclusive, False otherwise.
def mutually_exclusive(arr1, arr2):
    # Convert the arrays to sets of tuples for efficient comparison
    set1 = set(tuple(row) for row in arr1)
    set2 = set(tuple(row) for row in arr2)
    # Check if the intersection of the two sets is empty
    return not bool(set1.intersection(set2))


def compute_link_failures(G, minWeight):

    # Step 1: Compute link failure scenarios
    link_failures = []

    # Step 2: Check for disjoint spanning trees
    iterator1 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    iterator2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    # Get the first two spanning trees
    iter(iterator1)
    sumWeight1=0
    sumWeight2=0
    test= False
    while test==False or sumWeight1 < minWeight or sumWeight2 < minWeight:
        test=False
        try:
            tree1 = next(iterator1)
            print("################################################################")
            #how can we reset the iterator?
            iterator2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
            iter(iterator2)
            while test==False:
                try:
                    tree2 = next(iterator2)
                    print("Tree1:  ")
                    print(tree1.edges)
                    print("Tree2: ")
                    print(tree2.edges)
                    sumWeight1 = sum(tree1.edges[u, v]['weight'] for u, v in tree1.edges())
                    sumWeight2 = sum(tree2.edges[u, v]['weight'] for u, v in tree2.edges())
                    test = mutually_exclusive(tree1.edges, tree2.edges)
                    print(test)
                    print("----------------------------------------------------------------")
                except:
                    break
        except:
             break
    if(test==True and sumWeight1 >= minWeight and sumWeight2 >= minWeight):
        # Step 3: Fail links not in T1 and T2
        link_failures.append(list(set(G.edges) - set(tree1.edges)))
        link_failures.append(list(set(G.edges) - set(tree2.edges)))
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




#G = nx.petersen_graph()

G= nx.Graph();
G.add_edge("1", "2", weight=10)
G.add_edge("2", "3", weight=0.1)
G.add_edge("3", "4", weight=0.1)
G.add_edge("4", "1", weight=12)
G.add_edge("4", "2", weight=0.1)
#G.add_edge("1", "3", weight=4)
""""""
min=10
#nx.draw(G, with_labels=True, font_weight='bold')
#nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))
#plt.show()
# Draw the graph

#Run program and show results
link_failure_scenarios = compute_link_failures(G, min)
print(link_failure_scenarios)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

# Draw edge labels with weights
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Display the graph
plt.axis('off')
plt.show()
