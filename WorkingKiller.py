import networkx as nx
import helpers


def find_killable_edges(G, edges_to_consider, demands, max_cost, min_cap):
    """Find all edges from 'edges_to_consider' that can be killed while maintaining connectivity."""
    killable_edges = []

    # Attempt to remove each edge and check if the graph remains connected
    for edge in edges_to_consider:
        G.remove_edge(*edge)
        if helpers.check_requirements(G, demands, max_cost, min_cap):
            killable_edges.append(edge)  # This edge can be killed
        else:
            G.add_edge(*edge)  # Add it back if its removal disconnects the graph

    return killable_edges


def iterative_killer(G, demands, max_cost, min_cap):
    """Iterative algorithm to kill as many edges as possible while maintaining connectivity.
    The original graph remains untouched throughout the process."""
    killed_links = []  # List to store all edges that were killed
    remaining_edges = list(G.edges())  # List of edges to consider in the current iteration

    while remaining_edges:
        iteration_links=[]
        # Work with a fresh copy of the original graph in each round
        graph_copy = G.copy()

        # Try killing edges from the remaining set of edges
        killable_edges = find_killable_edges(graph_copy, remaining_edges, demands, max_cost, min_cap)

        if not killable_edges:
            # If no more edges can be killed in this round, stop the process
            break
        # Mark the killable edges as killed (but don't change the original graph)

        for edge in killable_edges:
            iteration_links.append(edge)  # Track the edges that are killed
            remaining_edges.remove(edge)  # Remove them from the list of remaining edges

        killed_links.append(iteration_links)

    return killed_links

# Example usage
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

# Draw Graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
link_failure_scenarios = iterative_killer(G, demands, max_cost, min_cap)
print(link_failure_scenarios)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()