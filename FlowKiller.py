import networkx as nx
import matplotlib.pyplot as plt

def mutually_exclusive(arr1, arr2):
    # Convert the arrays to sets of tuples for efficient comparison
    set1 = set(tuple(row) for row in arr1)
    set2 = set(tuple(row) for row in arr2)
    # Check if the intersection of the two sets is empty
    return not bool(set1.intersection(set2))


def check_flow_requirements(G, demands, minflow, maxcost):
    """
    Check if a flow exists that meets all the node demands with a maximum cost and a minimum flow.

    Parameters:
    G (nx.DiGraph): Directed graph with edge capacities and costs.
    demands (dict): Dictionary with node demands, e.g., {node1: demand1, node2: demand2, ...}
    maxcost (int): Maximum allowable cost.
    minflow (int): Minimum required flow.

    Returns:
    bool: True if requirements are met, False otherwise.
    """
    # Ensure the graph is directed for flow calculations
    if not isinstance(G, nx.DiGraph):
        G = G.to_directed()

    # Add demand attribute to nodes
    for node, demand in demands.items():
        G.nodes[node]['demand'] = demand

    try:
        # Calculate minimum cost flow
        flow_cost, flow_values = nx.network_simplex(G)

        # Check if the total cost exceeds the maximum allowed cost
        print("flow_cost: ", flow_cost)
        if flow_cost > maxcost:
            return False

        # Calculate the total flow through the network
        total_flow = sum(sum(flow_values[u][v] for v in flow_values[u]) for u in flow_values)
        G = G.to_undirected()
        # Check if the total flow is less than the minimum required flow
        print("total_flow: ", total_flow)
        if total_flow < minflow:
            return False

        # If both conditions are satisfied
        return True
    except nx.NetworkXUnfeasible:
        # If no feasible flow exists
        return False

def compute_cap_link_failures(G, demands, minCap, maxCost):
    # Step 1: Compute link failure scenarios
    link_failures = []

    # Step 2: Check for disjoint spanning trees
    iterator1 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    iterator2 = nx.algorithms.tree.mst.SpanningTreeIterator(G, weight='weight')
    # Get the first two spanning trees
    iter(iterator1)
    test = False
    while test == False:
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
                    test = check_flow_requirements(tree1, demands, minCap, maxCost)
                    print("Tree 1 valid?", test)
                    if test == True:
                        test = check_flow_requirements(tree2, demands, minCap, maxCost)
                        print("Tree 2 valid?", test)
                        if test == True:
                            test = mutually_exclusive(tree1.edges, tree2.edges)
                            print(test)
                    print("----------------------------------------------------------------")
                except:
                    break
        except:
            break
#TODO: Anpassen
    if (test == True):
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
            test = check_flow_requirements(tree, demands, minCap, maxCost)

            if test == True:
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
G.add_edge("x", "a", capacity=6.0, weight=1.0)
G.add_edge("x", "b", capacity=1.0, weight=1.0)
G.add_edge("a", "c", capacity=3.0, weight=1.0)
G.add_edge("b", "c", capacity=5.0, weight=1.0)
G.add_edge("b", "d", capacity=4.0, weight=1.0)
G.add_edge("d", "e", capacity=2.0, weight=1.0)
G.add_edge("c", "y", capacity=2.0, weight=1.0)
G.add_edge("e", "y", capacity=3.0, weight=1.0)

# Initialize demands and other parameters
demands = {
    'a': 0,  # Supply node
    'b': 0,   # Transit node
    'c': 0,  # Transit node
    'd': 0, # Demand node
    'e': 0,   # Transit node
    'x': 0,  # Transit node
    'y': 0    # Demand node
}
minCap = 0  # Minimum capacity for edges
maxCost = 10  # Maximum cost constraint

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
# Draw edge labels with weights
link_failure_scenarios = compute_cap_link_failures(G, demands,4, 50)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()

