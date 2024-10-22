import networkx as nx

import Analysis
import helpers
import parser
import os
import glob
import logging

# Configure logging
logging.basicConfig(filename='analysis.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Specify the directory containing the XML files
#directory = 'toobigtohandle'
snd_directory = 'sndlibcontent'
tzoo_directory = 'tzoocontent'
# Use glob to find all XML files in the directory
xml_files = glob.glob(os.path.join(snd_directory, '*.xml'))
gml_files = glob.glob(os.path.join(tzoo_directory, '*.gml'))
# Define parameters
G_SND=[]
G_TZOO=[]
max_costs = []
min_flows = []
five = []
twenty = []
seventh = []
halfed = []
counter = 0
for file in gml_files:
    try:
        G= nx.read_gml(file)
        print("Processing file: " +str(counter)+":   " + str(file))
        #min_flows.append(0)
        #max_costs.append(0)
        G_TZOO.append(G)
        counter += 1
    except:
        continue
counter = 0
for file in xml_files:
    print("Processing file: " +str(counter) + str(file))
    G, demands = parser.read_sndlib_topology(file)
    G_SND.append(G)
    highest_cost, five_percent, twenty_percent,  half,  lowest_flow = helpers.get_test_values(G)
    max_costs.append(highest_cost)
    five.append(five_percent)
    twenty.append(twenty_percent)
    halfed.append(half)
    min_flows.append(lowest_flow)

# Run the algorithms
#Write here how to run the experiments using Analysis.py+
helpers.clear_files()
logging.info("#################################All edges can be killed################################################")
Analysis.run_tests(G_SND, min_flows, max_costs, " 100\%")
logging.info("#################################99% of edges can be killed################################################")
#Analysis.run_tests(G_SND, min_flows, five, " 99\%")
logging.info("#################################95% of edges can be killed################################################")
#Analysis.run_tests(G_SND, min_flows, twenty , " 95\%")
logging.info("#################################50% of edges can be killed################################################")
#Analysis.run_tests(G_SND, min_flows, halfed, " 50\%")