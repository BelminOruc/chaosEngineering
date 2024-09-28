import networkx as nx
from matplotlib import pyplot as plt
import BacktrackTracker
import CleverBruteKiller
import DynamicKiller
import FlowKiller
import RandomKiller
import WorkingKiller
import helpers
import parser
import os
import glob
import logging

# Configure logging
logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Specify the directory containing the XML files
directory = 'sndlibcontent'

# Use glob to find all XML files in the directory
xml_files = glob.glob(os.path.join(directory, '*.xml'))
logging.info("Backtrack: ")
# Iterate through the list of XML files
for file in xml_files:
    logging.info(f'Processing file: {file}')
#file = xml_file
    G, demands = parser.read_sndlib_topology(file)
    logging.info("Number of Edges" )
    logging.info(G.number_of_edges())
    logging.info("DynamicKiller: ")
    logging.info(DynamicKiller.dynamic_killer(G, demands, 600000, 0))
    logging.info("Flowkiller: ")
    logging.info(FlowKiller.greedy_flow_killer(G, demands, 600000, 0))
    #logging.info("Backtrack: ")
    #logging.info(BacktrackTracker.backtrack_killer(G, demands, 60000, 0))
    #logging.info("CleverBrute: ")
    #logging.info(CleverBruteKiller.clever_brute_killer(G, demands, 60000, 0))
    #logging.info("Random: ")
    #logging.info(RandomKiller.random_killer(G, demands, 60000, 0))
    logging.info("Workingkiller: ")
    logging.info(WorkingKiller.working_killer(G, demands, 60000, 0))
    #print(G.edges)
    #file = 'sndlibcontent/brain.xml'
    #print(demands)
#      logging.info(G.edges)
#     logging.info(demands)
# Example usage
logging.info("--------------------------------------------------------------")
print("Finished")
# Add your code to process each XML file here
'''
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
'''