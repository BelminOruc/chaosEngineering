import networkx as nx
from matplotlib import pyplot as plt
import BacktrackTracker
import BruteKiller
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
#logging.info("Backtrack: ")
# Iterate through the list of XML files
#for file in xml_files:
logging.info("--------------------------------------------------------------------------------------")
#file = xml_file
file = 'sndlibcontent/nobel-germany.xml'
logging.info(f'Processing file: {file}')
G, demands = parser.read_sndlib_topology(file)
#helpers.show_plot(G)
logging.info("Number of Edges" )
logging.info(G.number_of_edges())


#print(G.edges.data())
FlowKiller.greedy_flow_killer(G, demands, 7000, 0)
#BacktrackTracker.backtrack_killer(G, demands, 6000, 0)
#BruteKiller.brute_killer(G, demands, 7000, 0)
#DynamicKiller.dynamic_killer(G, demands, 7000, 0)
#WorkingKiller.working_killer(G, demands, 7000, 0)
#RandomKiller.random_killer(G, demands, 60000, 0)

    #print(G.edges)
    #file = 'sndlibcontent/brain.xml'
    # Example usage
logging.info("--------------------------------------------------------------")
print("Finished")