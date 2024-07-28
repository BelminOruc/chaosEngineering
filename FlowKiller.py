import networkx as nx
import matplotlib.pyplot as plt

def mutually_exclusive(arr1, arr2):
    # Convert the arrays to sets of tuples for efficient comparison
    set1 = set(tuple(row) for row in arr1)
    set2 = set(tuple(row) for row in arr2)
    # Check if the intersection of the two sets is empty
    return not bool(set1.intersection(set2))


def ensure_demand_and_minimum_flow_met(G, demands, minimum_flow, maxCost):
    """
    Ensures that every node demand is met and the graph has at least the specified minimum flow.

    Parameters:
    G (nx.Graph): Undirected graph with edge weights and capacities.
    demands (dict): Dictionary with node as key and demand as value.
                    Positive values represent demand, and negative values represent supply.
    minimum_flow (float): The minimum total flow that must be met.

    Returns:
    bool: True if demands are met and total flow is at least minimum_flow, False otherwise.
    """
    # Convert undirected graph to directed graph
    DG = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        DG.add_edge(u, v, capacity=data.get('capacity', 0), weight=data.get('weight', 0))
        DG.add_edge(v, u, capacity=data.get('capacity', 0), weight=data.get('weight', 0))

    # Add a super-source and super-sink to balance demands
    super_source = 'super_source'
    super_sink = 'super_sink'
    DG.add_node(super_source)
    DG.add_node(super_sink)

    total_demand = 0
    for node, demand in demands.items():
        if demand > 0:
            DG.add_edge(super_source, node, capacity=demand, weight=0)
            total_demand += demand
        elif demand < 0:
            DG.add_edge(node, super_sink, capacity=-demand, weight=0)

    # Balance the total demand and supply
    DG.nodes[super_source]['demand'] = -total_demand
    DG.nodes[super_sink]['demand'] = total_demand

    # Use the network simplex algorithm to find the minimum cost flow that satisfies demands
    try:
        flow_cost, flow_dict = nx.network_simplex(DG)
    except nx.NetworkXUnfeasible:
        print("Demands not met")
        return False


    # Calculate the total flow from super_source
    total_flow = sum(flow_dict[super_source].values())
    print("total flow", total_flow)
    # Check if the total flow is at least the minimum flow
    if total_flow < minimum_flow:
        print("Not enough flow")
        return False
    if flow_cost > maxCost:
        print("Cost too high", flow_cost)
        return False
    return True

def compute_cap_link_failures(G, demands, minCap, maxCost):
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
                    test = ensure_demand_and_minimum_flow_met(tree1, demands, minCap, maxCost)
                    print("Tree 1 valid?", test)
                    test = ensure_demand_and_minimum_flow_met(tree2, demands, minCap, maxCost)
                    print("Tree 2 valid?", test)
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
            test = ensure_demand_and_minimum_flow_met(tree, demands, minCap, maxCost)

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
G.add_edge("x", "a", capacity=6.0)
G.add_edge("x", "b", capacity=1.0)
G.add_edge("a", "c", capacity=3.0)
G.add_edge("b", "c", capacity=5.0)
G.add_edge("b", "d", capacity=4.0)
G.add_edge("d", "e", capacity=2.0)
G.add_edge("c", "y", capacity=2.0)
G.add_edge("e", "y", capacity=3.0)

demands = {
        'a': 15,  # Supply node
        'b': 0,  # Transit node
        'c': -5,  # Transit node
        'd': -10,  # Demand node
        'e': 0,  # Transit node
        'x': -5,  # Transit node
        'y': 5  # Demand node
    }

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
# Draw edge labels with weights
link_failure_scenarios = compute_cap_link_failures(G, demands,4, 50)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()

