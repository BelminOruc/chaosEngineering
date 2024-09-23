import networkx as nx
from matplotlib import pyplot as plt
import parser
import os
import glob

# Specify the directory containing the XML files
directory = 'sndlibcontent'

# Use glob to find all XML files in the directory
xml_files = glob.glob(os.path.join(directory, '*.xml'))

# Iterate through the list of XML files
for xml_file in xml_files:
    print(f'Processing file: {xml_file}')
    file= xml_file
    G,demands = parser.read_sndlib_topology(file)
    print(G.edges)
    print(demands)
    print("--------------------------------------------------------------")
    # Add your code to process each XML file here
'''
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'capacity')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.axis('off')
plt.show()
# Add Edges'''

